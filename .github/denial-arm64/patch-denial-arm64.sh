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
    restore = m2.group(1) + 'git -C "$CHECKOUT" show HEAD:DEPS > "$CHECKOUT/DEPS"\n'
    line_end = s.index("\n", m2.start()) + 1
    s = s[:line_end] + restore + s[line_end:]

    def add_native_arg(host):
        out = []
        pat = re.compile(r"^([ \t]*)\./flutter/tools/gn \\$", re.M)
        pos = 0
        for m in pat.finditer(host):
            out.append(host[pos:m.start()])
            indent = m.group(1)
            out.append(indent + "./flutter/tools/gn \\\n")
            out.append(indent + "--linux \\\n")
            out.append(indent + "--linux-cpu=arm64 \\\n")
            pos = m.end() + 1
        out.append(host[pos:])
        return "".join(out)

    s = add_native_arg(s)
    assert s.count("./flutter/tools/gn \\") == 5

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
    (d / "ENGINE_REVISION").touch(exist_ok=True)
    (d / "FLUTTER_REVISION").touch(exist_ok=True)
    src = repo / "prebuilt" / "flutter-engine" / "linux-x64-release"
    for name in ("BUILD_INFO.md", "LICENSE.flutter", "LICENSE.third_party"):
        (d / name).write_bytes((src / name).read_bytes())
print("seeded linux-arm64 metadata placeholders (docs/licenses copied, pins empty)")

# ---------- tools/denial-pc ----------
pc = repo / "tools" / "denial-pc"
if patched(pc):
    print("denial-pc: already patched")
else:
    s = pc.read_text()
    n = s.count("linux-x64")
    m = s.count("linux/x64")
    s = s.replace("linux-x64", "linux-arm64").replace("linux/x64", "linux/arm64")

    checks = [
        (
            "prebuilt_engine_sha256() {\n"
            "    require_file \"$PREBUILT_ENGINE_SHA256\"\n"
            "    cut -d' ' -f1 < \"$PREBUILT_ENGINE_SHA256\"\n"
            "}\n",
            "prebuilt_engine_sha256() {\n"
            "    [[ -s \"$PREBUILT_ENGINE_SHA256\" ]] || return 0\n"
            "    cut -d' ' -f1 < \"$PREBUILT_ENGINE_SHA256\"\n"
            "}\n",
            "prebuilt_engine_sha256 lenient on empty baseline",
        ),
        (
            "    [[ \"$(file_sha256 \"$PREBUILT_ENGINE\")\" == \"$(prebuilt_engine_sha256)\" ]] \\\n"
            "        || die \"locally built Flutter engine does not match $PREBUILT_ENGINE_SHA256; rebuild or investigate it (see $PREBUILT_ENGINE_DIR/BUILD_INFO.md)\"\n",
            "    local expected_prebuilt\n"
            "    expected_prebuilt=\"$(prebuilt_engine_sha256)\"\n"
            "    [[ -z \"$expected_prebuilt\" ]] && return 0\n"
            "    [[ \"$(file_sha256 \"$PREBUILT_ENGINE\")\" == \"$expected_prebuilt\" ]] \\\n"
            "        || die \"locally built Flutter engine does not match $PREBUILT_ENGINE_SHA256; rebuild or investigate it (see $PREBUILT_ENGINE_DIR/BUILD_INFO.md)\"\n",
            "verify_prebuilt_engine lenient on empty baseline",
        ),
        (
            "        label=\"pinned build\"\n"
            "    fi\n"
            "    [[ \"$expected\" =~ ^[0-9a-f]{64}$ ]] \\\n"
            "        || die \"invalid expected SHA-256 for $label\"\n",
            "        label=\"pinned build\"\n"
            "    fi\n"
            "    [[ -z \"$expected\" ]] && return 0\n"
            "    [[ \"$expected\" =~ ^[0-9a-f]{64}$ ]] \\\n"
            "        || die \"invalid expected SHA-256 for $label\"\n",
            "require_pinned_engine lenient on empty baseline",
        ),
        (
            "require_flutter_bindings() {\n"
            "    require_file \"$PREBUILT_ENGINE_REVISION\"\n"
            "    require_file \"$PREBUILT_FLUTTER_REVISION\"\n"
            "    require_file \"$EMBEDDER_BINDINGS\"\n",
            "require_flutter_bindings() {\n"
            "    if [[ ! -s \"$PREBUILT_ENGINE_REVISION\" \\\n"
            "        || ! -s \"$PREBUILT_FLUTTER_REVISION\" ]]; then\n"
            "        require_file \"$EMBEDDER_BINDINGS\"\n"
            "        printf '%s: self-built engine without pinned revisions (skipping revision match)\\n' \\\n"
            "          \"$(basename -- \"$0\")\" >&2\n"
            "        return 0\n"
            "    fi\n"
            "    require_file \"$PREBUILT_ENGINE_REVISION\"\n"
            "    require_file \"$PREBUILT_FLUTTER_REVISION\"\n"
            "    require_file \"$EMBEDDER_BINDINGS\"\n",
            "require_flutter_bindings lenient on missing pinned revisions",
        ),
    ]
    for old, new, note in checks:
        if old not in s:
            sys.exit(f"patch: denial-pc anchor not found: {note}")
        s = s.replace(old, new, 1)
    mark(pc, s + marker, f"patched denial-pc (arch paths, {len(checks)} lenient engine checks)")

