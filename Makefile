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

# ---- Targets ----
.PHONY: help dep build html deploy ftp-deploy dev-container create-dev-container \
	drone-run drone-exec serve gen-og gen-og-png install-hooks

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

