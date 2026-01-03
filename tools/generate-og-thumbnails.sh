#!/usr/bin/env bash
set -euo pipefail
# Generate PNG thumbnails (1200x630 and 600x315) from og-image.svg files.
# Requires ImageMagick `convert` or `rsvg-convert`/`cairosvg` available.

which_convert() { command -v convert >/dev/null 2>&1; }
which_rsvg() { command -v rsvg-convert >/dev/null 2>&1; }
which_cairosvg() { command -v cairosvg >/dev/null 2>&1; }

OUT_SIZES=("1200x630" "600x315")

fail() { echo "ERROR: $1" >&2; exit 1; }

if ! which_convert && ! which_rsvg && ! which_cairosvg; then
  fail "No rasterizer found. Install ImageMagick (convert), librsvg (rsvg-convert) or cairosvg."
fi

find content/posts -type f -name og-image.svg | while read -r svg; do
  dir=$(dirname "$svg")
  base="$dir/og-image"
  echo "Processing $svg"
  if which_convert; then
    for size in "${OUT_SIZES[@]}"; do
      w=${size%x*}
      h=${size#*x}
      out="${base}-${w}x${h}.png"
      convert -background none -resize ${w}x${h} -gravity center "$svg" -extent ${w}x${h} "$out"
    done
  elif which_rsvg; then
    # rsvg-convert outputs PNG natively
    for size in "${OUT_SIZES[@]}"; do
      w=${size%x*}
      h=${size#*x}
      out="${base}-${w}x${h}.png"
      rsvg-convert -w "$w" -h "$h" -o "$out" "$svg"
    done
  else
    # cairosvg
    for size in "${OUT_SIZES[@]}"; do
      w=${size%x*}
      h=${size#*x}
      out="${base}-${w}x${h}.png"
      cairosvg "$svg" -o "$out" -w "$w"
    done
  fi
done

echo "Thumbnails generated."
