#!/usr/bin/env bash
# Pulls the woff2 files the ads use into this folder and writes fonts.css.
# Rendering reads these from disk, so a render never depends on the network.
set -euo pipefail
cd "$(dirname "$0")"
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
SPEC='family=Merriweather:wght@700;900&family=Source+Sans+3:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap'
curl -sS -A "$UA" "https://fonts.googleapis.com/css2?${SPEC}" -o raw.css
: > fonts.css
grep -oE 'https://fonts\.gstatic\.com/[^)]+\.woff2' raw.css | sort -u | while read -r url; do
  name="$(basename "$url")"
  [ -f "$name" ] || curl -sS -A "$UA" "$url" -o "$name"
done
sed -E 's#https://fonts\.gstatic\.com/[^)]*/([^/)]+\.woff2)#./\1#g' raw.css > fonts.css
rm -f raw.css
echo "$(ls -1 *.woff2 | wc -l) woff2 files, $(du -sh . | cut -f1) total"
