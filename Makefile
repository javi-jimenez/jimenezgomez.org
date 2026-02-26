# Makefile additions for OG generation
.PHONY: gen-og

gen-og:
	python3 tools/generate-og-image.py $(POST)

.PHONY: gen-og-png
gen-og-png:
	./tools/generate-og-thumbnails.sh

# CI / site targets
.PHONY: help html build serve docker-build docker-tag drone-exec ftp-deploy deploy commit push ci

HUGO_DOCKER_IMAGE ?= klakegg/hugo:0.155.2-ext
DOCKER_IMAGE ?= jimenezgomez-blog

# Load environment from `.env` file into the shell for recipes that need it.
# Use $(CURDIR) so sourcing works regardless of the shell's working directory
# (prevents ".: .env: not found" when make runs recipes in different shells).
ENV_LOAD = if [ -f "$(CURDIR)/.env" ]; then set -a; . "$(CURDIR)/.env"; set +a; fi

help:
	@echo "Available targets: html build serve docker-build docker-tag drone-exec ftp-deploy deploy commit push ci gen-og gen-og-png"

html:
	@echo "Generating site HTML..."
	$(ENV_LOAD)
	sh scripts/generate-html.sh

build: html

serve:
	@echo "Starting Hugo server (local or Docker fallback)..."
	$(ENV_LOAD)
	@if command -v hugo >/dev/null 2>&1; then \
		hugo server -D; \
	else \
		docker run --rm -it -p 1313:1313 -v "$$PWD":/src -w /src $(HUGO_DOCKER_IMAGE) hugo server -D; \
	fi

docker-build:
	@echo "Building Docker image $(DOCKER_IMAGE):latest"
	docker build -t $(DOCKER_IMAGE):latest .

docker-tag:
	@echo "Tagging Docker image with commit sha (if available)"
	$(ENV_LOAD)
	@if [ -n "$$DRONE_COMMIT_SHA" ]; then \
		docker tag $(DOCKER_IMAGE):latest $(DOCKER_IMAGE):$${DRONE_COMMIT_SHA:0:8}; \
	else \
		echo "DRONE_COMMIT_SHA not set; skipping tag"; \
	fi

drone-exec:
	@echo "Running Drone pipeline locally (requires drone CLI + docker)"
	@drone exec --trusted

ftp-deploy:
	@echo "Deploying public/ via FTP (uses lftp or Dockerized lftp)."
	$(ENV_LOAD)
	@if [ -z "$$FTP_HOST" ] || [ -z "$$FTP_USER" ] || [ -z "$$FTP_PASSWORD" ] || [ -z "$$FTP_REMOTE_PATH" ]; then \
		echo "FTP_HOST/USER/PASSWORD/REMOTE_PATH not set; skipping deploy"; exit 0; \
	fi
	@if command -v lftp >/dev/null 2>&1; then \
		lftp -u "$$FTP_USER","$$FTP_PASSWORD" "$$FTP_HOST" -e "mirror -R public $$FTP_REMOTE_PATH --delete --verbose; bye"; \
	else \
		docker run --rm -v "$$PWD":/work -w /work alpine:3.18 sh -c "apk add --no-cache lftp >/dev/null && lftp -u '$$FTP_USER','$$FTP_PASSWORD' '$$FTP_HOST' -e \"mirror -R public $$FTP_REMOTE_PATH --delete --verbose; bye\""; \
	fi

deploy: html ftp-deploy

ci: build docker-build docker-tag

commit:
	@echo "Staging changes and committing"
	@git add scripts/generate-html.sh .drone.yml Makefile || true
	@git commit -m "ci: add Makefile targets for build, serve, drone and deploy" || echo "No changes to commit"

push:
	@echo "Pushing to origin"
	@git push

