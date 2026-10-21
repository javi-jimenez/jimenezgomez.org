<?php
/* =============================================================================
   Servidor de formularios — endpoint de contacto
   -----------------------------------------------------------------------------
   Un único endpoint reutilizable por TODOS los sitios de la cuenta. Cada sitio
   copia este fichero en su raíz (con su propio estilo en el HTML) y todos los
   mensajes aterrizan en el MISMO directorio compartido:

       <home>/msgs/      →  /home/brisecw/msgs/

   Un fichero por mensaje (constancia), en Markdown:

       laia-20261016-145233-7f3a1c.md

   El directorio está FUERA de los docroots (no es accesible por URL) y FUERA de
   las carpetas de cada sitio, así que `make deploy` (mirror --delete) NO lo
   toca. Se revisa por FTP:  `make inbox`  (trae los nuevos) y/o rsync propio.

   NO envía correo (el hosting sale por una IP no autorizada en el SPF del
   dominio). Protecciones: honeypot + token firmado (HMAC) + límite por IP +
   comprobación de Origin. El destino es fijo: no acepta un "to" del cliente,
   por lo que no puede usarse como relay.
   ========================================================================== */

error_reporting(E_ALL);
ini_set('display_errors', '0');
ini_set('log_errors', '1');

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

// --- Configuración ----------------------------------------------------------
const MSGS_DIRNAME  = 'msgs';       // compartido, hermano de los docroots
const TOKEN_MIN_AGE = 2;            // s: por debajo, es un bot
const TOKEN_MAX_AGE = 7200;         // s: validez del token (2 h)
const RATE_MAX      = 8;            // envíos por IP...
const RATE_WINDOW   = 3600;         // ...por hora (los intentos inválidos también cuentan)
const MAX_NAME      = 120;
const MAX_EMAIL     = 160;
const MAX_SUBJECT   = 160;
const MAX_MESSAGE   = 5000;

// Orígenes EXTRA autorizados (además del mismo origen, que se acepta siempre).
// Añade aquí un dominio solo si va a publicar el formulario desde OTRO dominio.
const ALLOWED_ORIGINS = [
    'https://laia.brisecom.org',
    'https://brisecom.org',
    'https://www.brisecom.org',
    'https://jimenezgomez.org',
    'https://www.jimenezgomez.org',
];

/** Responde en JSON y termina. */
function out(int $code, array $payload): void {
    http_response_code($code);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

/** Directorio compartido de mensajes (fuera del docroot). */
function msgs_dir(): string {
    $env = getenv('FORMS_MSGS_DIR');                 // override (pruebas locales)
    $dir = $env !== false && $env !== '' ? $env : dirname(__DIR__) . '/' . MSGS_DIRNAME;

    if (!is_dir($dir) && !@mkdir($dir, 0755, true)) {
        out(500, ['ok' => false, 'error' => 'storage_unavailable']);
    }
    if (!is_writable($dir)) {
        out(500, ['ok' => false, 'error' => 'storage_unavailable']);
    }
    return rtrim($dir, '/');
}

/** Secreto para firmar tokens; se genera solo la primera vez. */
function secret(string $dir): string {
    $file = $dir . '/.secret.key';
    if (!is_file($file)) {
        @file_put_contents($file, bin2hex(random_bytes(32)), LOCK_EX);
        @chmod($file, 0600);
    }
    $s = @file_get_contents($file);
    return is_string($s) ? trim($s) : '';
}

/** Etiqueta del sitio a partir del host (laia, brisecom, jimenezgomez…). */
function site_label(): string {
    $host = strtolower((string) ($_SERVER['HTTP_HOST'] ?? 'unknown'));
    $host = preg_replace('/:\d+$/', '', $host);          // sin puerto
    $host = preg_replace('/^www\./', '', $host);         // sin www
    $label = preg_replace('/[^a-z0-9]+/', '-', $host);   // saneado
    return trim($label ?: 'unknown', '-');
}

/** Límite de envíos por IP (ventana deslizante simple). */
function rate_limited(string $dir, string $ip): bool {
    $file = $dir . '/.ratelimit.json';
    $now  = time();
    $fp   = @fopen($file, 'c+');
    if (!$fp) {
        return false;                                    // ante la duda, no bloquear
    }
    flock($fp, LOCK_EX);
    $data = json_decode((string) stream_get_contents($fp), true);
    if (!is_array($data)) {
        $data = [];
    }
    foreach ($data as $k => $times) {
        $times = array_values(array_filter((array) $times, fn($t) => $t > $now - RATE_WINDOW));
        if ($times) { $data[$k] = $times; } else { unset($data[$k]); }
    }
    $key     = hash('sha256', $ip);
    $hits    = $data[$key] ?? [];
    $limited = count($hits) >= RATE_MAX;
    if (!$limited) {
        $hits[] = $now;
        $data[$key] = $hits;
    }
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data));
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    return $limited;
}

