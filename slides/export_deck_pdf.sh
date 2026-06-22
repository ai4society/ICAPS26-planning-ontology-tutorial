#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT_PDF="${1:-$ROOT/final/maPO-AAAI-MAKE.pdf}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

mkdir -p "$(dirname "$OUT_PDF")"

# Keep PDF export in sync with the current slide HTML.
"$ROOT/render_deck.sh"

"$CHROME" \
  --headless \
  --disable-gpu \
  --print-to-pdf="$OUT_PDF" \
  --no-pdf-header-footer \
  --virtual-time-budget=6000 \
  "file://$ROOT/deck-print.html" >/dev/null

echo "Exported deck PDF to $OUT_PDF"
