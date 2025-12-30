#!/usr/bin/env bash
# Create a GitHub issue for RFC-0001 using environment variables

set -euo pipefail

REPO="${GITHUB_REPOSITORY:-}"
TOKEN="${GITHUB_TOKEN:-}"
TITLE="RFC-0001: Request for comments — ASSISTANT_CONTEXT"
BODY_FILE="tools/rfcs/RFC-0001-ISSUE-BODY.md"

if [ -z "$REPO" ] || [ -z "$TOKEN" ]; then
  echo "Please set GITHUB_REPOSITORY and GITHUB_TOKEN in your environment." >&2
  exit 1
fi

if [ ! -f "$BODY_FILE" ]; then
  cat > "$BODY_FILE" <<'EOF'
This issue opens the Request For Comments for RFC-0001: ASSISTANT_CONTEXT.

See file: `tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md`

Please comment below or submit a PR with suggested edits to the RFC file.

Suggested discussion topics:
- required/optional fields
- placement/visibility of the file
- security and privacy best practices

EOF
fi

DATA=$(jq -n --arg t "$TITLE" --arg b "$(cat "$BODY_FILE")" '{title: $t, body: $b}')

curl -s -X POST "https://api.github.com/repos/$REPO/issues" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "$DATA"

echo "Issue creation requested. Check repository issues." 
