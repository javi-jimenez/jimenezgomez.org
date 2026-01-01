#!/usr/bin/env bash
set -euo pipefail

# publish_buffer.sh
# Usage:
#   ./publish_buffer.sh "Text to post"            # post immediately
#   ./publish_buffer.sh -f path/to/file.txt        # post file contents
# Reads BUFFER_TOKEN and BUFFER_PROFILE_ID from env or ~/.config/linkedin_publish.env

ENV_FILE="$HOME/.config/linkedin_publish.env"
if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE" || true
fi

if [ -z "${BUFFER_TOKEN:-}" ] || [ -z "${BUFFER_PROFILE_ID:-}" ]; then
  echo "Missing BUFFER_TOKEN or BUFFER_PROFILE_ID. Set them in ~/.config/linkedin_publish.env or env." >&2
  exit 1
fi

TEXT=""
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 [-f file] <text>" >&2
  exit 1
fi

if [ "$1" = "-f" ]; then
  if [ -z "${2:-}" ] || [ ! -f "$2" ]; then
    echo "File not found: $2" >&2
    exit 1
  fi
  TEXT=$(cat "$2")
else
  TEXT="$*"
fi

echo "Posting to Buffer profile $BUFFER_PROFILE_ID..."

RESPONSE=$(curl -s -X POST "https://api.bufferapp.com/1/updates/create.json" \
  -H "Authorization: Bearer ${BUFFER_TOKEN}" \
  -d "text=${TEXT}" \
  -d "profile_ids[]=${BUFFER_PROFILE_ID}" \
  -d "now=true")

echo "$RESPONSE" | jq || echo "$RESPONSE"

echo "Done. Check response above for status and post id."
