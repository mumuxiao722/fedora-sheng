# fedora-sheng

[English](README.md)

> **项目状态**  
> 本项目仍处于**早期开发阶段**，功能可能不完整，构建结果可能存在未知问题。  
> 如果遇到任何问题，请提交 [Issue](https://github.com/mumuxiao722/fedora-sheng/issues)。

---

## 项目概述

本项目使用 **GitHub Actions** 自动构建适用于小米平板 6S Pro (sheng) 的 Fedora 根文件系统，提供可刷入的 `rootfs.img` 和 `boot.img`。  
只需在您自己的仓库中启动工作流，即可获得一个开箱即用的 Fedora 环境。

---

## 快速开始

### 1. Fork 并启用 Actions

点击右上角的 **Fork** 按钮，将仓库复制到您的 GitHub 账户。

导航到您 Fork 后仓库的 **Actions** 选项卡。  
如果 Actions 被禁用，请点击 `I understand my workflows, go ahead and enable them`。

### 2. 运行构建工作流

在 **Actions** 页面，从左侧选择 **"Build Fedora RootFS"**，然后点击右侧的 **Run workflow** 下拉菜单。

您将看到一系列可配置选项（详见 [高级配置](#高级配置)）。  
如果保持所有设置不变，构建将使用**默认设置**进行。

点击绿色的 **Run workflow** 按钮开始构建。

### 3. 下载产物

工作流完成后，打开该运行的摘要页面。  
在 **Artifacts** 部分，下载 `rootfs-*.zip` 和 `boot-*.zip`（GitHub Actions 会将原始 `.img` 文件压缩为 zip 归档）。

---

## 高级配置

当您通过 `workflow_dispatch` 触发 **Build Fedora RootFS** 工作流时，可以使用以下输入参数：

### 通用设置

| 参数 | 说明 | 选项 | 默认值 |
|------|------|------|--------|
| **Fedora Version** | 要安装的 Fedora 版本 | `43` / `44` / `45` / `rawhide` | `45` |
| **Enable Third-Party** | 启用第三方仓库 | `true` / `false` | `false` |
| **Desktop** | 要安装的桌面环境 | `GNOME` / `KDE Plasma` / `Denial` / `server` | `GNOME` |
| **GNOME Mobile** | 使用 @mobility/gnome-mobile COPR 的 GNOME Mobile（需要启用 Enable Third-Party）。各 Fedora 版本的包可用性不同——详见下方**严重警告**，构建前请查看 [COPR Monitor](https://copr.fedorainfracloud.org/coprs/g/mobility/gnome-mobile/monitor/)。 | `true` / `false` | `false` |
| **Plasma Mobile** | 使用 Plasma Mobile 界面而非 Plasma Desktop（仅 Desktop=KDE Plasma 时有效）。仅 Fedora 43 确认可用，fc44/45/rawhide 上崩溃。已将 SDDM 替换为 plasma-login-manager，可能解决此问题但未测试。 | `true` / `false` | `false` |
| **Denial: Mobile mode** | Denial：使用 Mobile 模式（类似 Android 平板的 UI）而非 Desktop 模式（无屏幕键盘）（仅 Desktop=Denial 时有效）。 | `true` / `false` | `true` |
| **Denial: 插件管理器** | 一并安装 Denial 的插件管理器与插件构建工具（仅 Desktop=Denial 时有效）。增加约 82 MB，本镜像未对其做过其他验证。 | `true` / `false` | `false` |
| **Quiet Boot** | 启用 Plymouth 启动画面和安静启动信息 | `true` / `false` | `true` |
| **Autologin** | 创建的用户是否自动登录 | `true` / `false` | `true` |
| **Username** | 非 root 用户的用户名 | 字符串 | `username` |
| **Hostname** | 系统主机名 | 字符串 | `xiaomi-sheng` |
| **System language** | 系统语言环境 | `None (C.UTF-8)` / `en_US.UTF-8` / `zh_CN.UTF-8` / `zh_TW.UTF-8` / `ja_JP.UTF-8` / `ko_KR.UTF-8` / `de_DE.UTF-8` / `fr_FR.UTF-8` / `es_ES.UTF-8` / `ru_RU.UTF-8` | `None (C.UTF-8)` |
| **Boot mode** | Fedora 从哪个分区启动 | `single (userdata)` / `dual (linux)` / `custom` | `dual (linux)` |
| **Custom partition** | 分区名称（boot_mode=custom 时必填） | 任意分区名称 | *（空）* |
| **Extra packages** | 额外安装的软件包（空格分隔） | 字符串 | *（空）* |

> **🚫 严重警告**
> 
> - **Fedora 43**：gsd-mobile 49 已从 COPR **过期**，且最新的 mutter 构筑**失败**。仓库中仍是 gsd=51~beta 搭配 mutter+shell=49^mobile（2026-03 构建），因此在 fc43 上选择 GNOME Mobile 会得到**混合构建**。这种版本不匹配**可能导致运行时问题或不稳定**。使用风险自负。
> - **Fedora 44**：仅发布了 gnome-settings-daemon（51~beta）；gnome-shell 与 mutter **缺失**（最新 mutter 构筑失败，gnome-shell 构筑 forked）。GNOME Mobile 无法组装，构建会**回退到原版 Fedora GNOME**。**本项目不负责** fc44 构建后发现不是 GNOME Mobile 的情况。
> - **Fedora 45 / rawhide**：完整移动套件——gnome-shell、mutter、gnome-settings-daemon **51.1.mobile.3**（2026-10-20 构建）——在 aarch64 与 x86_64 上均可用。
> - **如果不确定**，请先查看 [COPR Monitor](https://copr.fedorainfracloud.org/coprs/g/mobility/gnome-mobile/monitor/) 确认包是否可用。
> 
> **截至 2026 年 10 月，Fedora 45 与 rawhide 完全支持 GNOME Mobile。**

### 内核设置

| 参数 | 说明 | 选项 | 默认值 |
|------|------|------|--------|
| **Kernel Source** | 使用预构建内核还是从源码构建 | `prebuilt` / `custom_build` | `prebuilt` |
| **Kernel Prebuilt Source** | 预构建内核来源（仅 prebuilt 时） | `upstream` / `own` | `upstream` |
| **Kernel Repo URL** | 内核源码仓库地址（仅 custom_build 时） | 有效的 Git URL | `https://github.com/ianchb/sm8550-mainline` |
| **Kernel Branch** | 内核分支名或 release tag（custom_build: 上游分支名；prebuilt: 要下载的 release tag） | 分支名 / tag | `sheng-7.3.0` |
| **Kernel Config** | 仓库中的配置文件路径（仅 custom_build 时） | 文件路径 | `sm8550.config` |

### 固件设置

| 参数 | 说明 | 选项 | 默认值 |
|------|------|------|--------|
| **Firmware Repo URL** | 设备固件文件的 Git 仓库 URL | 有效的 Git URL | `https://github.com/ianchb/sheng-firmware` |
| **Firmware Branch** | 从固件仓库检出的分支 | 分支名称 | `master` |

> **注意**  
> - 要使用自定义密码，您**必须**在运行工作流之前创建名为 `ROOTFS_PASSWORD` 的仓库密钥。  
> - 如果未设置 `ROOTFS_PASSWORD`，密码将使用不安全的默认值：`password`。  
> - 如果选择 **Boot mode = `custom`**，您**必须**填写 **Custom partition** 字段。  

---

## 自定义内核构建

如果您想使用自定义内核而非预构建内核：

### 方式一：通过工作流从源码构建

1. 将 **Kernel Source** 设为 `custom_build`
2. 填写 **Kernel Repo URL**、**Kernel Branch** 和 **Kernel Config**
3. 运行工作流 — 它将编译内核并包含在产物中

### 方式二：使用自己的预构建内核 RPM

1. 运行 `custom_build` 工作流编译内核
2. 从 Actions 运行结果中下载 `kernel-sheng.zip` artifact
3. 创建一个 release，tag 名称自定（如 `my-kernel-v1`）
4. 上传 `kernel-sheng.zip` 到该 release（文件**必须**命名为 `kernel-sheng.zip`）
5. 将 **Kernel Source** 设为 `prebuilt`，**Kernel Prebuilt Source** 设为 `own`
6. 在 **Kernel Branch** 中填入你的 tag 名称
7. 运行工作流 — 它将从 release 下载内核 RPM

---

## 软件包

| 软件包 | 说明 |
|--------|------|
| [firmware-xiaomi-sheng](https://github.com/ianchb/sheng-firmware) | 设备固件（WiFi、蓝牙、DSP等） |
| [sheng-devauth](https://github.com/ianchb/sheng_devauth) | 设备认证守护进程 |
| [xiaomi-mipps-auth](https://github.com/ianchb/xiaomi-mipps-auth) | MIPPS 快充认证 |
| [xiaomi-charger-mode](https://github.com/ianchb/xiaomi-charger-mode) | 关机充电显示 |
| [xiaomi-sheng-thp](https://github.com/ianchb/xiaomi-sheng-thp) | 触摸数据处理（手指和手写笔） |
| [xiaomi-pen-status](https://github.com/ianchb/xiaomi-pen-status) | 手写笔连接/电池状态显示 |
| [xiaomi-sheng-fingerprint](https://github.com/ianchb/xiaomi-sheng-fingerprint) | FPC1553 指纹传感器支持 |
| [xiaomi-sheng-keyboard-helper](https://github.com/ianchb/xiaomi-sheng-keyboard-helper) | 键盘麦克风指示灯和角度控制 |
| [xiaomi-sheng-keyboard-backlight](https://github.com/slhssb/xiaomi-sheng-keyboard-backlight) | 键盘背光亮度控制 |
| [fastrpc](https://github.com/qualcomm/fastrpc) | Qualcomm FastRPC（DSP 通信） |
| [libssc](https://codeberg.org/DylanVanAssche/libssc) | Qualcomm Sensor Core 用户空间库 |
| [iio-sensor-proxy](https://github.com/hadess/iio-sensor-proxy) | IIO 传感器代理守护进程 |
| [sheng-gnome-fix](https://github.com/mumuxiao722/sheng-gnome-fix) | GNOME 自动旋转、电源键息屏锁屏、系统级禁用挂起 |
| [Denial](https://github.com/denialwm/denial) | Flutter-native Wayland 合成器（AArch64 RPM 取自[上游 release](https://github.com/denialwm/denial/releases)） |
| [sheng-sensors](#) | 设备特定传感器配置和 udev 规则 |
| [alsa-xiaomi-sheng](#) | ALSA UCM2 音频配置 |

---

## 刷入设备

### 前提条件

- 设备已**解锁 bootloader**
- 已安装 **TWRP** 恢复模式
- 计算机已正确设置 `fastboot`

> **警告**  
> 以下步骤会修改设备分区，可能导致设备变砖或数据丢失。请备份重要数据并确保您理解每个命令。

### 分区设置

1. **双启动（保留现有系统）**  
   在 TWRP 中，使用 `parted` 缩小 `userdata` 分区并在末尾创建新分区，例如命名为 `linux`。

2. **单启动（完全替换系统）**  
   直接使用 `userdata` 分区安装 Fedora（将擦除所有先前数据）。

### 刷入镜像

以下命令假设：
- 您将使用 **slot B** 启动 Fedora
- Fedora 分区命名为 **linux**

```bash
# 1. 擦除 dtbo
fastboot erase dtbo_b

# 2. 刷入 boot 镜像
fastboot flash boot_b boot.img

# 3. 将根文件系统刷入 linux 分区
fastboot flash linux rootfs.img

# 4. 重启
fastboot reboot
```

重启后，设备应从 slot B 启动并进入 Fedora。

---

## 已知问题

1. **开机后传感器方向可能变为 undefined，几分钟内会恢复** – 开机后几分钟内加速度计方向可能显示为 undefined，导致无法自动旋转，之后会自动恢复为 normal。

### GNOME Mobile

1. **各 Fedora 版本的包状态不同** – 详见 [Advanced Configuration](#advanced-configuration) 下方的**严重警告**，构建前请查看 [COPR Monitor](https://copr.fedorainfracloud.org/coprs/g/mobility/gnome-mobile/monitor/)。截至 2026 年 10 月，Fedora 45 与 rawhide 完全支持，Fedora 43 与 44 不支持。
2. **随机崩溃回到 GDM** – GNOME Mobile 可能会随机崩溃并返回 GDM 登录界面。这是上游问题，在 Debian 上也可复现。
3. **GDM 密码输入框不可见** – GDM 登录界面的密码输入框可能显示为空白，但实际可以输入。这也是上游问题，在 Debian 上同样存在。

### KDE Plasma Mobile

1. **Plasma Mobile 在 Fedora 44、45 和 rawhide 上崩溃** – 桌面启动时崩溃。仅 **Fedora 43** 确认可用。
2. **部分移动 UI 仍可访问** – 即使桌面崩溃，部分移动 shell 组件仍可正常工作：首次启动引导、锁屏密码输入、以及电源菜单（关机/重启/注销）。
3. 我已将 SDDM 替换为 `plasma-login-manager`（SDDM 在 Fedora 上已弃用）。这**可能**解决 Plasma Mobile 崩溃的问题，但我**尚未测试**。欢迎反馈。

---

## 致谢

本项目得益于以下优秀工作：

- **[map220v](https://github.com/map220v)** – TWRP、主线内核移植以及使 Linux 能够在小米平板 6S Pro (sheng) 上运行的众多设备特定适配
- **[ianchb](https://github.com/ianchb)** – 维护 [debian-sheng](https://github.com/ianchb/debian-sheng) 项目、用户态驱动以及各种设备特定软件包，本项目基于此衍生
- **[alghiffaryfa19](https://github.com/alghiffaryfa19)** – Qualcomm 传感器配置文件（sheng-sensors-file）
- **[slhssb](https://github.com/slhssb)** – 键盘背光驱动（xiaomi-sheng-keyboard-backlight）
- **[GhfunNiHe](https://github.com/GhfunNiHe)** – 自动分区扩容（growfs）实现，取自 [debian-sheng](https://github.com/ianchb/debian-sheng)
- **[code002-2](https://github.com/code002-2)** – WiFi 固件警告参考
- **[DotRedstone](https://github.com/DotRedstone)** – 提供 [nixos-sheng](https://github.com/DotRedstone/nixos-sheng) 项目，其 `fake-tablet-mode` 的合盖/开盖息屏处理、`sheng-power-key-display-toggle` 服务及 `docs/hall-sensor-rotation.md` 调试记录，是 [`sheng-gnome-fix`](https://github.com/mumuxiao722/sheng-gnome-fix) 软件包中合盖/电源键处理的基础
- **[CFM880](https://github.com/CFM880)** – 提供 [nabu-accelerometer](https://github.com/CFM880/nabu-accelerometer)，其 `userspace/nabu-tablet-mode.c`（GPL-2.0-only）是 `sheng-gnome-fix` 新 tablet-mode 核心的移植来源

---

## 相关项目

- [debian-sheng](https://github.com/ianchb/debian-sheng) - 小米平板 6S Pro 的 Debian 版本
- [sm8550-mainline](https://github.com/ianchb/sm8550-mainline) - SM8550 主线内核
- [sheng-firmware](https://github.com/ianchb/sheng-firmware) - 设备固件文件
