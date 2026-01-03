OG Image generation

This repository includes a small helper to generate a basic `og-image.svg` for a Hugo post.

Usage

```bash
# generate OG for a post folder
make gen-og POST=content/posts/2026-01-03-slug

# generate and update frontmatter (if you want the script to set `image` in index.md):
python3 tools/generate-og-image.py content/posts/2026-01-03-slug --set-frontmatter
```

How it works

- The script creates `og-image.svg` inside the given post folder.
- It can optionally edit the post frontmatter to set `image: "og-image.svg"`.

Automation suggestions

- Add a pre-commit hook that runs the script for newly created post folders.
- Add a CI check that verifies every post has an `image` frontmatter value.
