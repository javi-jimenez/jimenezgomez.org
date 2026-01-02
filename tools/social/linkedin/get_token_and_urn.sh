#!/usr/bin/env bash
set -euo pipefail

# get_token_and_urn.sh
# Interactive helper to obtain a LinkedIn access token (authorization code flow)
# and write LINKEDIN_ACCESS_TOKEN and LINKEDIN_URN to ~/.config/linkedin_publish.env
# Usage: ./get_token_and_urn.sh

CONFIG_DIR="$HOME/.config"
ENV_FILE="$CONFIG_DIR/linkedin_publish.env"

echo "This script helps you obtain a LinkedIn access token and compute your URN."
echo "It will prompt for your app credentials and redirect URI."

read -rp "Enter LinkedIn Client ID: " CLIENT_ID
read -rp "Enter LinkedIn Client Secret: " CLIENT_SECRET
read -rp "Enter Redirect URI (must match app config, e.g. http://localhost:3000/callback): " REDIRECT_URI

SCOPES="r_liteprofile w_member_social r_emailaddress"

AUTH_URL="https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=$(echo ${SCOPES} | sed 's/ /%20/g')"

echo
echo "Open the following URL in your browser, authorize the app, and copy the 'code' parameter from the redirected URL:"
echo
echo "$AUTH_URL"
echo
if command -v xdg-open >/dev/null 2>&1; then
  read -rn1 -p "Open URL in default browser? (y/N) " OPEN_NOW
  echo
  if [[ "$OPEN_NOW" =~ ^[Yy]$ ]]; then
    xdg-open "$AUTH_URL" || true
  fi
fi

read -rp "Paste the 'code' parameter from the redirect URL here: " AUTH_CODE

echo "Exchanging code for access token..."

RESP=$(curl -s -X POST "https://www.linkedin.com/oauth/v2/accessToken" \
  -d grant_type=authorization_code \
  -d code="$AUTH_CODE" \
  -d redirect_uri="$REDIRECT_URI" \
  -d client_id="$CLIENT_ID" \
  -d client_secret="$CLIENT_SECRET")

ACCESS_TOKEN=$(echo "$RESP" | jq -r '.access_token // empty')
EXPIRES_IN=$(echo "$RESP" | jq -r '.expires_in // empty')

if [ -z "$ACCESS_TOKEN" ]; then
  echo "Failed to obtain access token. Response:" >&2
  echo "$RESP" >&2
  exit 1
fi

echo "Access token obtained (expires_in=$EXPIRES_IN). Fetching profile id..."

ME=$(curl -s -H "Authorization: Bearer $ACCESS_TOKEN" https://api.linkedin.com/v2/me)
PERSON_ID=$(echo "$ME" | jq -r '.id // empty')

if [ -z "$PERSON_ID" ]; then
  echo "Failed to fetch profile id. Response:" >&2
  echo "$ME" >&2
  exit 1
fi

URN="urn:li:person:${PERSON_ID}"

mkdir -p "$CONFIG_DIR"

cat > "$ENV_FILE" <<EOF
# LinkedIn local publish credentials (store securely; do not commit)
LINKEDIN_ACCESS_TOKEN="$ACCESS_TOKEN"
LINKEDIN_URN="$URN"
EOF

chmod 600 "$ENV_FILE"

echo "Wrote credentials to $ENV_FILE"
echo "LINKEDIN_URN=$URN"
echo "You can now run: ./tools/social/linkedin/publish_local.sh tools/social/linkedin/dns-universal-summary.txt"
