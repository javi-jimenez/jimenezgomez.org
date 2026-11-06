---
title: "Un disco, tres meses: snapshots de coste cero con hardlinks"
date: 2026-11-05T18:00:00+01:00
draft: false
description: "Cómo tener un histórico mensual de un backup de un terabyte sin duplicar un solo byte. Un hardlink no es una copia: es otro nombre para el mismo fichero. La única condición es no escribir nunca en sitio, y casi todos los backups lo hacen mal."
image: "figura-hardlinks.svg"
og_image: "figura-hardlinks.svg"
categories:
  - "Notas técnicas"
tags: ["backup", "hardlinks", "rsync", "ext4", "snapshots", "linux", "sistemas"]
---

*Esto es una nota de trabajo, no un artículo. Nació intentando resolver un
problema concreto: un backup de un terabyte que quería histórico mensual y no
podía permitirse duplicarlo. El código está en
[backup-remoto-snapshot](https://github.com/javi-jimenez/backup-remoto-snapshot).*

![Un único inodo en el centro, con dos nombres apuntando a él: el fichero vivo y el snapshot congelado. La escritura atómica por rename lo deja intacto; la escritura en sitio lo destruye todo.](figura-hardlinks.svg)

---

## El problema

Tengo un terabyte que copiar. Quiero saber cómo estaba hace tres meses. Y no
quiero tres terabytes.

La respuesta obvia — «haz una copia al mes» — no funciona a esa escala. Tres
copias de un terabyte son tres discos, y el tercer mes ya no sabes qué está
donde.

La respuesta de moda — «usa btrfs o ZFS» — funciona, pero cambia el sistema de
ficheros entero, y en una máquina que ya funciona eso es un riesgo que no
siempre puedes permitirte.

Hay una tercera respuesta, más vieja, que casi nadie usa porque tiene mala fama
de frágil:

```
cp -al
```

Nueve caracteres. Copia un directorio **sin copiar los datos**.

---

## Qué es realmente un hardlink

Un fichero en un sistema Unix no es un nombre. Es un **inodo**: un bloque de
metadatos que contiene el dueño, los permisos, el tamaño, las fechas y — lo
importante — **la lista de bloques de disco donde vive el contenido**.

Lo que llamamos «nombre de fichero» es solo una entrada en un directorio que
apunta a un inodo. Y **un inodo puede tener varios nombres**. Todos igual de
reales. Ninguno es «el original».

```
inodo 24598
├── /srv/backup/current/f.txt      ← nombre 1
└── /srv/backup/202601/f.txt       ← nombre 2
```

Los dos ocupan lo mismo porque **son lo mismo**. No hay original y copia: hay dos
puertas a la misma habitación.

`cp -al` crea ese segundo nombre. Recorre el árbol, y por cada fichero en lugar
de copiar bytes llama a `link()`. Con un terabyte de datos, tarda segundos y
consume **cero bytes**.

El número que lo confirma:

```bash
$ stat -c '%i %h %n' current/f.txt 202601/f.txt
24598 2 current/f.txt
24598 2 202601/f.txt
```

Mismo inodo (`24598`), link count `2`. Dos nombres, un contenido.

---

## La condición que lo rompe todo

Aquí está la parte que casi nadie explica, y la razón por la que los snapshots
por hardlink tienen mala fama.

**Cualquier escritura en sitio sobre un fichero cambia todos sus nombres.** No
los nombres anteriores: *todos*, porque el contenido es único.

Si mañana el backup abre `current/f.txt` y escribe encima, `202601/f.txt` cambia
también. El snapshot deja de ser un histórico y pasa a ser un alias del presente.

### La diferencia que lo salva: `rename()`

`rsync -a` cuando detecta que un fichero cambió no lo abre para escribir. Hace
esto:

1. Copia el contenido nuevo a `f.txt.a1B2c3` (un fichero temporal).
2. Llama a `rename("f.txt.a1B2c3", "f.txt")`.

`rename()` es una operación **atómica** del sistema de ficheros: o se hace entera
o no se hace. Y cuando se hace, **lo que sustituye es el nombre, no el inodo**.

```
ANTES:   current/f.txt ──→ inodo 24598 ←── 202601/f.txt
DESPUÉS: current/f.txt ──→ inodo 24604
         202601/f.txt  ──→ inodo 24598   ← intacto
```

El inodo viejo pierde un nombre (`link count` baja de 2 a 1), pero **nadie lo ha
tocado**. El snapshot conserva exactamente lo que decía.

Verificado:

```bash
$ cat current/f.txt   →  V2-CAMBIADO
$ cat 202601/f.txt    →  V1            ← el histórico funciona
$ stat -c '%i %h %n' current/f.txt 202601/f.txt
24604 1 current/f.txt      ← inodo nuevo
24598 1 202601/f.txt       ← inodo viejo, intacto
```

Por eso `cp -al` no es frágil. **Es frágil si el cliente escribe mal.**

---

## Lo que corrompe, y lo que no

| Escritura | Qué hace | Snapshots |
|:---|:---|:---|
| `rsync -a` | `.tmp` + `rename()` | ✅ intactos |
| `rsync --inplace` | escribe sobre el inodo | ❌ **rompe todos** |
| `rclone --inplace` | escribe sobre el inodo | ❌ **rompe todos** |
| `rclone sync` (mismo tamaño) | reescribe en sitio | ❌ **rompe todos** |
| `cp` sin `-a` | trunca y escribe | ❌ **rompe todos** |
| `-L` / `--copy-links` | convierte enlace en copia | ⚠️ rompe la deduplicación |

La última fila de `rclone` es la que me costó un rato entender. `rclone sync`
normalmente crea un objeto nuevo y lo renombra, así que en teoría es seguro.
Pero **cuando el tamaño del fichero coincide, reescribe en sitio** aunque no
pases `--inplace`. Y eso basta para llevarse el histórico.

Conclusión práctica: **rclone no sirve para este esquema.** Hay que usar `rsync`.

---

## Un intento fallido que enseñó algo

Al principio puse el script del servidor a hacer `chown -R root` y
`chmod -R a-w` sobre el snapshot recién creado. El razonamiento parecía sensato:
«si es de root y no tiene escritura, un `--inplace` falla en vez de corromper».

No funciona. Y el motivo es el mismo de todo el artículo: **el inodo es
compartido**.

```
chown root 202601/f.txt   →  cambia el dueño del inodo
                          →  y current/f.txt es el mismo inodo
                          →  ahora el cliente no puede escribir en su propio destino
```

Se rompe el destino para «proteger» la copia. Un inodo no puede ser de root en
el snapshot y de otro usuario en `current/`: es el mismo objeto.

La lección: **en un esquema de hardlinks no puedes tener permisos distintos para
la copia y el original**, porque no son dos cosas. La protección tiene que venir
de la forma de escribir, no de los permisos.

---

## El sistema completo

Dos scripts y dos líneas de cron.

### Servidor

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE="${BACKUP_BASE:-/srv/backup}"
MES="$(date +%Y%m)"

[[ -e "$BASE/$MES" ]] && { echo "$BASE/$MES ya existe."; exit 0; }
[[ -d "$BASE/current" ]] || { echo "No existe current/." >&2; exit 1; }
[[ "$(stat -c %d "$BASE")" == "$(stat -c %d "$BASE/current")" ]] \
  || { echo "Filesystems distintos." >&2; exit 1; }

cp -al "$BASE/current" "$BASE/$MES"
echo "Creado $BASE/$MES ($(find "$BASE/$MES" -type f | wc -l) ficheros, 0 bytes)"
```

Nada más. Ni `chown`, ni `chmod`, ni borrado de snapshots viejos.

### Cliente

`rsync -a --delete` con exclusiones, cerrojo con `flock` y log. Sin
`--inplace`, sin `-L`.

### Cron

**Servidor:** diario, no el día 1.

```cron
30 3 * * * /usr/local/bin/snapshot-mensual.sh >> /var/log/snapshot-mensual.log 2>&1
```

El script sale en cuanto ve que el snapshot del mes ya existe, así que solo
trabaja una vez al mes. Si el servidor estaba apagado el día 1, se crea el primer
día que arranque.

**Cliente:** `anacron`, no `cron`.

```
1  10  backup-cliente  /home/usuario/.local/bin/backup-cliente.sh
```

Un `cron` normal solo dispara si el aparato está encendido a esa hora. En un
portátil, el backup de las 02:00 **nunca** se hace: a las 02:00 el portátil está
cerrado. `anacron` anota cuándo tocaba y lo ejecuta al arrancar si se pasó la
hora.

Enciendes el ordenador por la mañana y el backup que no se hizo anoche se hace
solo mientras te preparas el café.

Comprobado: el segundo mes cuesta **0 bytes**.

---

## Lo que esto no hace

- **No rellena meses perdidos.** Si estuvo apagado de enero a abril, en abril se
  crea solo `202604`. El nombre de un snapshot es la fecha en que se tomó, no la
  fecha que debería haber tenido. Un snapshot que falta dice algo; uno falso, no.
- **No borra snapshots viejos.** Eso lo decides tú, no un script con `find -mtime`.
- **No cifra.** Eso es del transporte (SSH) o del volumen.
- **No sustituye un 3-2-1.** Esto es *una* copia. Un backup en el mismo edificio
  no es un backup.
- **No funciona en QNAP, FAT/exFAT ni montajes de red** sin soporte de hardlinks.
  `cp -al` falla y el script sale con error, que es lo correcto.

---

## Por qué esto sigue importando

Vivimos en una época donde la respuesta a todo es «usa ZFS» o «usa btrfs». Y no
están mal: son mejores. Tienen snapshots nativos, checksums, send/receive
incremental y no dependen de que el cliente se porte bien.

Pero exigen cambiar el sistema de ficheros de una máquina que funciona. Y en un
servidor modesto, en un disco externo, o en una máquina que no puedes reinstalar,
eso a veces no es una opción.

`cp -al` no necesita nada. Funciona en ext4, que es lo que tiene todo el mundo.
Ocupa cero bytes. Y si respetas una sola regla — **nunca escribir en sitio** —
conserva el histórico exactamente igual que ZFS.

La regla no es un detalle: es todo el sistema. Un backup que escribe en sitio no
es un backup incremental, es una copia que se cree a sí misma.