/** Longitud en caracteres UTF-8 (sin depender de mbstring). */
function u_len(string $s): int {
    if (function_exists('mb_strlen')) {
        return mb_strlen($s, 'UTF-8');
    }
    return (int) preg_match_all('/./us', $s);
}

/** Trunca a N caracteres UTF-8 (sin depender de mbstring). */
function u_cut(string $s, int $max): string {
    if (function_exists('mb_substr')) {
        return mb_substr($s, 0, $max, 'UTF-8');
    }
    if (preg_match('/^.{0,' . $max . '}/us', $s, $m) === 1) {
        return $m[0];
    }
    return substr($s, 0, $max);   // último recurso (podría partir un carácter)
}

/** Limpia una cadena de entrada (sin caracteres de control inyectables). */
function clean(string $v, int $max, bool $multiline = false): string {
    $v = str_replace(["\r\n", "\r"], "\n", $v);
    $pattern = $multiline ? '/[^\P{C}\n\t]/u' : '/[^\P{C}\t]/u';
    $v = preg_replace($pattern, '', $v) ?? '';
    return u_cut(trim($v), $max);
}

/** Escribe el fichero del mensaje (exclusivo, sin sobrescribir). */
function save_message(string $dir, array $m): string {
    $safe = fn(string $s) => preg_replace('/[^A-Za-z0-9._-]+/', '-', $s);
    $file = sprintf(
        '%s/%s-%s-%s.md',
        $dir,
        $safe($m['site']),
        $m['at']->format('Ymd-His'),
        bin2hex(random_bytes(3))
    );

    $body = $m['message'] !== '' ? $m['message'] : '(empty)';
    $md = "---\n"
        . "site: {$m['site']}\n"
        . "date: {$m['at']->format(DateTimeInterface::ATOM)}\n"
        . "name: {$m['name']}\n"
        . "email: {$m['email']}\n"
        . "subject: {$m['subject']}\n"
        . "ip_hash: {$m['ip_hash']}\n"
        . "user_agent: {$m['ua']}\n"
        . "referer: {$m['ref']}\n"
        . "---\n\n"
        . $body . "\n";

    if (@file_put_contents($file, $md, LOCK_EX) === false) {
        out(500, ['ok' => false, 'error' => 'write_failed']);
    }
    return basename($file);
}

/** Comprueba si un Origin está autorizado. */
function origin_allowed(string $origin): bool {
    if ($origin === '') {
        return true;                              // sin Origin: no aplicable
    }
    if (in_array($origin, ALLOWED_ORIGINS, true)) {
        return true;                              // lista blanca explícita
    }
    // Mismo origen: el host del Origin debe coincidir con el del request.
    // Así el endpoint vale para cualquier sitio de la cuenta sin listas.
    $oHost = parse_url($origin, PHP_URL_HOST);
    $rHost = preg_replace('/:\d+$/', '', (string) ($_SERVER['HTTP_HOST'] ?? ''));
    return $oHost !== null && $oHost !== false
        && strcasecmp((string) $oHost, (string) $rHost) === 0;
}

// ---------------------------------------------------------------------------
// AVISO POR CORREO (opcional) — el mensaje se guarda SIEMPRE en /msgs/
//
// El correo es solo un extra para enterarse antes. Si el SMTP falla, el
// formulario sigue respondiendo "ok", el .md ya está escrito y el error queda
// en /msgs/.mail.log. Nunca se pierde un mensaje porque el correo no salga.
//
// Configuración: /msgs/.smtp.json (FUERA del docroot → 404 por URL, y el
// `mirror --delete` del deploy no lo toca). Ver docs/contact-smtp.md.
// ---------------------------------------------------------------------------

