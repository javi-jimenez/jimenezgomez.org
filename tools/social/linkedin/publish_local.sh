#!/usr/bin/env bash
set -euo pipefail

# publish_local.sh
# Usage: publish_local.sh path/to/textfile.txt
# Reads LINKEDIN_ACCESS_TOKEN and LINKEDIN_URN from environment.

if [ -f "$HOME/.config/linkedin_publish.env" ]; then
  # shellcheck disable=SC1090
  source "$HOME/.config/linkedin_publish.env"
fi

if [ -z "${LINKEDIN_ACCESS_TOKEN:-}" ] || [ -z "${LINKEDIN_URN:-}" ]; then
  echo "Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_URN. Create ~/.config/linkedin_publish.env with these variables (chmod 600)."
  exit 1
fi

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <text-or-file>"
  exit 1
fi

INPUT="$1"
if [ -f "$INPUT" ]; then
  TEXT=$(cat "$INPUT")
else
  TEXT="$INPUT"
fi

# Build JSON payload using Python to ensure proper escaping
PAYLOAD=$(python3 - <<PY
import json,sys
author = "$LINKEDIN_URN"
text = sys.stdin.read()
obj = {
  "author": author,
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {"text": text},
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
}
print(json.dumps(obj))
PY
<<<"$TEXT")

echo "Posting to LinkedIn as $LINKEDIN_URN..."
curl -s -X POST "https://api.linkedin.com/v2/ugcPosts" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" | jq || true

echo "Done. Check output above for the created post or errors."
