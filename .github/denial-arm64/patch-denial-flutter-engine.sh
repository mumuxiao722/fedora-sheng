#!/usr/bin/env bash
set -euo pipefail

repo_dir="${1:?usage: patch-denial-flutter-engine.sh <repo-dir>}"
tool="${repo_dir%/}/tools/denial-flutter-engine"
[[ -f "$tool" ]] || { echo "tool not found: $tool" >&2; exit 1; }

python3 - "$tool" <<'PY'
import re, sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    s = f.read()
if "patch-deps.py" in s:
    print("already patched")
    sys.exit(0)
m = re.search(r"^(\s*)gclient sync --no-history --nohooks\s*$", s, re.M)
if not m:
    sys.exit("anchor not found: gclient sync line in " + path)
indent = m.group(1)
insert = indent + 'python3 "$ROOT/../.github/denial-arm64/patch-deps.py" "$CHECKOUT/DEPS"\n'
s = s[: m.start()] + insert + s[m.start():]
with open(path, "w", encoding="utf-8") as f:
    f.write(s)
print("injected patch-deps.py before gclient sync")
PY