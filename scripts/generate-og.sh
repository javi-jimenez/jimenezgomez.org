#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <post_dir>"
  exit 1
fi
POST_DIR="$1"
TEMPLATE="$(git rev-parse --show-toplevel)/assets/og-template.svg"
OUT_SVG="$POST_DIR/og-image.svg"
OUT_PNG1="$POST_DIR/og-image-1200x630.png"
OUT_PNG2="$POST_DIR/og-image-600x315.png"

INDEX_MD="$POST_DIR/index.md"
if [ ! -f "$INDEX_MD" ]; then
  echo "index.md not found in $POST_DIR"
  exit 1
fi

# extract frontmatter values (simple sed/grep approach)
FRONT=$(sed -n '1,200p' "$INDEX_MD" | sed -n '/^---$/,/^---$/p')

title=$(echo "$FRONT" | sed -n 's/^title: *"\(.*\)"/\1/p' | head -n1)
[ -z "$title" ] && title=$(echo "$FRONT" | sed -n "s/^title: *'\(.*\)'/\1/p" | head -n1)

date=$(echo "$FRONT" | sed -n 's/^date: *\(.*\)/\1/p' | head -n1)

author=$(echo "$FRONT" | sed -n 's/^author: *"\(.*\)"/\1/p' | head -n1)
[ -z "$author" ] && author=""

excerpt=$(echo "$FRONT" | sed -n 's/^description: *"\(.*\)"/\1/p' | head -n1)
if [ -z "$excerpt" ]; then
  excerpt=$(echo "$FRONT" | sed -n "s/^description: *'\(.*\)'/\1/p" | head -n1)
fi

image=$(echo "$FRONT" | sed -n 's/^image: *"\(.*\)"/\1/p' | head -n1)
if [ -z "$image" ]; then
  image=$(ls "$POST_DIR"/*.png 2>/dev/null | head -n1 || true)
  image=${image##*/}
fi

SITE_NAME="Mi Sitio"

# fallback values
[ -z "$date" ] && date=""
[ -z "$title" ] && title=""
[ -z "$excerpt" ] && excerpt=""

# export for envsubst
export TITLE="$title"
export DATE="$date"
export AUTHOR="$author"
export EXCERPT="$excerpt"
export POST_IMAGE="$image"
export SITE_NAME="$SITE_NAME"

# generate svg via envsubst
if [ ! -f "$TEMPLATE" ]; then
  echo "Template $TEMPLATE not found"
  exit 1
fi

envsubst < "$TEMPLATE" > "$OUT_SVG"

echo "Generated $OUT_SVG"

# render PNGs: require inkscape (more robust). Do not fall back to rsvg-convert to avoid librsvg crashes.
if command -v inkscape >/dev/null 2>&1; then
  inkscape "$OUT_SVG" --export-filename="$OUT_PNG1" -w 1200 -h 630
  inkscape "$OUT_SVG" --export-filename="$OUT_PNG2" -w 600 -h 315
  echo "Rendered PNGs with inkscape"
else
  echo "Inkscape not found. SVG generated at $OUT_SVG. Install inkscape to render PNGs."
  exit 0
fi

echo "OG images generated in $POST_DIR"
