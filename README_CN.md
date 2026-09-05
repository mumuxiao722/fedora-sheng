# fedora-sheng

[English](README.md)

> **项目状态**  
> 本项目仍处于**早期开发阶段**，功能可能不完整，构建结果可能存在未知问题。  
> 如果遇到任何问题，请提交 [Issue](https://github.com/mumuxiao722/fedora-sheng/issues)。

---

## 项目概述

本项目使用 **GitHub Actions** 自动构建适用于小米平板 6S Pro (sheng) 的 Fedora 根文件系统，提供可刷入的 `rootfs.img.zip` 和 `boot.img.zip`。  
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
在 **Artifacts** 部分，下载 `rootfs-*.zip` 和 `boot-*.zip`。

---

## 高级配置

当您通过 `workflow_dispatch` 触发 **Build Fedora RootFS** 工作流时，可以使用以下输入参数：

### 通用设置

| 参数 | 说明 | 选项 | 默认值 |
|------|------|------|--------|
| **Fedora Version** | 要安装的 Fedora 版本 | `44` / `45` | `44` |
| **Autologin** | 创建的用户是否自动登录 | `true` / `false` | `true` |
| **Username** | 非 root 用户的用户名 | 字符串 | `username` |
| **Hostname** | 系统主机名 | 字符串 | `xiaomi-sheng` |
| **System language** | 系统语言环境 | `None (C.UTF-8)` / `en_US.UTF-8` / `zh_CN.UTF-8` / `zh_TW.UTF-8` / `ja_JP.UTF-8` / `ko_KR.UTF-8` / `de_DE.UTF-8` / `fr_FR.UTF-8` / `es_ES.UTF-8` / `ru_RU.UTF-8` | `None (C.UTF-8)` |
| **Boot mode** | Fedora 从哪个分区启动 | `single (userdata)` / `dual (linux)` / `custom` | `dual (linux)` |
| **Custom partition** | 分区名称（boot_mode=custom 时必填） | 任意分区名称 | *（空）* |
| **Extra packages** | 额外安装的软件包（空格分隔） | 字符串 | *（空）* |

### 内核设置

| 参数 | 说明 | 选项 | 默认值 |
|------|------|------|--------|
| **Kernel Source** | 使用预构建内核还是从源码构建 | `prebuilt` / `custom_build` | `prebuilt` |
| **Kernel Prebuilt Source** | 预构建内核来源（仅 prebuilt 时） | `upstream` / `own` | `upstream` |
| **Kernel Repo URL** | 内核源码仓库地址（仅 custom_build 时） | 有效的 Git URL | `https://github.com/ianchb/sm8550-mainline` |
| **Kernel Branch** | 内核分支名或 release tag（custom_build: 上游分支名；prebuilt: 要下载的 release tag） | 分支名 / tag | `sheng-7.2.2` |
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
2. 从 Actions 运行结果中下载 `kernel-sheng-*.rpm` artifact
3. 创建一个 release，tag 名称自定（如 `my-kernel-v1`）
4. 上传 `kernel-sheng-*.rpm` 到该 release
5. 将 **Kernel Source** 设为 `prebuilt`，**Kernel Prebuilt Source** 设为 `own`
6. 在 **Kernel Branch** 中填入你的 tag 名称
7. 运行工作流 — 它将从 release 下载内核 RPM

### 上传内核 RPM 到 release（手动）

`custom_build` 工作流运行后，内核 RPM 作为 workflow artifact 可用：

1. 进入 Actions → 选择 `custom_build` 运行
2. 在 **Artifacts** 中下载 `kernel-sheng.zip`
3. 解压得到 `kernel-sheng-*.rpm`
4. 创建一个 release，tag 名称自定（如 `my-kernel-v1`）
5. 上传 RPM 文件到该 release

之后构建 rootfs 时，将 **Kernel Prebuilt Source** 设为 `own`，并在 **Kernel Branch** 中填入 tag 名称。

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

## 致谢

本项目得益于以下优秀工作：

- **map220v** – TWRP、主线内核移植以及使 Linux 能够在小米平板 6S Pro (sheng) 上运行的众多设备特定适配
- **ianchb** – 维护 [debian-sheng](https://github.com/ianchb/debian-sheng) 项目、用户态驱动以及各种设备特定软件包，本项目基于此衍生
- **slhssb** – 键盘背光驱动（xiaomi-sheng-keyboard-backlight）

---

## 相关项目

- [debian-sheng](https://github.com/ianchb/debian-sheng) - 小米平板 6S Pro 的 Debian 版本
- [sm8550-mainline](https://github.com/ianchb/sm8550-mainline) - SM8550 主线内核
- [sheng-firmware](https://github.com/ianchb/sheng-firmware) - 设备固件文件
