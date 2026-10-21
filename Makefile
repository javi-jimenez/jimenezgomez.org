# ============================================================
# jimenezgomez.org — Makefile (single source of truth)
#
# Los mismos targets se ejecutan desde LOCAL, desde DRONE o
# desde GitHub Actions. El Makefile es la única fuente de
# verdad: cada entorno solo aporta las herramientas.
#
# Patrón de detección (D2): cada receta usa la herramienta si ya
# está disponible en el entorno (p. ej. dentro del contenedor de
# un step de Drone) y, si no, la ejecuta vía `docker run` con una
# imagen OFICIAL. Así `make build`/`make deploy` funcionan igual
# en local, en Drone y en Actions sin instalar nada en el host.
# ============================================================

# ---- Imágenes oficiales (usa siempre imágenes oficiales) ----
HUGO_IMAGE   ?= ghcr.io/gohugoio/hugo:latest
ALPINE_IMAGE ?= alpine:3.18
DRONE_IMAGE  ?= drone/cli:latest
DEV_IMAGE    ?= jimenezgomez-dev

# ---- Config de despliegue ----
# Ruta remota en el servidor FTP (raíz del sitio, NO crear public/).
# `override` es DELIBERADO: el destino es intrínseco a este repo. Sin él, una
# variable FTP_REMOTE_PATH heredada del shell (p. ej. de otro proyecto) haría
# que `make deploy` subiera el sitio al directorio EQUIVOCADO (pasó el
# 2026-10-16: se subió este sitio encima de /laia.brisecom.org).
override FTP_REMOTE_PATH := /jimenezgomez.org/

# ---- Réplica de remotos ----
# El repo vive en dos forjas: GitHub (origin) y Gitea (gitea).
# `make push-all` / `make release` empujan a las dos.
GIT_REMOTES ?= origin gitea
GIT_BRANCH  ?= main

# ---- Targets ----
.PHONY: help dep build html deploy ftp-deploy dev-container create-dev-container \
	drone-run drone-exec serve gen-og gen-og-png install-hooks \
	version version-bump changelog-new readme-check \
	git-status git-commit push push-all pull tag push-tags release

help:
	@echo "Available targets:"
	@echo "  dep             dependencias/herramientas (no instala nada en el sistema)"
	@echo "  build (html)    genera public/ con Hugo"
	@echo "  deploy          genera y sube public/ al FTP (target: $(FTP_REMOTE_PATH))"
	@echo "  ftp-deploy      solo subida FTP (requiere public/ ya generado)"
	@echo "  dev-container   contenedor dev: shell si no hay args, comando si los hay"
	@echo "  create-dev-container   construye la imagen de desarrollo (Dockerfile.dev)"
	@echo "  drone-run       ejecuta el pipeline .drone.yml en local (drone exec)"
	@echo "  drone-exec      alias de drone-run"
	@echo "  serve           preview local de Hugo"
	@echo "  gen-og / gen-og-png   genera imágenes OG y miniaturas"
	@echo
	@echo "Versionado y git (lógica de makeit):"
	@echo "  version         muestra la versión; con VERSION=x.y.z la establece"
	@echo "  version-bump    sube la versión (BUMP=major|minor|patch)"
	@echo "  changelog-new   prepara la entrada de la versión en CHANGELOG.md"
	@echo "  readme-check    comprueba que README y CHANGELOG citan la versión"
	@echo "  git-status      estado de git"
	@echo "  git-commit      commit de todo (COMMIT_MSG=\"...\")"
	@echo "  push            commit + push a $(GIT_BRANCH) en origin"
	@echo "  push-all        commit + push a TODOS los remotos ($(GIT_REMOTES))"
	@echo "  tag             crea el tag <versión>-<timestamp>"
	@echo "  push-tags       sube los tags a todos los remotos"
	@echo "  release         tag + push-tags (etiquetar y publicar)"
	@echo
	@echo "Uso del contenedor dev:"
	@echo "  make dev-container                    # shell interactivo"
	@echo "  make dev-container EXEC='make build'  # ejecuta dentro y retorna"

# ------------------------------------------------------------
# dep — dependencias / herramientas
# No instala nada en el sistema: las herramientas corren en
# contenedores oficiales vía los targets build/deploy.
# ------------------------------------------------------------
dep:
	@echo "No system installs needed."
	@echo "Tools run in official Docker images via 'make build' / 'make deploy'."
	@echo "To run the Drone pipeline locally: make dev-container EXEC='make drone-run'."

# ------------------------------------------------------------
# build / html — genera public/ con Hugo
# Usa hugo si está en el entorno; si no, lo lanza en Docker.
# ------------------------------------------------------------
build:
	@echo "Building site with Hugo..."
	@if command -v hugo >/dev/null 2>&1; then \
		hugo --minify; \
	else \
		docker run --rm -v "$$PWD":/src -w /src "$(HUGO_IMAGE)" --minify; \
	fi

