#!/usr/bin/env sh
set -e

# Script to generate the site HTML using Hugo.
# If `hugo` is present in PATH it will be used. Otherwise a Docker image is used as fallback.

if command -v hugo >/dev/null 2>&1; then
  echo "Using local hugo"
  hugo --minify
  exit 0
fi

IMAGE="${HUGO_DOCKER_IMAGE:-klakegg/hugo:0.155.2-ext}"
echo "Running Hugo via Docker image ${IMAGE}"
docker run --rm -v "$PWD":/src -w /src "${IMAGE}" hugo --minify
