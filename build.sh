#!/bin/sh
# Build a scene into a project, render a check frame, and compare it with its reference.
#   ./build.sh hero            → out/hero.ecproj, out/hero-1s.png, PASS/FAIL against refs/hero-1s.png
#   ./build.sh hero --bless    → accept the new render as the reference
# EFFECTCRAFT_CLI picks the CLI (default: effectcraft-cli on PATH).
set -e
KIT=$(cd "$(dirname "$0")" && pwd)
CLI=${EFFECTCRAFT_CLI:-effectcraft-cli}
NAME=$1
mkdir -p "$KIT/out"
"$CLI" script "$KIT/$NAME.jsx" --empty --save-as "$KIT/out/$NAME.ecproj"
"$CLI" render-frame "$KIT/out/$NAME.ecproj" --comp Main --time 1 --out "$KIT/out/$NAME-1s.png"
if [ "$2" = "--bless" ] || [ ! -f "$KIT/refs/$NAME-1s.png" ]; then
  cp "$KIT/out/$NAME-1s.png" "$KIT/refs/$NAME-1s.png" && echo "reference saved: refs/$NAME-1s.png"
else
  "$CLI" compare "$KIT/refs/$NAME-1s.png" "$KIT/out/$NAME-1s.png" --diff "$KIT/out/$NAME-diff.png"
fi