html: build

# ------------------------------------------------------------
# deploy — genera y sube al FTP
# Depende de build. Sube el CONTENIDO de public/ a la raíz del
# sitio (FTP_REMOTE_PATH), igual que hacía el pipeline validado.
# ------------------------------------------------------------
deploy: build
	@$(MAKE) ftp-deploy

# ------------------------------------------------------------
# ftp-deploy — solo la subida FTP
# Usa lftp si está en el entorno; si no, en contenedor Alpine.
# ------------------------------------------------------------
ftp-deploy:
	@# IMPORTANTE: todo va en UNA sola invocación de shell. Cada línea `@` de
	@# un Makefile es un shell distinto, así que cargar el .env en una línea no
	@# valía para las siguientes: el deploy solo funcionaba si FTP_* ya venían
	@# exportadas en el entorno (y entonces un FTP_REMOTE_PATH heredado ganaba).
	@set -e; \
	 if [ -f "$(CURDIR)/.env" ] && [ -z "$${FTP_SERVER:-}" ]; then \
	   set -a; . "$(CURDIR)/.env"; set +a; \
	 fi; \
	 if [ -z "$${FTP_SERVER:-}" ] || [ -z "$${FTP_USERNAME:-}" ] || [ -z "$${FTP_PASSWORD:-}" ]; then \
	   echo "ERROR: FTP_SERVER/FTP_USERNAME/FTP_PASSWORD no definidos (expórtalos o rellena .env)"; exit 1; \
	 fi; \
	 echo "Uploading public/ -> $(FTP_REMOTE_PATH) on $$FTP_SERVER"; \
	 if command -v lftp >/dev/null 2>&1; then \
	   lftp -u "$$FTP_USERNAME","$$FTP_PASSWORD" "$$FTP_SERVER" \
	     -e "set ssl:verify-certificate no; mirror -R public/. $(FTP_REMOTE_PATH) --delete --no-empty-dirs; bye"; \
	 else \
	   docker run --rm -v "$$PWD":/work -w /work \
	     -e FTP_USERNAME -e FTP_PASSWORD -e FTP_SERVER \
	     -e FTP_REMOTE_PATH="$(FTP_REMOTE_PATH)" \
	     "$(ALPINE_IMAGE)" sh -c \
	     'apk add --no-cache lftp >/dev/null && lftp -u "$$FTP_USERNAME","$$FTP_PASSWORD" "$$FTP_SERVER" -e "set ssl:verify-certificate no; mirror -R public/. $$FTP_REMOTE_PATH --delete --no-empty-dirs; bye"'; \
	 fi

# ------------------------------------------------------------
# dev-container — contenedor de desarrollo portable
#   make dev-container                  -> shell interactivo
#   make dev-container EXEC="make build"   -> ejecuta el comando dentro (no -it)
#   make dev-container EXEC="make drone-run"
# Pasa el comando a ejecutar dentro mediante la variable EXEC para
# evitar que make ejecute targets en el HOST. El contenedor lleva
# drone CLI + docker client + make; el repo y el socket de Docker
# se montan desde el host.
#
# IMPORTANTE: el repo se monta en la MISMA ruta del host ("$$PWD":"$$PWD")
# para que cualquier `docker run -v "$$PWD":...` anidado (make build/deploy)
# funcione con paths que el daemon de Docker del host sí reconoce.
# ------------------------------------------------------------
create-dev-container:
	docker build -t "$(DEV_IMAGE)" -f Dockerfile.dev .

dev-container: create-dev-container
	@if [ -z "$(EXEC)" ]; then \
		echo "Starting interactive shell in $(DEV_IMAGE)"; \
		docker run --rm -it \
			-v /var/run/docker.sock:/var/run/docker.sock \
			-v "$$PWD":"$$PWD" -w "$$PWD" "$(DEV_IMAGE)"; \
	else \
		echo "Running inside $(DEV_IMAGE): $(EXEC)"; \
		docker run --rm \
			-v /var/run/docker.sock:/var/run/docker.sock \
			-v "$$PWD":"$$PWD" -w "$$PWD" "$(DEV_IMAGE)" sh -c "$(EXEC)"; \
	fi

# ------------------------------------------------------------
# drone-run / drone-exec — ejecuta el pipeline .drone.yml en local
# Requiere el CLI de drone (se obtiene con 'make dev-container').
# ------------------------------------------------------------
drone-run:
	@echo "Running Drone pipeline locally (drone exec)..."
	@if command -v drone >/dev/null 2>&1; then \
		drone exec --trusted --secret-file=.env; \
	else \
		echo "drone CLI not found. Run inside the dev container:"; \
		echo "  make dev-container EXEC='make drone-run'"; \
		exit 1; \
	fi

