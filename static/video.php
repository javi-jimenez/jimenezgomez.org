<?php
/* =============================================================================
   Contador de reproducciones — endpoint de vídeo
   -----------------------------------------------------------------------------
   Sirve el MP4 y cuenta cada reproducción en un fichero de texto plano, para
   contabilidad interna. NO hay panel público, NO hay número visible en ninguna
   página, y NO se envía nada a terceros. Es un contador casero, con la misma
   idea que los contadores CGI de los noventa: un fichero al lado y una línea
   por evento.

   Almacén, fuera del docroot y fuera de las carpetas que sincroniza el deploy
   (igual que `msgs/` en contact.php, y por la misma razón: `FTP_DELETE=1` no
   debe poder borrar la contabilidad):

       <home>/stats/                    →  /home/brisecw/stats/
           plays.log                    ← una línea por reproducción
           .secret.key                  ← HMAC del token de sesión
           .ratelimit.json              ← cupo por IP

   Cómo se cuenta, y por qué así
   -----------------------------
   Se cuenta una REPRODUCCIÓN cuando el reproductor pide el fichero con
   `?play=1` (lo pide el JS del player, no el <video> directamente). Así:

     - Pedir el MP4 a pelo (descarga directa, scrapers, previsualización de
       WhatsApp, `curl`) NO cuenta: no pasa por aquí con `play=1`.
     - Las peticiones de rango (Range: bytes=…) que hace el navegador para
       hacer seek NO cuentan: solo cuenta la primera, la que crea la sesión.
     - Una misma sesión (cookie `bsc_play`, 30 min) cuenta UNA vez. Recargar
       la página no infla el número.

   Es decir: cuenta personas que le dan al play, no bytes servidos. Es la
   métrica que sirve para contabilidad; la de YouTube será otra y no tienen por
   qué coincidir.

   Protecciones: token firmado (HMAC) con caducidad, límite por IP, y lista de
   ficheros servibles cerrada (no es un proxy de ficheros arbitrarios).
   ========================================================================== */

error_reporting(E_ALL);
ini_set('display_errors', '0');
ini_set('log_errors', '1');

// --- Configuración ----------------------------------------------------------
const STATS_DIRNAME  = 'stats';    // compartido, hermano de los docroots
const SECRET_FILE    = '.secret.key';
const LOG_FILE       = 'plays.log';
const RATE_FILE      = '.ratelimit.json';
const COOKIE_NAME    = 'bsc_play';
const COOKIE_TTL     = 1800;       // 30 min: una sesión = una reproducción
const TOKEN_MAX_AGE  = 900;        // 15 min de validez del token de arranque
const RATE_MAX       = 30;         // reproducciones contadas por IP...
const RATE_WINDOW    = 3600;       // ...por hora (margen generoso: no es un form)

// Ficheros servibles. Lista cerrada: el nombre NUNCA viene del cliente.
const MEDIA = [
    'year-one'      => 'brisecom-year-one-1080p.mp4',
    'meteoectasis'  => 'meteoectasis-1080p.mp4',
];

/** JSON y fin. */
function out_json(int $code, array $payload): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Cache-Control: no-store');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

/** Directorio de contabilidad (fuera del docroot). */
function stats_dir(): string {
    $env = getenv('VIDEO_STATS_DIR');                 // override (pruebas locales)
    $dir = $env !== false && $env !== '' ? $env : dirname(__DIR__) . '/' . STATS_DIRNAME;

    if (!is_dir($dir) && !@mkdir($dir, 0755, true)) {
        out_json(500, ['ok' => false, 'error' => 'storage_unavailable']);
        exit;
    }
    if (!is_writable($dir)) {
        out_json(500, ['ok' => false, 'error' => 'storage_unavailable']);
        exit;
    }
    return rtrim($dir, '/');
}

/** Secreto HMAC; se genera solo la primera vez. */
function secret(string $dir): string {
    $file = $dir . '/' . SECRET_FILE;
    if (!is_file($file)) {
        @file_put_contents($file, bin2hex(random_bytes(32)), LOCK_EX);
        @chmod($file, 0600);
    }
    return trim((string) @file_get_contents($file));
}

/** Token de arranque: "<expira>.<hmac>". Caduca, así que no se puede reusar. */
function make_token(string $secret): string {
    $exp = time() + TOKEN_MAX_AGE;
    return $exp . '.' . hash_hmac('sha256', (string) $exp, $secret);
}

function check_token(string $secret, string $token): bool {
    $parts = explode('.', $token, 2);
    if (count($parts) !== 2) {
        return false;
    }
    [$exp, $mac] = $parts;
    if (!ctype_digit($exp) || (int) $exp < time()) {
        return false;
    }
    return hash_equals(hash_hmac('sha256', $exp, $secret), $mac);
}

/** Hash de la IP: se guarda el hash, no la IP. Basta para contar y para el
    límite, y no convierte este fichero en un registro de datos personales. */
function ip_hash(): string {
    $ip = $_SERVER['REMOTE_ADDR'] ?? '';
    return substr(hash('sha256', $ip . '|bsc-video'), 0, 16);
}

