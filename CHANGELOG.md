# Changelog

Una entrada por tag. Cada entrada dice **qué** cambió y **por qué**; el porqué es
lo primero que se pierde y lo más caro de reconstruir.

## [1.2.4] — 2026-10-21

### Añadido

- **La fecha de publicación se ve en el cuerpo de todos los artículos.** Aparece
  en la cabecera, bajo el título, junto al tiempo de lectura.

### Corregido

- **La fecha llevaba tiempo oculta.** El `details.html` local tenía
  `{{ $showDate := false }}` con la condición de que el post declarara
  `showDate: true`; ningún artículo lo declaraba, así que no se mostraba en
  ninguno. Se restaura el criterio del tema (`not .Date.IsZero`) y se invierte el
  override: ahora se oculta solo con `showDate: false` explícito.
- **Dos versiones de Hugo generaban el mismo sitio.** `make build` usaba `hugo`
  del PATH (0.113) mientras los builds manuales usaban 0.162: cada deploy
  reescribía todos los hashes de assets y el sitio alternaba entre dos renders
  sin que nadie tocara el contenido. Ahora el Makefile fija `HUGO_VERSION` y
  resuelve el binario en orden (`hugo-extended` → `hugo-<versión>` → `hugo` →
  Docker), y **dice qué versión usa** en cada build.
- **`build` limpia el destino** (`--cleanDestinationDir`). Sin eso, los assets
  con hash de la versión anterior se acumulaban en `public/` y viajaban al
  servidor en cada deploy.

### Decidido

- **Fijar la versión de Hugo, no confiar en el PATH.** El orden de resolución
  prefiere `hugo-extended` porque el tema Stack requiere la versión *extended*
  (SCSS); caer en un `hugo` normal rompe el CSS.
- **La fecha es información del artículo, no un extra opcional.** Un artículo sin
  fecha obliga al lector a deducir la antigüedad por el contexto; si alguna vez
  hay que ocultarla, se hace explícitamente con `showDate: false` y queda
  registrado en el frontmatter.

## [1.2.3] — 2026-10-21

### Corregido

- **`/posts/2024-03-31-vbd/` daba 404.** La carpeta existe en `content/posts/`,
  pero es una **plantilla vacía** (frontmatter y nada más) marcada `draft: true`,
  así que Hugo no la genera. Como la URL es antigua y puede estar enlazada desde
  fuera, ahora el artículo publicado equivalente declara
  `aliases: ["/posts/2024-03-31-vbd/"]` y esa dirección responde con una
  redirección a *VBD, Fractal Architecture*.
- **Limpieza de 126 artefactos obsoletos en `public/`**: variantes de imagen con
  hash antiguo (portadas azules anteriores y redimensionados de versiones viejas
  de Hugo). Se comprobó que **ninguna página las referencia** antes de borrarlas.

### Decidido

- **El draft se queda como draft.** No tiene contenido: es una plantilla. Lo que
  se arregla es la *URL*, no el artículo. Publicarlo habría creado una página
  vacía e indexable, que es peor que un 404.
- **Redirección y no página vacía.** Un alias es honesto (dice a dónde va) y
  conserva el valor de cualquier enlace entrante.
- **`--cleanDestinationDir` en los builds manuales.** `make build` no limpia, así
  que los artefactos con hash viejo se acumulaban en `public/` y viajaban al
  servidor en cada deploy. Limpiar en cada build evita que el repositorio crezca
  con ficheros que ya nadie sirve.

## [1.2.2] — 2026-10-21

### Cambiado

- **Gitea pasa a SSH** (antes HTTPS con token). El SSH del servidor entra por el
  **puerto 22 a través del router TCP de Traefik**, que reenvía al OpenSSH del
  host; ese OpenSSH delega en Gitea. Resultado: `git push` no pide nada, porque
  la clave `hek-push` ya está registrada y el agente la tiene cargada.
- **URL canónica del remoto**, la que publica la API de Gitea:
  `git@gitea.app.brisecom.net:gitea/jimenezgomez.org.git` (sin `:22`).

### Corregido

- **Documentación de credenciales desfasada**: el README describía un almacén de
  credenciales HTTP que ya no se usa.

### Decidido

- **Un secreto menos en disco.** Se elimina `~/.config/gitea/credentials` y el
  `helper` de git para ese host. El token de API se queda en
  `~/.config/gitea/token` porque sigue haciendo falta para la API REST (crear
  repos, consultar metadatos), pero ya no es una credencial de git.