/** Lee la configuración SMTP; null si no está o está incompleta. */
function smtp_config(string $dir): ?array {
    $file = getenv('FORMS_SMTP_CONFIG');
    if ($file === false || $file === '') {
        $file = $dir . '/.smtp.json';
    }
    if (!is_file($file)) {
        return null;
    }
    $c = json_decode((string) @file_get_contents($file), true);
    if (!is_array($c)) {
        return null;
    }
    foreach (['host', 'user', 'pass', 'from', 'to'] as $k) {
        if (!isset($c[$k]) || !is_string($c[$k]) || $c[$k] === '') {
            return null;
        }
    }
    $c += [
        'port'      => 587,
        'secure'    => 'tls',    // tls (587 + STARTTLS) | ssl (465) | none (pruebas)
        'from_name' => '',
        'timeout'   => 10,
    ];
    return $c;
}

/** Colapsa espacios y saltos de línea (evita inyección de cabeceras). */
function one_line(string $s): string {
    return trim((string) preg_replace('/\s+/u', ' ', $s));
}

/** Cabeceras del aviso (RFC 5322, UTF-8 en base64). */
function mail_headers(array $cfg, string $subject, string $replyTo, string $site): string {
    $from = (string) $cfg['from'];
    $name = one_line((string) ($cfg['from_name'] ?? ''));
    $fromHdr = $name !== ''
        ? '=?UTF-8?B?' . base64_encode($name) . '?= <' . $from . '>'
        : '<' . $from . '>';

    $at     = strrchr($from, '@');
    $domain = $at !== false ? substr($at, 1) : 'localhost';

    $headers = [
        'Date: ' . date('r'),
        'From: ' . $fromHdr,
        'To: <' . $cfg['to'] . '>',
        'Reply-To: <' . $replyTo . '>',
        'Subject: =?UTF-8?B?' . base64_encode(one_line($subject)) . '?=',
        'Message-ID: <' . bin2hex(random_bytes(8)) . '@' . $domain . '>',
        'X-Mailer: contact.php (' . one_line($site) . ')',
        'Auto-Submitted: auto-generated',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ];
    return implode("\r\n", $headers);
}

/** Cuerpo legible del aviso. */
function mail_body(array $m, string $file): string {
    return "Nuevo mensaje desde el formulario web\n"
        . str_repeat('=', 38) . "\n"
        . "Sitio:     {$m['site']}\n"
        . "Fecha:     {$m['at']->format('Y-m-d H:i:s')}\n"
        . "Nombre:    {$m['name']}\n"
        . "Email:     {$m['email']}\n"
        . "Asunto:    {$m['subject']}\n"
        . "Fichero:   {$file}\n"
        . "IP hash:   {$m['ip_hash']}\n"
        . "Navegador: {$m['ua']}\n"
        . "Referer:   {$m['ref']}\n"
        . str_repeat('-', 38) . "\n\n"
        . $m['message'] . "\n";
}

/** Ejecuta un comando SMTP y devuelve [código, respuesta]. */
function smtp_cmd($fp, string $line = ''): array {
    if ($line !== '') {
        fwrite($fp, $line . "\r\n");
    }
    $resp = '';
    while (($l = fgets($fp, 1024)) !== false) {
        $resp .= $l;
        if (strlen($l) < 4 || $l[3] === ' ') {      // "250-" sigue, "250 " acaba
            break;
        }
    }
    if ($resp === '') {
        throw new RuntimeException('sin respuesta del servidor');
    }
    return [(int) substr($resp, 0, 3), rtrim($resp)];
}

/** Igual que smtp_cmd pero exige uno de los códigos esperados. */
function smtp_expect($fp, string $line, array $ok): string {
    [$code, $resp] = smtp_cmd($fp, $line);
    if (!in_array($code, $ok, true)) {
        throw new RuntimeException('SMTP ' . $code . ': ' . substr($resp, 0, 200));
    }
    return $resp;
}