/** Límite por IP con ventana deslizante simple. */
function rate_ok(string $dir): bool {
    $file = $dir . '/' . RATE_FILE;
    $now  = time();
    $data = [];
    if (is_file($file)) {
        $raw = @file_get_contents($file);
        $decoded = json_decode((string) $raw, true);
        if (is_array($decoded)) {
            $data = $decoded;
        }
    }
    $key  = ip_hash();
    $hits = array_values(array_filter(
        $data[$key] ?? [],
        static fn($t) => is_int($t) && $t > $now - RATE_WINDOW
    ));
    if (count($hits) >= RATE_MAX) {
        $data[$key] = $hits;
        @file_put_contents($file, json_encode($data), LOCK_EX);
        @chmod($file, 0600);
        return false;
    }
    $hits[] = $now;
    $data[$key] = $hits;
    // Poda: fuera las IP que ya no tienen actividad en la ventana.
    foreach ($data as $k => $v) {
        $kept = array_values(array_filter($v, static fn($t) => is_int($t) && $t > $now - RATE_WINDOW));
        if ($kept === []) {
            unset($data[$k]);
        } else {
            $data[$k] = $kept;
        }
    }
    @file_put_contents($file, json_encode($data), LOCK_EX);
    @chmod($file, 0600);
    return true;
}

/** Anota una reproducción. Una línea por evento, tabulada, legible a ojo. */
function log_play(string $dir): void {
    $line = implode("\t", [
        gmdate('Y-m-d\TH:i:s\Z'),
        ip_hash(),
        // Se limpia para que una cabecera con saltos de línea no pueda inyectar
        // líneas falsas en el log, pero SE CONSERVAN los caracteres de una URL
        // (':', '.', '?', '=', '&'): sin ellos el referer sale inservible
        // («http//127.0.0.14195/»), y el referer es la mitad del valor.
        (string) substr(preg_replace('/[^A-Za-z0-9 _.:;?=&%+\/()\[\]-]/', '', $_SERVER['HTTP_REFERER'] ?? '-'), 0, 160),
        (string) substr(preg_replace('/[^A-Za-z0-9 .;:()\/\-]/', '', $_SERVER['HTTP_USER_AGENT'] ?? '-'), 0, 100),
    ]) . "\n";

    $fh = @fopen($dir . '/' . LOG_FILE, 'ab');
    if ($fh === false) {
        return;
    }
    if (flock($fh, LOCK_EX)) {
        fwrite($fh, $line);
        fflush($fh);
        flock($fh, LOCK_UN);
    }
    fclose($fh);
}

// ---------------------------------------------------------------------------
// Enrutado
// ---------------------------------------------------------------------------

$dir    = stats_dir();
$secret = secret($dir);
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$action = $_GET['a'] ?? '';

// 1) El player pide un token para arrancar. Evita que un bot cuente solo con
//    pedir el MP4, y permite caducar la capacidad de contar.
if ($action === 'token') {
    out_json(200, ['ok' => true, 'token' => make_token($secret)]);
}

// 2) Total (solo para consulta interna desde línea de comandos / FTP).
//    Nunca se enlaza desde el sitio y no hay ningún panel público.
if ($action === 'total') {
    $file = $dir . '/' . LOG_FILE;
    $n = is_file($file) ? count(file($file, FILE_SKIP_EMPTY_LINES)) : 0;
    out_json(200, ['ok' => true, 'plays' => $n]);
}

// 3) Servir el vídeo. `play=1` + token válido = cuenta y sirve.
$f   = $_GET['f'] ?? '';
$vid = MEDIA[$f] ?? null;
if ($vid === null) {
    http_response_code(404);
    exit;
}

$path = __DIR__ . '/video/' . $vid;
if (!is_file($path)) {
    http_response_code(404);
    exit;
}

$counted = false;
if ($method === 'GET' && ($_GET['play'] ?? '') === '1') {
    $token = (string) ($_GET['t'] ?? '');
    $already = isset($_COOKIE[COOKIE_NAME]);
    if (!$already && check_token($secret, $token) && rate_ok($dir)) {
        log_play($dir);
        $counted = true;
    }
    if (!$already) {
        setcookie(COOKIE_NAME, '1', [
            'expires'  => time() + COOKIE_TTL,
            'path'     => '/',
            'httponly' => true,
            'samesite' => 'Lax',
            'secure'   => !empty($_SERVER['HTTPS']),
        ]);
    }
}

// --- Servicio del fichero con soporte de Range (sin él, el seek no funciona
//     en Safari ni en móviles) -------------------------------------------------
$size  = filesize($path);
$start = 0;
$end   = $size - 1;
$code  = 200;

if (isset($_SERVER['HTTP_RANGE']) && preg_match('/bytes=(\d*)-(\d*)/', $_SERVER['HTTP_RANGE'], $m)) {
    $rangeOk = true;
    if ($m[1] === '' && $m[2] === '') {
        $rangeOk = false;
    } else {
        if ($m[1] !== '') {
            $start = (int) $m[1];
        }
        if ($m[2] !== '') {
            $end = (int) $m[2];
        }
        if ($start > $end || $start >= $size) {
            $rangeOk = false;
        }
    }
    if ($rangeOk) {
        $code = 206;
        $end  = min($end, $size - 1);
        header(sprintf('Content-Range: bytes %d-%d/%d', $start, $end, $size));
    } else {
        header('Content-Range: bytes */' . $size);
        http_response_code(416);
        exit;
    }
}

$length = $end - $start + 1;

header('Content-Type: video/mp4');
header('Accept-Ranges: bytes');
header('Content-Length: ' . $length);
// El vídeo puede cachearse, pero la decisión de contar no: el token caduca.
header('Cache-Control: public, max-age=86400');
header('X-Content-Type-Options: nosniff');
if ($counted) {
    header('X-Play-Counted: 1');   // visible en devtools; el número, no.
}

http_response_code($code);

$fh = fopen($path, 'rb');
if ($fh === false) {
    http_response_code(500);
    exit;
}
fseek($fh, $start);
$left = $length;
while ($left > 0 && !feof($fh)) {
    $chunk = fread($fh, min(262144, $left));
    if ($chunk === false || $chunk === '') {
        break;
    }
    echo $chunk;
    $left -= strlen($chunk);
    flush();
}
fclose($fh);
exit;