drone-exec: drone-run

# ------------------------------------------------------------
# serve — preview local de Hugo
# ------------------------------------------------------------
serve:
	@if command -v hugo >/dev/null 2>&1; then \
		hugo server -D; \
	else \
		docker run --rm -it -p 1313:1313 -v "$$PWD":/src -w /src "$(HUGO_IMAGE)" server -D; \
	fi

# ------------------------------------------------------------
# OG helpers (generan imágenes de portada)
# ------------------------------------------------------------
gen-og:
	python3 tools/generate-og-image.py $(POST)

gen-og-png:
	./tools/generate-og-thumbnails.sh

# ------------------------------------------------------------
# install-hooks — activa los git hooks del repo
# ------------------------------------------------------------
install-hooks:
	@./tools/install-git-hooks.sh

# ============================================================
# Versionado, etiquetado y publicación
# ------------------------------------------------------------
# Esta sección es la de **makeit** (el framework de Makefiles de
# ~/data/repo/makeit) y se mantiene sincronizada con él: allí es la
# referencia, aquí la copia autocontenida.
#
# Por qué copiada y no `include`: este Makefile tiene que funcionar
# igual en local, en Drone y en GitHub Actions, donde
# ~/data/repo/makeit no existe. Un `include` de una ruta del HOME
# haría que `make build` / `make deploy` (la ruta de producción)
# dependiera de un directorio que solo está en esta máquina.
# Sincronizado con: makeit 0.3.0 (version, version-bump, changelog-new,
# readme-check, tag, push-tags, release, push-all, install-hooks).
#
# Política de versión visible: un tag es invisible desde dentro del
# proyecto, así que la versión vive en VERSION, en README.md (arriba)
# y en CHANGELOG.md (una entrada por tag, diciendo el porqué).
# ============================================================

VERSION_FILE    ?= VERSION
PROJECT_VERSION := $(shell cat $(VERSION_FILE) 2>/dev/null || echo 0.0.0)
README_FILE     ?= README.md
CHANGELOG_FILE  ?= CHANGELOG.md
CHANGELOG_AUTO  ?= 1

# ---- versión ----
version:
	@if [ -n "$(VERSION)" ]; then \
		printf "%s\n" "$(VERSION)" > $(VERSION_FILE); \
		echo "Version del proyecto: $(VERSION)"; \
	else \
		echo "jimenezgomez.org: $(PROJECT_VERSION)"; \
	fi

version-bump:
	@cur="$(PROJECT_VERSION)"; \
	major=$$(echo $$cur | cut -d. -f1); minor=$$(echo $$cur | cut -d. -f2); patch=$$(echo $$cur | cut -d. -f3); \
	case "$(BUMP)" in \
		major) major=$$((major+1)); minor=0; patch=0 ;; \
		minor) minor=$$((minor+1)); patch=0 ;; \
		patch|"") patch=$$((patch+1)) ;; \
		*) echo "BUMP debe ser major, minor o patch."; exit 1 ;; \
	esac; \
	new="$$major.$$minor.$$patch"; \
	printf "%s\n" "$$new" > $(VERSION_FILE); \
	echo "Version: $$cur -> $$new"

# ---- CHANGELOG ----
changelog-new:
	@ver="$$(cat $(VERSION_FILE) 2>/dev/null || echo 0.0.0)"; \
	if [ "$$ver" = "0.0.0" ]; then \
		echo "No hay version. Ejecuta 'make version VERSION=x.y.z'."; exit 1; \
	fi; \
	if [ ! -f "$(CHANGELOG_FILE)" ]; then \
		printf "# Changelog\n\n## [%s] — %s\n\n### Añadido\n\n### Cambiado\n\n### Corregido\n\n### Decidido\n" \
			"$$ver" "$$(date +%Y-%m-%d)" > "$(CHANGELOG_FILE)"; \
	else \
		tmp="$$(mktemp)"; \
		printf "# Changelog\n\n## [%s] — %s\n\n### Añadido\n\n### Cambiado\n\n### Corregido\n\n### Decidido\n\n" \
			"$$ver" "$$(date +%Y-%m-%d)" > "$$tmp"; \
		if head -1 "$(CHANGELOG_FILE)" | grep -q '^# Changelog'; then \
			tail -n +2 "$(CHANGELOG_FILE)" >> "$$tmp"; \
		else \
			cat "$(CHANGELOG_FILE)" >> "$$tmp"; \
		fi; \
		mv "$$tmp" "$(CHANGELOG_FILE)"; \
	fi; \
	echo "Entrada $$ver preparada en $(CHANGELOG_FILE)"

