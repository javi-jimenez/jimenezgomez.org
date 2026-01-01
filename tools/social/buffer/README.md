Buffer publish helper

This folder contains a small helper to publish a text post to Buffer from your local machine.

Requirements
- `curl`, `jq` installed.
- Add your Buffer credentials to `~/.config/linkedin_publish.env` (or export them in your shell):

```ini
# Buffer API token (obtain from your Buffer account)
BUFFER_TOKEN="your_buffer_token"
# Buffer profile id to post to (found in Buffer UI or API)
BUFFER_PROFILE_ID="your_profile_id"
```

Usage

Post a file:

```bash
./tools/social/buffer/publish_buffer.sh -f tools/social/linkedin/dns-universal-summary.txt
```

Or post a short text directly:

```bash
./tools/social/buffer/publish_buffer.sh "Mi texto para publicar en LinkedIn via Buffer"
```

Notes
- Keep `BUFFER_TOKEN` secret. Do not commit it. Use `chmod 600 ~/.config/linkedin_publish.env`.
- The script posts immediately (`now=true`). Edit script to schedule instead.
