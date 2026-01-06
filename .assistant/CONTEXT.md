Project context (auto-generated)
================================

Repository: Hugo site (content under `content/posts`).

What I changed/added in this session:
- Added frontmatter to `2026-01-06-smartphone-sin-sim-y-telefono-basico/index.md` and `og_image` field.
- Replaced HTML `<img>` in that post with Markdown image syntax.
- Added `assets/og-template.svg` (SVG template for OG images).
- Added `scripts/generate-og.sh` (fills template from frontmatter and renders PNGs with Inkscape).
- Installed `librsvg2-bin` and `inkscape` in the environment to render SVGs.
- Generated `og-image.svg`, `og-image-1200x630.png`, `og-image-600x315.png` for the post and committed them.

Pre-commit/CI behavior observed:
- A pre-commit hook runs OG generation for staged posts (seen in commit logs).

Important files:
- `content/posts/...` : blog posts (frontmatter + markdown content).
- `assets/og-template.svg` : SVG template, placeholders: $TITLE, $DATE, $AUTHOR, $EXCERPT, $POST_IMAGE, $SITE_NAME.
- `scripts/generate-og.sh` : generate OG SVG/PNGs from a post directory (requires `envsubst` and `inkscape`).

How to regenerate OG images locally:
1. Install Inkscape (Debian/Ubuntu):
   sudo apt update
   sudo apt install -y inkscape

2. Run the generator for a post (example):
   bash scripts/generate-og.sh content/posts/2026-01-06-smartphone-sin-sim-y-telefono-basico

3. The script will create `og-image.svg`, `og-image-1200x630.png`, `og-image-600x315.png` inside the post folder.

Notes about SVG renderers:
- `rsvg-convert` (librsvg) was unstable for some SVG content (stack overflow). The script was adjusted to require Inkscape to avoid crashes.

Suggested next steps I can do for you:
- Update the site layout to show posts as card boxes (image, title link, excerpt summary).
- Make the OG generator more robust (text wrapping, font embedding) or add a CI step that runs in GitHub Actions using `inkscape` or Puppeteer.
- Add a small README or usage notes for contributors.

Saved session snapshot: This file records the essential state and commands to reproduce the work done by the assistant.

Assistant context update rule:
- When the user asks the assistant to "actualiza el fichero de contexto" or to "update the context file", the assistant MUST update `.assistant/CONTEXT.md` with the current project state, including:
   - brief summary of recent changes
   - list of important files and scripts added or modified
   - commands to reproduce any generated assets (OG images, thumbnails)
   - any notes about environment requirements (Inkscape, librsvg, fonts)
   - a short reminder line: "REMEMBER: ask the assistant to update the context file when you want the session state saved"

This file is the canonical place for session context; other assistants or automation should read it to resume work.