- **El workaround de packs se mantiene** (`GIT_SLOW_REMOTES = gitea`): el
  problema es el almacén en s3fs, no el transporte. Cambiar HTTPS por SSH no lo
  arregla.

## [1.2.1] — 2026-10-21

### Añadido

- **`GIT_SLOW_REMOTES`**: los remotos cuyo almacén no soporta packs grandes
  empujan con `-c pack.threads=1 --no-thin` automáticamente. Se acabó el
  workaround manual en cada push a Gitea.
- **Token de API de Gitea** guardado en un almacén dedicado
  (`~/.config/gitea/credentials`, 0600) en sustitución de la contraseña de la
  cuenta que había en el llavero. Revocable sin tocar la contraseña.

### Corregido

- **`make push-all` fallaba en Gitea**: `-c` es una opción global de git y
  `--no-thin` es una opción de push, así que no pueden ir en la misma variable
  (`git push -c ...` imprime la ayuda). Ahora se pasan como dos grupos y se
  expanden sin comillas para que se dividan en palabras.

### Decidido

- **Almacén de credenciales propio para Gitea, no GCM.** GCM puede *leer* del
  llavero en esta máquina pero no *escribir* (`Failed to open secret service
  session`), así que el token no se podía guardar ahí. Un `store --file`
  dedicado, precedido de un `helper =` vacío para anular los heredados, es
  explícito, aislado por host y verificable.
- **Token en lugar de contraseña.** Un token se revoca sin cambiar la clave de
  la cuenta y sin afectar a otros servicios del mismo usuario.
- **El matcher compara nombre y URL del remoto.** Así `GIT_SLOW_REMOTES=gitea`
  vale tanto si el remoto se llama `gitea` como si apunta a
  `gitea.dominio.tld`, que es como se configuran los espejos en la práctica.

## [1.2.0] — 2026-10-21

### Añadido

- **Portadas propias para los 39 artículos** (`tools/coverart/`). Antes todos
  compartían la misma plantilla: degradado azul y el título encima. Ahora cada
  uno tiene un **motivo** dibujado para su tema —redes, capas, fractales,
  órbitas, sellos, estratos, muros, fichas, símbolos formales— y una **paleta**
  distinta, incluidas portadas claras de aire editorial.
- `python3 -m coverart --all|<slug>` y `--list` para generar y auditar el reparto.
- Motivo `plinth` para el artículo de ética: placa decorativa que flota frente a
  cimiento que sostiene. Es la tesis del texto, dibujada.

### Cambiado

- **`og:image` y `twitter:image` apuntan al PNG**, no al SVG. Las redes sociales
  no renderizan SVG: hasta ahora cada enlace compartido salía sin imagen. El
  frontmatter de los 39 artículos se ha actualizado.
- **El hook `pre-commit` sólo regenera la portada de los artículos del commit.**
  Antes rehacía las 39 en cada commit (lento) y, al usar la plantilla genérica,
  **sobrescribía cualquier portada hecha a mano** — le pasó la primera vez a la
  del artículo de ética.
- `tools/generate-og-image.py` pasa a delegar en `coverart`; se mantiene como
  punto de entrada porque lo llama el hook, y avisa cuando un artículo no tiene
  portada propia.

### Corregido

- **Frontmatter corrupto en `2026-01-28-la-fe`**: los delimitadores `---` estaban
  duplicados y las claves `image`/`og_image` quedaban parte dentro y parte fuera
  del bloque, como texto del cuerpo. Venía de una inserción anterior.

### Decidido

- **Ninguna pareja (motivo, paleta) se repite.** Con 39 artículos y una librería
  de motivos menor que ese número, la variedad se consigue combinando: quien
  comparte tema comparte dibujo y cambia de color y de parámetros. Así se
  reconoce la familia sin confundir las piezas.
- **Los PNG se cuantizan a 256 colores.** El grano de la portada es ruido, y el
  ruido no comprime: 300 KB por portada. Con `PNG8` baja a ~120 KB y no se nota,
  porque el propio grano hace de tramado. El repositorio pesa 6,5 MB menos.
- **El color se decide por artículo, no por plantilla.** Una lista de 39
  portadas idénticas no distingue nada; en cuanto cambia el color, se reconoce
  cuál es cuál antes de leer el título.

## [1.1.0] — 2026-10-21

