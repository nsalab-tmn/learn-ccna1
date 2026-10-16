#!/bin/bash
# Normalise every tracked raster to a PNG <=1200px wide for viewing; GIFs -> first/middle/last frame strip.
# Usage: prep_rasters.sh OUT_DIR   (needs ImageMagick: identify, convert)
set -u
OUT=$(realpath -m "$1"); mkdir -p "$OUT"
REPO=${AUDIT_REPO:-$(cd "$(dirname "$0")/../.." && pwd)}
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
cd "$REPO"
git ls-files | grep -iE '\.(png|jpe?g|gif)$' | while read -r f; do
  key=$(echo "$f" | sed 's#/#__#g')
  case "${f,,}" in
    *.gif)
      n=$(identify -format '%n\n' "$f" 2>/dev/null | head -1); n=${n:-1}
      if [ "$n" -gt 1 ]; then
        mid=$((n/2)); last=$((n-1))
        convert "$f" -coalesce "$TMP/_all_%03d.png" 2>/dev/null
        convert "$TMP/_all_$(printf %03d 0).png" "$TMP/_all_$(printf %03d $mid).png" "$TMP/_all_$(printf %03d $last).png" -resize '700x>' +append -background white -flatten "$OUT/$key.png"
        rm -f "$TMP"/_all_*.png
        echo "$f gif frames=$n" >> "$OUT/_gif.txt"
      else
        convert "$f[0]" -background white -flatten -resize '1200x>' "$OUT/$key.png"
      fi;;
    *) convert "$f[0]" -background white -flatten -resize '1200x>' "$OUT/$key.png" 2>>"$OUT/_err.txt";;
  esac
done
echo done
