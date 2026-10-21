# jimenezgomez.org

**Versión: 1.2.1** · [CHANGELOG](CHANGELOG.md)

Sitio personal de Francisco Javier Jiménez Gómez: `index.html` en la raíz es la
landing de portfolio (en español, independiente de Hugo) y el blog se genera con
**Hugo** + tema **Stack** bajo `/posts`.

## Estructura

| Ruta | Qué hay |
|---|---|
| `index.html` | Landing de portfolio. Fichero suelto, **no** lo genera Hugo |
| `content/posts/YYYY-MM-DD-slug/index.md` | Artículos: cada uno en su carpeta con sus imágenes |
| `layouts/`, `assets/` | Sobrescrituras del tema (`themes/stack` no se toca) |
| `static/` | Ficheros servidos tal cual (`contact.php`, `img/`, `og/`) |
| `public/` | Salida de Hugo. **Se versiona**: el deploy es su espejo por FTP |
| `tools/`, `scripts/` | Generación de imágenes OG, hooks, mantenimiento de posts |

## Construir y publicar

```bash
make build     # genera public/ con Hugo
make deploy    # build + subida por FTP a /jimenezgomez.org/
make serve     # preview en http://localhost:1313
make help      # lista completa de targets
```

El `.env` (no versionado) lleva `FTP_SERVER` / `FTP_USERNAME` / `FTP_PASSWORD`.
El Makefile funciona igual en local, en Drone y en GitHub Actions: usa la
herramienta si está en el entorno y, si no, la lanza en contenedor oficial.

## Versionado

```bash
make version                 # versión actual (VERSION)
make version-bump BUMP=minor # sube minor/major/patch
make changelog-new           # prepara la entrada en CHANGELOG.md
make readme-check            # verifica que README y CHANGELOG citan la versión
make tag                     # tag <versión>-YYYYMMDDHHMM
make release                 # tag + push de tags a todos los remotos
```

La lógica de esta sección viene de [**makeit**](file:///home/user/data/repo/makeit)
(0.3.0), que es la referencia. Aquí está copiada de forma autocontenida a
propósito: este Makefile tiene que correr en CI, donde el repo de makeit no está.

## Remotos

El repo se replica en dos forjas:

| Remoto | URL |
|---|---|
| `origin` | `github.com/javi-jimenez/jimenezgomez.org` |
| `gitea` | `gitea.app.brisecom.net/gitea/jimenezgomez.org` (privado) |

```bash
make push-all     # commit + push a ambos, informando de cuál falla
make push-tags    # sube los tags a ambos
```

### Credenciales

`origin` (GitHub) va por **SSH**: la clave `~/.ssh/id_rsa-github` está cargada en
el agente de la sesión, así que no pide passphrase. Si algún día la pide en
consola, es que falta `SSH_AUTH_SOCK` en el shell (ver el bloque de
`~/.bashrc`) o que hay que añadir la clave con `ssh-add`.

`gitea` va por **HTTPS con token**, en un almacén dedicado y separado del
llavero de GCM (GCM puede leerlo pero no escribirlo en esta máquina):

| Elemento | Ruta |
|---|---|
| Token de API | `~/.config/gitea/token` (0600) |
| Almacén de git | `~/.config/gitea/credentials` (0600) |
| Config | `[credential "https://gitea.app.brisecom.net"]` en `~/.gitconfig` |

```bash
git config --global --get-regexp '^credential\.https://gitea'
```

El bloque vacío `helper =` es deliberado: borra los helpers heredados
(llavero/GCM) para ese host y deja solo el fichero. Sin él, GCM devolvería
primero la credencial antigua. Para revocar el acceso: borrar el token en
Gitea → *Settings → Applications* y regenerar.

### Remotos lentos

El repositorio de Gitea vive en un sistema de ficheros sin locking (s3fs), y un
`push` normal falla al descomprimir el pack:

```
remote unpack failed: index-pack abnormal exit
```

Por eso `GIT_SLOW_REMOTES = gitea` hace que `push`, `push-all`, `push-tags` y
`release` empujen a ese remoto con `-c pack.threads=1 --no-thin` **solo a él**.
GitHub sigue con `push` normal. Ya no hay que recordar el workaround a mano.

## Convenciones de contenido

- Carpeta `YYYY-MM-DD-slug`, `index.md` con frontmatter YAML y `layout: post`.
- Imágenes **co-locadas** con el artículo, nunca en `/static`.
- `hugo.toml`: `mainSections = ['posts']`, `unsafe = true` en goldmark (permite
  HTML en markdown).

## Portadas

Cada artículo tiene su propia portada: un **motivo** (dibujo geométrico) y una
**paleta** elegidos por tema, no una plantilla con el título encima. El generador
está en `tools/coverart/`:

| Fichero | Qué define |
|---|---|
| `specs.py` | El reparto: qué motivo y qué paleta lleva cada artículo |
| `motifs.py` | Los motivos (redes, capas, fractales, sellos, órbitas…) |
| `palettes.py` | Las paletas (oscuras y claras) |
| `compose.py` | Composición: fondo, grano, velo, tipografía |

```bash
cd tools
python3 -m coverart --list          # ver el reparto motivo/paleta
python3 -m coverart --all           # generar todas
python3 -m coverart <slug>          # generar una
```

Escribe `og-image.svg` y lo rasteriza a `og-image-1200x630.png` (y 600×315). El
frontmatter apunta al **PNG**: las redes sociales no renderizan SVG en
`og:image`.

**Regla**: ninguna pareja (motivo, paleta) se repite. Si dos artículos comparten
tema, comparten motivo y cambian de paleta y de parámetros, de modo que se
reconocen como familia sin confundirse. Un artículo sin entrada en `specs.py`
recibe una plantilla sobria y un aviso.

El hook `pre-commit` regenera la portada **sólo de los artículos que entran en el
commit**, así que no hay que acordarse de nada.
