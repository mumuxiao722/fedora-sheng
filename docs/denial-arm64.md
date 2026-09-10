# Denial ARM64 自建备忘

状态跟踪文件：记录把 Denial 在 ARM64 上从源码构建出来的全部已知障碍、本地修复与上游沟通。

> 更新时间：2026-09-10（upstream dev 回复后）

## 锁定版本

- Denial 仓库固定 tag **v0.3.1**（为确定性，不再用 main/dev 分支）。
- 引擎源锁 `prebuilt/flutter-engine/SOURCE_LOCK.json`：
  - flutter fork `denialwm/flutter` 分支 `denial/3.44.7-r1`，revision `d728e61e7d835e02c453c70ae9523a40f6c03215`（upstream `84fc5cbb…`）
  - skia fork `denialwm/skia` revision `0ee042f542b3e79f5ac49115387718c6bb3d7d34`
- CI：`.github/workflows/rootfs.yml` → `build-denial` job（ubuntu-24.04-arm，首次慢、缓存 key `denial-build-v0.3.1`）。

## 三堵墙（当前已知）

### 墙 1：openjdk linux-arm64 CIPD 不存在

- 现象：`gclient sync` → `cipd ensure` 报
  `failed to resolve flutter/java/openjdk/linux-arm64@version:21 (line 35): no such package`
- 根因：锁定的 flutter DEPS 第 627 行 `'engine/src/flutter/third_party/java/openjdk'` 的无条件 cipd 依赖
  `flutter/java/openjdk/${{platform}}@version:21`，上游从未发布 `linux-arm64` 变体（只有 linux-amd64）。
- 上游真实情况：`flavor` 无 arm64，CI 只跑 x64；dev 确认 tools x64-only。

### 墙 2：fuchsia hook 需要 x64 host 二进制

- 现象：跨过墙 1 后 `gclient runhooks` 的 `Generate Fuchsia GN build rules`
  （`engine/src/flutter/tools/fuchsia/test_scripts/gen_build_defs.py`）执行
  `buildtools/linux-x64/clang/bin/llvm-readelf -n` → `OSError: [Errno 8] Exec format error`。
- 根因：DEPS 伞开关 `'download_fuchsia_deps': 'host_os == "linux"'`（第 111 行）在 Linux 无条件开启，
  拉 fuchsia SDK/gn-sdk/test-scripts，且 hook 无 amd64/arm64 区分。

### 墙 3：`tools/denial-flutter-engine` 硬编码 linux-x64 元数据（架构级锁）

- `tools/denial-flutter-engine`（v0.3.1，blob `b91179f8…`）：
  - `cache_key()`：`target=linux-x64`（约 285 行）
  - `normalize_generated_args()`：对比 `prebuilt/flutter-engine/linux-x64-$mode/args.gn` 字节一致（约 204/292/658 行）——ARM64 生成 args.gn 含 `target_cpu="arm64"` 必不匹配
  - `expected_engine_sha256()`：对照 `linux-x64-$mode/libflutter_engine.so.sha256`（约 182-185/295 行）
  - `build_artifacts()`/`refresh_metadata()`：`buildtools/linux-x64`、`linux-x64-$mode/…` 路径（约 350/639/754/808-814 行）
- 结论：即便绕过墙 1、2，工具在 ARM64 宿主也会在上述任一校验失败——真正的架构支持需要上游改动。

## 上游反馈（2026-09-10，denialwm dev @doctorlogix）

> cross-building is not yet automated by tools/denial-pc (currently x64-only).
> 手动步骤：
> 1. 提供含 EGL/GBM、libinput、libseat、udev、libxkbcommon、Fontconfig dev 库的 AArch64 sysroot；
> 2. `flutter engine` 用 `--linux --linux-cpu=arm64` 构建；
> 3. 组装 shell：`release_bundle_linux-arm64_assets`；
> 4. 合成器：`cargo build --release --target aarch64-unknown-linux-gnu`。
> “I will integrate this into Denial build tools soon.”
>
> 性能参考：dev 在 Snapdragon 8 Gen 2 1264x2780@120hz + kernel 7.1.4（Arch）跑 Denial，负载很轻。

即：x64-only 属实；正式 arm64 支持靠 upstream 整合（等待），我们本地用补丁先跑通现有版本。

## 本地修复（本仓库）

`build-denial` job 先 `Checkout Repo`（workspace 根），随后对工具的 checkout 打确定性补丁：

- `.github/denial-arm64/patch-deps.py`：对 `$CHECKOUT/DEPS` 做两处精确替换
  - 删除 `engine/src/flutter/third_party/java/openjdk` cipd 块（破墙 1）
  - `download_fuchsia_deps` 置 `False`（破墙 2）
- `.github/denial-arm64/patch-denial-flutter-engine.sh`：在 `gclient sync --no-history --nohooks` 前注入
  `python3 "$ROOT/../.github/denial-arm64/patch-deps.py" "$CHECKOUT/DEPS"`（幂等，锚点丢失即失败）

预期下一步失败点：墙 3（`normalize_generated_args` 或 `expected_engine_sha256`），届时以该日志作为上游 issue 的架构锁证据。

## 待办 / 沟通

- [ ] 跑 `desktop=Denial` workflow，验证补丁后能跨过墙 1、2
- [ ] 收集墙 3 失败日志
- [ ] 提 denialwm/denial issue：#openjdk linux-arm64 CIPD 缺失、fuchsia hook x64 依赖、工具 x64 元数据锁（附本 memo 与日志）
- [ ] 跟进 dev“整合进工具”的进展；上游落地 arm64 后：更新 README 去“暂无 ARM64 二进制”措辞、可考虑切回分支/新 tag、移除本补丁