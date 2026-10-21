# Aviso por correo del formulario de contacto

El formulario **guarda siempre** el mensaje como `.md` en `/msgs/` del hosting.
Este documento explica el **aviso opcional por correo**, que es solo un extra
para enterarse antes. Si el correo falla, el formulario sigue respondiendo `ok`
y el mensaje ya está en disco: **nunca se pierde un mensaje por un fallo de SMTP**.

## Por qué SMTP autenticado y no `mail()`

| | `mail()` | SMTP autenticado (`smtp.mail.ovh.net:587`) |
|---|---|---|
| IP de salida | la del hosting web (`87.98.230.241`) | la de los servidores de correo de OVH |
| SPF del dominio | **no la cubre** → fallo duro (`-all` en brisecom.org) | **sí** (`include:mx.ovh.com`) |
| Resultado | spam o rechazo | entrega normal |

Por eso el aviso se manda por SMTP autenticado. `mail()` no se usa.

## Configuración: `/msgs/.smtp.json`

El fichero vive **fuera del docroot** (404 por URL) y **fuera de la carpeta del
sitio**, así que el `mirror --delete` del deploy **no lo borra**. Es el mismo
sitio donde ya viven `.secret.key` y `.ratelimit.json`.

```json
{
  "host": "smtp.mail.ovh.net",
  "port": 587,
  "secure": "tls",
  "user": "no-reply@jimenezgomez.org",
  "pass": "LA-CONTRASEÑA-DEL-BUZON",
  "from": "no-reply@jimenezgomez.org",
  "from_name": "Formulario jimenezgomez.org",
  "to": "ximenez.francisco@gmail.com"
}
```

| Campo | Obligatorio | Notas |
|---|---|---|
| `host` | sí | `smtp.mail.ovh.net` |
| `port` | no (587) | 587 con STARTTLS, 465 con SSL |
| `secure` | no (`tls`) | `tls` · `ssl` · `none` (solo pruebas) |
| `user` | sí | buzón **completo**, con `@dominio` |
| `pass` | sí | contraseña del buzón |
| `from` | sí | debe ser el buzón autenticado (si no, OVH lo rechaza) |
| `to` | sí | dónde llega el aviso (puede ser otra cuenta, p. ej. Gmail) |
| `from_name` | no | nombre visible del remitente |
| `timeout` | no (10) | segundos |

Crear con permisos restringidos:

```bash
# por FTP/SFTP al hosting
chmod 600 /home/brisecw/msgs/.smtp.json
```

## Comprobar que funciona

El propio fichero tiene un modo de prueba que **no toca la web**:

```bash
php contact.php --test-mail
```

- `OK: aviso enviado a … vía smtp.mail.ovh.net:587 (tls)` → correcto.
- `ERROR: autenticación rechazada (SMTP 535)` → usuario o contraseña mal.
- `ERROR: conexión: Connection refused` → host/puerto mal o firewall.

## Qué se envía

Asunto: `[web:<sitio>] <asunto del mensaje>`

```
Nuevo mensaje desde el formulario web
======================================
Sitio:     jimenezgomez-org
Fecha:     2026-10-22 00:30:40
Nombre:    …
Email:     …
Asunto:    …
Fichero:   jimenezgomez-org-20261022-003040-3c3e22.md
IP hash:   12ca17b49af2
Navegador: …
Referer:   …

--------------------------------------

<cuerpo del mensaje>
```

`Reply-To` es el email del visitante: responder al aviso contesta directamente a
quien escribió.

## Registro: `/msgs/.mail.log`

Una línea por intento, **sin datos sensibles**:

```
2026-10-21T22:30:40+00:00 ok    127-0-0-1-20261022-003040-3c3e22.md → x@y.z
2026-10-21T22:30:57+00:00 ERROR 127-0-0-1-20261022-003057-cc34dc.md — conexión: Connection refused
```

Un `ERROR` en el log **no significa mensaje perdido**: el `.md` de esa misma
línea está en `/msgs/` y el colector de Semaphore lo recogerá igual.

## Orden de operaciones (y por qué importa)

1. Validar → 2. guardar el `.md` → 3. **responder al visitante** → 4. enviar el aviso.

Entre el 3 y el 4 se llama a `fastcgi_finish_request()` si existe (PHP-FPM), de
modo que el visitante recibe la respuesta **sin esperar** a que OVH acepte el
correo. El envío es *best-effort*: va envuelto en `try/catch` y una excepción
solo escribe en `.mail.log`.

## Si OVH bloquea el envío

OVH puede pausar el envío de scripts por seguridad (panel **«Scripts de correo»**,
se desbloquea desde el panel). Cuando eso pasa:

- el aviso deja de llegar,
- el formulario **sigue funcionando**,
- los mensajes **siguen guardándose** en `/msgs/`,
- el colector de Semaphore **los sigue trayendo**.

Es exactamente el motivo de que el correo no sea el canal principal.

## Captcha

No hace falta, y por eso no se usa. El endpoint ya lleva honeypot + token HMAC
con caducidad (mín. 2 s, máx. 2 h) + límite de 8 envíos por IP y hora +
comprobación de `Origin`. Un captcha añadiría una dependencia externa (Google) y
un iframe por muy poco más.