# ---------- tools/stage-denial-runtime ----------
stage = repo / "tools" / "stage-denial-runtime"
if patched(stage):
    print("stage-denial-runtime: already patched")
else:
    s = stage.read_text()

    root_anchor = 'ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"\n'
    if root_anchor not in s:
        sys.exit("patch: stage-denial-runtime ROOT anchor not found")
    host_cpu = (
        'HOST_CPU="${DENIAL_HOST_CPU:-}"\n'
        'case "${HOST_CPU:-$(uname -m)}" in\n'
        "  aarch64|arm64) HOST_CPU=arm64 ;;\n"
        "  x86_64|amd64) HOST_CPU=x64 ;;\n"
        "  *)\n"
        '    printf \'stage-denial-runtime: unsupported host CPU: %s\\n\' "${HOST_CPU:-$(uname -m)}" >&2\n'
        "    exit 1\n"
        "    ;;\n"
        "esac\n"
    )
    s = s.replace(root_anchor, root_anchor + host_cpu, 1)

    settings_anchor = (
        'SETTINGS_BUNDLE="${DENIAL_PC_SETTINGS_BUNDLE:-$ROOT/settings_app/build/linux/x64/release/bundle}"\n'
    )
    if settings_anchor not in s:
        sys.exit("patch: stage-denial-runtime SETTINGS_BUNDLE anchor not found")
    s = s.replace(
        settings_anchor,
        'SETTINGS_BUNDLE="${DENIAL_PC_SETTINGS_BUNDLE:-$ROOT/settings_app/build/linux/${HOST_CPU}/release/bundle}"\n',
        1,
    )

    engine_anchor = 'engine_source_root="$ROOT/prebuilt/flutter-engine/linux-x64-release"\n'
    if engine_anchor not in s:
        sys.exit("patch: stage-denial-runtime engine_source_root anchor not found")
    s = s.replace(
        engine_anchor,
        'engine_source_root="$ROOT/prebuilt/flutter-engine/linux-${HOST_CPU}-release"\n',
        1,
    )

    sha_anchor = (
        'expected_engine_sha256="$(cut -d\' \' -f1 < "$engine_source_root/libflutter_engine.so.sha256")"\n'
        'actual_engine_sha256="$(sha256sum "$BUNDLE/lib/libflutter_engine.so" | cut -d\' \' -f1)"\n'
        '[[ "$actual_engine_sha256" == "$expected_engine_sha256" ]] \\\n'
        '  || die "Flutter Engine SHA-256 is $actual_engine_sha256, expected $expected_engine_sha256"\n'
    )
    if sha_anchor not in s:
        sys.exit("patch: stage-denial-runtime engine sha anchor not found")
    sha_repl = (
        'expected_engine_sha256="$(cut -d\' \' -f1 < "$engine_source_root/libflutter_engine.so.sha256")"\n'
        'actual_engine_sha256="$(sha256sum "$BUNDLE/lib/libflutter_engine.so" | cut -d\' \' -f1)"\n'
        'if [[ -n "$expected_engine_sha256" ]]; then\n'
        '  [[ "$actual_engine_sha256" == "$expected_engine_sha256" ]] \\\n'
        '    || die "Flutter Engine SHA-256 is $actual_engine_sha256, expected $expected_engine_sha256"\n'
        "fi\n"
    )
    s = s.replace(sha_anchor, sha_repl, 1)
    mark(stage, s + marker, "patched stage-denial-runtime (host-cpu paths, lenient engine sha)")

# ---------- tools/package-denial-rpm ----------
rpm = repo / "tools" / "package-denial-rpm"
if patched(rpm):
    print("package-denial-rpm: already patched")
else:
    s = rpm.read_text()
    n = s.count(".x86_64.rpm")
    s = s.replace(".x86_64.rpm", ".*.rpm")
    mark(rpm, s + marker, f"patched package-denial-rpm ({n} x86_64 rpm globs widened)")

# ---------- packaging/fedora/denial.spec ----------
spec = repo / "packaging" / "fedora" / "denial.spec"
if patched(spec):
    print("denial.spec: already patched")
else:
    s = spec.read_text()
    anchor = "ExclusiveArch:  x86_64\n"
    if anchor not in s:
        sys.exit("patch: denial.spec ExclusiveArch anchor not found")
    s = s.replace(anchor, "ExclusiveArch:  x86_64 aarch64\n", 1)
    mark(spec, s + marker, "patched denial.spec (ExclusiveArch includes aarch64)")

# ---------- tools/verify-denial-native-package-metadata ----------
verify = repo / "tools" / "verify-denial-native-package-metadata"
if patched(verify):
    print("verify-denial-native-package-metadata: already patched")
else:
    s = verify.read_text()
    anchor = '  [[ "$package_arch" == x86_64 ]] \\\n'
    if anchor not in s:
        sys.exit("patch: verify-denial-native-package-metadata arch anchor not found")
    s = s.replace(
        anchor,
        '  [[ "$package_arch" == x86_64 || "$package_arch" == aarch64 ]] \\\n',
        1,
    )
    mark(verify, s + marker, "patched verify-denial-native-package-metadata (accepts aarch64 rpm arch)")
PY