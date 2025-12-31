Social publish tools

This folder contains small helpers to publish content to social networks from your local machine without sharing secrets here.

Secure credential practice
- Create a local env file at `~/.config/linkedin_publish.env` with these variables (do not commit):

  LINKEDIN_ACCESS_TOKEN="your_long_lived_token"
  LINKEDIN_URN="urn:li:person:XXXXXXXX"

  Then secure it:

  ```bash
  mkdir -p "$HOME/.config"
  cp tools/social/example.env "$HOME/.config/linkedin_publish.env"
  chmod 600 "$HOME/.config/linkedin_publish.env"
  ```

LinkedIn (local publish)
- Script: `tools/social/linkedin/publish_local.sh`
- It reads `~/.config/linkedin_publish.env` (if present) or environment variables and posts the provided text.
- Usage examples:

```bash
# one-liner text
LINKEDIN_ACCESS_TOKEN=... LINKEDIN_URN=urn:li:person:... ./tools/social/linkedin/publish_local.sh "Mi post corto" 

# or from file
./tools/social/linkedin/publish_local.sh tools/social/linkedin/dns-universal-summary.txt
```

Buffer (3rd party)
- Buffer is a third-party scheduler. If you prefer to schedule via Buffer you can use their API; DO NOT paste tokens here. Example curl (needs `BUFFER_TOKEN` and `PROFILE_ID`):

```bash
curl -X POST https://api.bufferapp.com/1/updates/create.json \
  -d "text=TU_TEXTO_AQUI" \
  -d "profile_ids[]=PROFILE_ID" \
  -d "now=false" \
  -H "Authorization: Bearer BUFFER_TOKEN"
```

Notes
- I cannot accept secrets here. Use the local script above to keep tokens on your machine.
- If you want, I can: (1) prepare a GitHub Action / Drone step that reads secrets from your CI provider (you provide them there), or (2) prepare more scripts to format images/links for richer posts.