readme-check:
	@fail=0; \
	for f in $(README_FILE) $(CHANGELOG_FILE); do \
		if [ ! -f "$$f" ]; then echo "Falta $$f"; fail=1; fi; \
	done; \
	ver="$$(cat $(VERSION_FILE) 2>/dev/null || echo 0.0.0)"; \
	if [ "$$ver" != "0.0.0" ]; then \
		if [ -f "$(README_FILE)" ] && ! grep -qF "$$ver" "$(README_FILE)"; then \
			echo "$(README_FILE) no menciona la version $$ver"; fail=1; fi; \
		if [ -f "$(CHANGELOG_FILE)" ] && ! grep -qF "$$ver" "$(CHANGELOG_FILE)"; then \
			echo "$(CHANGELOG_FILE) no tiene entrada para $$ver"; fail=1; fi; \
	fi; \
	if [ "$$fail" -eq 0 ]; then echo "OK: version $$ver visible en README y CHANGELOG"; \
	else exit 1; fi

# ---- git ----
git-status:
	@git status --short --branch

git-commit:
	@git add -A; \
	if git diff --cached --quiet; then \
		echo "Sin cambios que commitear."; \
	else \
		git commit -m "$(if $(COMMIT_MSG),$(COMMIT_MSG),chore: sincronizar)"; \
		echo "Commit creado."; \
	fi

push:
	@$(MAKE) --no-print-directory git-commit
	@git push origin $(GIT_BRANCH)
	@echo "Subido a origin/$(GIT_BRANCH)."

pull:
	@git pull origin $(GIT_BRANCH)

# Réplica: un commit y un push por remoto. El fallo de uno NO aborta los
# demás (puede estar caído) pero sí afecta al código de salida, para no
# dar por buena una subida a medias.
push-all:
	@$(MAKE) --no-print-directory git-commit
	@remotes="$(GIT_REMOTES)"; fail=0; \
	for r in $$remotes; do \
		printf "  %-10s -> " "$$r"; \
		out=$$(git push "$$r" "$(GIT_BRANCH)" 2>&1); rc=$$?; \
		if [ $$rc -eq 0 ]; then echo "ok"; \
		else echo "ERROR"; printf "%s\n" "$$out" | sed 's/^/    /'; fail=1; fi; \
	done; \
	if [ $$fail -eq 0 ]; then echo "Subido a todos los remotos."; \
	else echo "Algun remoto fallo (ver arriba)."; exit 1; fi

# Etiqueta con timestamp: <version>-YYYYMMDDHHMM (convención de makeit).
# Antes de etiquetar, garantiza la entrada del CHANGELOG y **la commitea**:
# sin ese commit la entrada quedaría fuera del tag.
tag:
	@stamp=$$(date +%Y%m%d%H%M); \
	ver="$(PROJECT_VERSION)"; \
	if [ -n "$$ver" ] && [ "$$ver" != "0.0.0" ]; then tag="$$ver-$$stamp"; else tag="$$stamp"; fi; \
	if git rev-parse "$$tag" >/dev/null 2>&1; then \
		echo "El tag $$tag ya existe."; \
	else \
		if [ "$(CHANGELOG_AUTO)" != "0" ] && [ -n "$$ver" ] && [ "$$ver" != "0.0.0" ]; then \
			if ! grep -qF "## [$$ver]" "$(CHANGELOG_FILE)" 2>/dev/null; then \
				$(MAKE) --no-print-directory changelog-new >/dev/null 2>&1 || true; \
			fi; \
			if [ -n "$$(git status --porcelain -- "$(CHANGELOG_FILE)" 2>/dev/null)" ]; then \
				git add "$(CHANGELOG_FILE)"; \
				git commit -q -m "changelog: entrada $$ver (antes del tag)" -- "$(CHANGELOG_FILE)"; \
				echo "Entrada $$ver commiteada en $(CHANGELOG_FILE) — rellénala."; \
			fi; \
		fi; \
		git tag -a "$$tag" -m "Release $$tag"; \
		echo "Tag $$tag creado."; \
	fi

push-tags:
	@remotes="$(GIT_REMOTES)"; fail=0; \
	for r in $$remotes; do \
		printf "  %-10s -> " "$$r"; \
		out=$$(git push "$$r" --tags 2>&1); rc=$$?; \
		if [ $$rc -eq 0 ]; then echo "ok"; \
		else echo "ERROR"; printf "%s\n" "$$out" | sed 's/^/    /'; fail=1; fi; \
	done; \
	[ $$fail -eq 0 ] || { echo "Algun remoto rechazo los tags."; exit 1; }

# Etiquetar y publicar en un paso.
release:
	@$(MAKE) --no-print-directory tag
	@$(MAKE) --no-print-directory push-tags

