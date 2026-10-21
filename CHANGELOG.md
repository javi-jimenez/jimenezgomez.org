# Changelog

Una entrada por tag. Cada entrada dice **qué** cambió y **por qué**; el porqué es
lo primero que se pierde y lo más caro de reconstruir.

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
