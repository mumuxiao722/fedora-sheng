#!/usr/bin/env bash
# Minimal ARM64 workaround for upstream tools/denial-flutter-engine.
# Strips the flutter/java/openjdk CIPD dep (no linux-arm64 package exists) for
# gclient sync, then restores DEPS so locked-checkout checks still pass.
set -euo pipefail

TOOL="$1/tools/denial-flutter-engine"
[[ -f "$TOOL" ]] || { echo "missing tool: $TOOL" >&2; exit 1; }

python3 - "$TOOL" <<'PY'
import sys

tool = sys.argv[1]
src = open(tool, encoding='utf-8').read()

if 'strip-jdk.py' in src:
    sys.exit(0)

anchor = '  write_gclient_config "$flutter_repository"'
assert src.count(anchor) == 1, 'gclient config anchor not unique'
src = src.replace(
    anchor,
    '  # ARM64: drop the openjdk CIPD dep (no linux-arm64 package upstream).\n'
    '  python3 "$ROOT/../.github/denial-arm64/strip-jdk.py" "$CHECKOUT/DEPS"\n'
    + anchor,
    1,
)

anchor = '      gclient runhooks\n  )\n\n  checkout_matches_lock \\'
assert src.count(anchor) == 1, 'sync-restore anchor not unique'
src = src.replace(
    anchor,
    '      gclient runhooks\n  )\n\n  git -C "$CHECKOUT" checkout --quiet -- DEPS\n'
    '  checkout_matches_lock \\',
    1,
)

open(tool, 'w', encoding='utf-8').write(src)
PY

echo "✓ ARM64 denial-flutter-engine patch applied"