#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="${1:-$ROOT/renders/export}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

mkdir -p "$OUT_DIR"

for slide in "$ROOT"/slide-[0-9][0-9]-*.html; do
  base="$(basename "$slide" .html)"
  "$CHROME" \
    --headless \
    --disable-gpu \
    --hide-scrollbars \
    --window-size=1920,1080 \
    --screenshot="$OUT_DIR/$base.png" \
    "file://$slide?render=1" >/dev/null
done

echo "Rendered slides to $OUT_DIR"