/** Envía un mensaje ya formado (cabeceras + cuerpo) por SMTP autenticado. */
function smtp_send(array $cfg, string $message): void {
    $host    = (string) $cfg['host'];
    $port    = (int) $cfg['port'];
    $secure  = strtolower((string) $cfg['secure']);
    $timeout = max(3, (int) $cfg['timeout']);

    $target = ($secure === 'ssl' ? 'ssl://' : '') . $host . ':' . $port;
    $errno  = 0;
    $errstr = '';
    $fp = @stream_socket_client($target, $errno, $errstr, $timeout);
    if (!$fp) {
        throw new RuntimeException('conexión: ' . ($errstr !== '' ? $errstr : 'fallo'));
    }
    stream_set_timeout($fp, $timeout);

    try {
        smtp_expect($fp, '', [220]);

        $ehlo = 'EHLO ' . (gethostname() ?: 'localhost');
        smtp_expect($fp, $ehlo, [250]);

        if ($secure === 'tls') {
            smtp_expect($fp, 'STARTTLS', [220]);
            if (@stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT) !== true) {
                throw new RuntimeException('STARTTLS rechazado');
            }
            smtp_expect($fp, $ehlo, [250]);          // capacidades tras el TLS
        }

        // Autenticación: PLAIN (una línea) y, si no lo acepta, LOGIN.
        [$code] = smtp_cmd($fp, 'AUTH PLAIN ' . base64_encode(
            "\0" . $cfg['user'] . "\0" . $cfg['pass']
        ));
        if ($code !== 235) {
            if ($code !== 500 && $code !== 504) {
                throw new RuntimeException('autenticación rechazada (SMTP ' . $code . ')');
            }
            smtp_expect($fp, 'AUTH LOGIN', [334]);
            smtp_expect($fp, base64_encode((string) $cfg['user']), [334]);
            smtp_expect($fp, base64_encode((string) $cfg['pass']), [235]);
        }

        smtp_expect($fp, 'MAIL FROM:<' . $cfg['from'] . '>', [250]);
        smtp_expect($fp, 'RCPT TO:<' . $cfg['to'] . '>', [250, 251]);
        smtp_expect($fp, 'DATA', [354]);

        $data = str_replace(["\r\n", "\r"], "\n", $message);
        $data = (string) preg_replace('/^\./m', '..', $data);     // dot-stuffing
        fwrite($fp, str_replace("\n", "\r\n", $data) . "\r\n.\r\n");
        smtp_expect($fp, '', [250]);

        smtp_cmd($fp, 'QUIT');
    } finally {
        @fclose($fp);
    }
}

/** Anota el resultado del aviso (sin datos sensibles). */
function mail_log(string $dir, string $line): void {
    $file = $dir . '/.mail.log';
    @file_put_contents(
        $file,
        gmdate('c') . ' ' . $line . "\n",
        FILE_APPEND | LOCK_EX
    );
    @chmod($file, 0600);
}

/** Aviso best-effort: nunca lanza ni cambia la respuesta al visitante. */
function notify_by_mail(string $dir, array $m, string $file): void {
    $cfg = smtp_config($dir);
    if ($cfg === null) {
        return;                                  // sin configurar: no se avisa
    }
    $subject = '[web:' . $m['site'] . '] ' . $m['subject'];
    $message = mail_headers($cfg, $subject, $m['email'], $m['site'])
        . "\r\n\r\n"
        . mail_body($m, $file);
    try {
        smtp_send($cfg, $message);
        mail_log($dir, 'ok    ' . $file . ' → ' . $cfg['to']);
    } catch (Throwable $e) {
        mail_log($dir, 'ERROR ' . $file . ' — ' . $e->getMessage());
    }
}

/** Modo CLI: `php contact.php --test-mail` comprueba el SMTP sin tocar la web. */
function cli_main(): void {
    $dir = msgs_dir();
    $cfg = smtp_config($dir);
    if ($cfg === null) {
        fwrite(STDERR, "No hay configuración SMTP.\n"
            . "Crea " . $dir . "/.smtp.json (ver docs/contact-smtp.md).\n");
        exit(2);
    }
    $fake = [
        'site'    => 'cli-test',
        'at'      => new DateTimeImmutable('now'),
        'name'    => 'Prueba de aviso',
        'email'   => $cfg['to'],
        'subject' => 'Prueba del aviso del formulario',
        'message' => "Mensaje de prueba generado con `php contact.php --test-mail`.\n",
        'ip_hash' => 'cli',
        'ua'      => 'cli',
        'ref'     => 'cli',
    ];
    $subject = '[web:cli-test] ' . $fake['subject'];
    $message = mail_headers($cfg, $subject, $fake['email'], 'cli-test')
        . "\r\n\r\n"
        . mail_body($fake, '(prueba)');
    try {
        smtp_send($cfg, $message);
        fwrite(STDOUT, 'OK: aviso enviado a ' . $cfg['to']
            . ' vía ' . $cfg['host'] . ':' . $cfg['port']
            . ' (' . $cfg['secure'] . ")\n");
        exit(0);
    } catch (Throwable $e) {
        fwrite(STDERR, 'ERROR: ' . $e->getMessage() . "\n");
        exit(1);
    }
}

