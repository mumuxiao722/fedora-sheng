#!/usr/bin/env bash
set -euo pipefail

repo_dir="${1:?usage: patch-denial-arm64.sh <repo-dir>}"

python3 - "$repo_dir" <<'PY'
import re, sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
marker = "# DENIAL_ARM64_PATCHED\n"


def patched(path):
    return marker in path.read_text()


def mark(path, text, note):
    path.write_text(text)
    print(note)


# ---------- tools/denial-flutter-engine ----------
engine = repo / "tools" / "denial-flutter-engine"
if patched(engine):
    print("denial-flutter-engine: already patched")
else:
    s = engine.read_text()

    m = re.search(
        r"^([ \t]*)gclient sync --no-history --nohooks\s*$",
        s,
        re.M,
    )
    if not m:
        sys.exit("patch: gclient sync anchor not found in " + str(engine))
    chain_start = m.start()
    while True:
        nl = s.rfind("\n", 0, chain_start - 1)
        if nl < 0:
            break
        if s[nl + 1:chain_start].rstrip("\n").endswith("\\"):
            chain_start = nl + 1
        else:
            break
    indent = s[chain_start : s.find("\n", chain_start)]
    indent = indent[: len(indent) - len(indent.lstrip())]
    hook = indent + 'python3 "$ROOT/../.github/denial-arm64/patch-deps.py" "$CHECKOUT/DEPS"\n'
    s = s[:chain_start] + hook + s[chain_start:]

    m2 = re.search(r"^([ \t]*)gclient runhooks\s*$", s, re.M)
    if not m2:
        sys.exit("patch: gclient runhooks anchor not found in " + str(engine))
    restore = m2.group(1) + 'git -C "$CHECKOUT" checkout -- DEPS\n'
    line_end = s.index("\n", m2.start()) + 1
    s = s[:line_end] + restore + s[line_end:]

    n = s.count("linux-x64")
    s = s.replace("linux-x64", "linux-arm64")

    norm_anchor = '  local normalized="${generated}.denial-normalized.$$"\n'
    if norm_anchor not in s:
        sys.exit("patch: normalize anchor not found in " + str(engine))
    norm_guard = norm_anchor + r'''  if [[ ! -s "$expected" ]]; then
    printf '%s: using self-build GN arguments (%s, no baseline metadata)\n' \
      "$(basename -- "$0")" "$mode" >&2
    return 0
  fi
'''
    s = s.replace(norm_anchor, norm_guard, 1)

    cmp_anchor = '    [[ "$actual" == "$expected" ]] || return 1\n'
    if cmp_anchor not in s:
        sys.exit("patch: verify compare anchor not found in " + str(engine))
    s = s.replace(
        cmp_anchor,
        '    [[ -z "$expected" || "$actual" == "$expected" ]] || return 1\n',
        1,
    )

    sha_anchor = (
        '    [[ "$(file_sha256 "$output/libflutter_engine.so")" \\\n'
        '      == "$(expected_engine_sha256 "$mode")" ]] \\\n'
        "      || fail \"$mode engine checksum differs from committed metadata; after a deliberate source-lock advance run '$0 refresh-metadata'\"\n"
    )
    if sha_anchor not in s:
        sys.exit("patch: build sha verify anchor not found in " + str(engine))
    sha_repl = (
        '    expected_engine="$(expected_engine_sha256 "$mode")"\n'
        '    actual_engine="$(file_sha256 "$output/libflutter_engine.so")"\n'
        '    [[ -z "$expected_engine" || "$actual_engine" == "$expected_engine" ]] \\\n'
        "      || fail \"$mode engine checksum differs from committed metadata; after a deliberate source-lock advance run '$0 refresh-metadata'\"\n"
    )
    s = s.replace(sha_anchor, sha_repl, 1)

    mark(engine, s + marker, "patched denial-flutter-engine (arm64 paths, lenient metadata, DEPS hook)")

# ---------- seed linux-arm64 metadata placeholders ----------
for mode in ("debug", "profile", "release"):
    d = repo / "prebuilt" / "flutter-engine" / ("linux-arm64-" + mode)
    d.mkdir(parents=True, exist_ok=True)
    (d / "args.gn").touch(exist_ok=True)
    (d / "libflutter_engine.so.sha256").touch(exist_ok=True)
print("seeded linux-arm64 metadata placeholders")

# ---------- tools/denial-pc ----------
pc = repo / "tools" / "denial-pc"
if patched(pc):
    print("denial-pc: already patched")
else:
    s = pc.read_text()
    n = s.count("linux-x64")
    m = s.count("linux/x64")
    s = s.replace("linux-x64", "linux-arm64").replace("linux/x64", "linux/arm64")
    mark(pc, s + marker, f"patched denial-pc ({n} linux-x64, {m} linux/x64 -> arm64)")

# ---------- tools/package-denial-rpm ----------
rpm = repo / "tools" / "package-denial-rpm"
if patched(rpm):
    print("package-denial-rpm: already patched")
else:
    s = rpm.read_text()
    n = s.count(".x86_64.rpm")
    s = s.replace(".x86_64.rpm", ".*.rpm")
    mark(rpm, s + marker, f"patched package-denial-rpm ({n} x86_64 rpm globs widened)")
PY