Primera versión con versionado explícito desde `v1.0.0` (2026-09-07). Recoge los
10 commits acumulados desde entonces más el trabajo de esta sesión.

### Añadido

- **Artículo «Working as Equals: Ethics as Infrastructure, Not Decoration»**
  (`content/posts/2026-10-21-working-as-equals-ethics-as-infrastructure/`): la
  reflexión sobre trabajo de igual a igual y ética como infraestructura, con la
  sección legal sobre el **EU AI Act** (Reglamento (UE) 2024/1689), bibliografía
  comentada de 16 fuentes y figura ilustrativa propia.
- **Whitepaper #13 de LAIA** — *Ethics as Infrastructure: Build Conditions and the
  Layer the EU AI Act Does Not Regulate*, publicado en `javi-jimenez/laia` y
  enlazado desde el artículo en dos puntos (sección V y bibliografía). El artículo
  es la entrada legible; el whitepaper es la versión citable.
- **`VERSION`, `CHANGELOG.md` y `README.md`** en la raíz — política de versión
  visible: un tag es invisible desde dentro del proyecto.
- **Versionado y publicación en el Makefile** (`version`, `version-bump`,
  `changelog-new`, `readme-check`, `tag`, `push-tags`, `release`, `push-all`,
  `git-status`, `git-commit`, `push`, `pull`), tomados de `makeit` 0.3.0.
- **Réplica a dos remotos**: `GIT_REMOTES = origin gitea`. `push-all` y
  `push-tags` empujan a GitHub y Gitea e informan de **cuál** falla.
- Página de contacto neutra con formulario y endpoint PHP (`static/contact.php`)
  que guarda un `.md` por mensaje en un almacén compartido fuera de los docroots.
- Artículo «The Neptuno Network» y «Desktop Launcher Creator».

### Cambiado

- **El deploy por FTP pasó a una sola invocación de shell.** Cada línea `@` de un
  Makefile es un shell distinto, así que cargar el `.env` en una línea no servía
  para las siguientes: el deploy **solo funcionaba si las variables ya venían
  exportadas** del entorno, que es exactamente el camino por el que se produjo el
  incidente del 2026-10-16 (subida del sitio encima de `/laia.brisecom.org`).
- **`override FTP_REMOTE_PATH := /jimenezgomez.org/`** — el destino es intrínseco
  a este repo y no debe poder heredarse del shell.
- **CI**: se sustituyen GitHub Actions por Gitea Actions + imagen Docker portable;
  el pipeline llama a los targets de `make`, y el Makefile queda como única fuente
  de verdad.

### Corregido

- Dirección de contacto a `info@brisecom.org`.
- Experiencia declarada: «más de 30 años» (antes 15).

### Decidido

- **El Makefile sigue autocontenido, no `include` de makeit.** `makeit` es la
  referencia (de allí sale toda la lógica de etiquetado y changelog), pero este
  Makefile debe funcionar en Drone y GitHub Actions, donde
  `~/data/repo/makeit` no existe. Un `include` de una ruta del HOME haría que la
  ruta de producción (`make build` / `make deploy`) dependiera de un directorio
  que solo está en esta máquina.
- **`1.1.0` y no `2.0.0`**: hay funcionalidad nueva (formulario, versionado,
  réplica de remotos) y correcciones de despliegue, pero ninguna ruptura de la
  estructura de URLs del sitio.
- **El artículo se enlaza al whitepaper, no se duplica**: el blog es la puerta de
  entrada; el documento formal es el que se cita y se revisa.

### Pendiente

- **`public/` sin regenerar**: el contenido nuevo está en `content/`, pero la
  salida publicada (`public/`, versionada porque el deploy es su espejo por FTP)
  todavía no se ha reconstruido con estos artículos. Se hará junto con la
  revisión de portadas de los artículos que aún usan la imagen genérica azul.
- **Push a Gitea**: el 2026-10-21 el host de Gitea (`helike`,
  `100.70.218.123`) no respondía en ningún puerto (443/3000/22), así que el tag y
  el commit están en GitHub y pendientes de réplica. `make push-all` y
  `make push-tags` los subirán a ambos remotos en cuanto vuelva.
- Artículos antiguos con portada genérica azul: sustituir por imágenes propias.

## [1.0.0] — 2026-09-07

(Anterior al establecimiento de este CHANGELOG: la entrada no existe de forma
retroactiva. El tag `v1.0.0` corresponde a «ci: make Makefile the single source of
truth; Drone pipeline calls make targets».)