// Modo CLI (solo desde la terminal: PHP_SAPI nunca es 'cli' por HTTP).
if (PHP_SAPI === 'cli') {
    cli_main();
}

// ---------------------------------------------------------------------------
// CORS (por si un sitio publica el formulario desde otro dominio de la lista)
// ---------------------------------------------------------------------------
$origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? '');
if ($origin !== '' && origin_allowed($origin)) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    header('Vary: Origin');
}
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$dir = msgs_dir();

// ---------------------------------------------------------------------------
// GET ?token=1 → entrega un token firmado para el formulario
// ---------------------------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'GET') {
    if (isset($_GET['token'])) {
        $ts = time();
        out(200, ['ok' => true, 't' => $ts, 's' => hash_hmac('sha256', (string) $ts, secret($dir))]);
    }
    out(405, ['ok' => false, 'error' => 'method_not_allowed']);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    out(405, ['ok' => false, 'error' => 'method_not_allowed']);
}

if (!origin_allowed($origin)) {
    out(403, ['ok' => false, 'error' => 'forbidden_origin']);
}

// --- Entrada (JSON o formulario) -------------------------------------------
$ctype = (string) ($_SERVER['CONTENT_TYPE'] ?? '');
if (stripos($ctype, 'application/json') !== false) {
    $in = json_decode((string) file_get_contents('php://input'), true);
    $in = is_array($in) ? $in : [];
} else {
    $in = $_POST;
}

// --- Antibot: honeypot (debe venir vacío) ----------------------------------
if ((string) ($in['website'] ?? '') !== '') {
    out(200, ['ok' => true]);                             // éxito falso para el bot
}

// --- Antibot: token firmado con edad válida --------------------------------
$ts       = (int) ($in['t'] ?? 0);
$sig      = (string) ($in['s'] ?? '');
$expected = hash_hmac('sha256', (string) $ts, secret($dir));
$age      = time() - $ts;
if ($ts <= 0 || !hash_equals($expected, $sig) || $age < TOKEN_MIN_AGE || $age > TOKEN_MAX_AGE) {
    out(400, ['ok' => false, 'error' => 'bad_token']);
}

// --- Límite por IP ----------------------------------------------------------
$ip = (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
if (rate_limited($dir, $ip)) {
    out(429, ['ok' => false, 'error' => 'rate_limited']);
}

// --- Validación ------------------------------------------------------------
$name    = clean((string) ($in['name'] ?? ''), MAX_NAME);
$email   = clean((string) ($in['email'] ?? ''), MAX_EMAIL);
$subject = clean((string) ($in['subject'] ?? ''), MAX_SUBJECT);
$message = clean((string) ($in['message'] ?? ''), MAX_MESSAGE, true);

$errors = [];
if (u_len($name) < 2)                          { $errors[] = 'name'; }
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) { $errors[] = 'email'; }
if (u_len($subject) < 3)                       { $errors[] = 'subject'; }
if (u_len($message) < 10)                      { $errors[] = 'message'; }
if ($errors) {
    out(422, ['ok' => false, 'error' => 'invalid', 'fields' => $errors]);
}

// --- Guardar (un fichero por mensaje) --------------------------------------
$entry = [
    'site'    => site_label(),
    'at'      => new DateTimeImmutable('now', new DateTimeZone('Europe/Madrid')),
    'name'    => $name,
    'email'   => $email,
    'subject' => $subject,
    'message' => $message,
    'ip_hash' => substr(hash('sha256', $ip), 0, 12),     // no se guarda la IP
    'ua'      => clean((string) ($_SERVER['HTTP_USER_AGENT'] ?? ''), 200),
    'ref'     => clean((string) ($_SERVER['HTTP_REFERER'] ?? ''), 300),
];

$file = save_message($dir, $entry);

// Responder YA: el visitante no debe esperar a que salga el correo. Con PHP-FPM
// `fastcgi_finish_request()` cierra la respuesta y el script sigue vivo para
// mandar el aviso; sin FPM se vacía el buffer y se continúa igual.
http_response_code(200);
echo json_encode(['ok' => true, 'id' => $file], JSON_UNESCAPED_UNICODE);
if (function_exists('fastcgi_finish_request')) {
    fastcgi_finish_request();
} else {
    if (ob_get_level() > 0) {
        @ob_end_flush();
    }
    @flush();
}

notify_by_mail($dir, $entry, $file);
exit;
