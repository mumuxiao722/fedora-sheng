# fedora-sheng

[中文版](README_CN.md)

> **Project Status**  
> This project is still in its **early development stage**. Functionality may be incomplete and build results may contain unknown issues.  
> If you encounter any problems, please open an [Issue](https://github.com/mumuxiao722/fedora-sheng/issues).

---

## Overview

This project uses **GitHub Actions** to automatically build a Fedora root filesystem for the Xiaomi Pad 6S Pro (sheng), providing a flashable `rootfs.img` and `boot.img`.  
Simply start a workflow in your own repository and you will have a ready-to-use Fedora environment.

---

## Getting Started

### 1. Fork & Enable Actions

Click the **Fork** button at the top right to copy the repository to your GitHub account.

Navigate to the **Actions** tab of your forked repository.  
If Actions are disabled, click `I understand my workflows, go ahead and enable them`.

### 2. Run the Build Workflow

In the **Actions** page, select **"Build Fedora RootFS"** from the left sidebar, then click the **Run workflow** dropdown on the right.

You will see a list of configurable options (see [Advanced Configuration](#advanced-configuration) for details).  
If you leave everything unchanged, the build will proceed with the **default settings**.

Click the green **Run workflow** button to start the build.

### 3. Download Artifacts

Once the workflow finishes, open the summary page of that run.  
Under the **Artifacts** section, download `rootfs-*.zip` and `boot-*.zip` (GitHub Actions compresses the raw `.img` files into zip archives).

---

## Advanced Configuration

When you trigger the **Build Fedora RootFS** workflow via `workflow_dispatch`, the following inputs are available:

### General

| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| **Fedora Version** | Fedora version to install | `44` / `45` | `44` |
| **Enable Third-Party** | Enable third-party repositories | `true` / `false` | `false` |
| **Desktop** | Desktop environment to install | `GNOME` / `KDE Plasma` / `server` | `GNOME` |
| **GNOME Mobile** | Use GNOME Mobile instead of GNOME (only when Desktop=GNOME) | `true` / `false` | `false` |
| **Plasma Mobile** | Use Plasma Mobile shell instead of Plasma Desktop (only when Desktop=KDE Plasma) | `true` / `false` | `false` |
| **Enable COPR** | Enable COPR repository (required for GNOME Mobile) | `true` / `false` | `false` |
| **Quiet Boot** | Enable Plymouth splash screen and quiet boot messages | `true` / `false` | `true` |
| **Autologin** | Whether the created user should be logged in automatically | `true` / `false` | `true` |
| **Username** | Username for the non-root user | string | `username` |
| **Hostname** | System hostname | string | `xiaomi-sheng` |
| **System language** | System locale | `None (C.UTF-8)` / `en_US.UTF-8` / `zh_CN.UTF-8` / `zh_TW.UTF-8` / `ja_JP.UTF-8` / `ko_KR.UTF-8` / `de_DE.UTF-8` / `fr_FR.UTF-8` / `es_ES.UTF-8` / `ru_RU.UTF-8` | `None (C.UTF-8)` |
| **Boot mode** | Which partition Fedora boots from | `single (userdata)` / `dual (linux)` / `custom` | `dual (linux)` |
| **Custom partition** | Partition name (required when boot_mode=custom) | any partition name | *(empty)* |
| **Extra packages** | Extra packages to install (space-separated) | string | *(empty)* |

### Kernel

| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| **Kernel Source** | Use prebuilt kernel or build from source | `prebuilt` / `custom_build` | `prebuilt` |
| **Kernel Prebuilt Source** | Where to get the prebuilt kernel (only when prebuilt) | `upstream` / `own` | `upstream` |
| **Kernel Repo URL** | Git repo for kernel source (only when custom_build) | valid Git URL | `https://github.com/ianchb/sm8550-mainline` |
| **Kernel Branch** | Kernel branch name or release tag (custom_build: upstream branch to clone; prebuilt: release tag to download) | branch name / tag | `sheng-7.2.2` |
| **Kernel Config** | Config file path in repo (only when custom_build) | file path | `sm8550.config` |

### Firmware

| Parameter | Description | Options | Default |
|-----------|-------------|---------|---------|
| **Firmware Repo URL** | Git repository URL for device firmware files | valid Git URL | `https://github.com/ianchb/sheng-firmware` |
| **Firmware Branch** | Branch to checkout from the firmware repository | branch name | `master` |

> **Notes**  
> - To use a custom password, you **must** create a repository secret named `ROOTFS_PASSWORD` before running the workflow.  
> - If `ROOTFS_PASSWORD` is not set, the password will fall back to the insecure default: `password`.  
> - If you choose **Boot mode = `custom`**, you **must** fill in the **Custom partition** field.

---

## Custom Kernel Build

If you want to use a custom kernel instead of the prebuilt one:

### Option 1: Build from source via workflow

1. Set **Kernel Source** to `custom_build`
2. Fill in **Kernel Repo URL**, **Kernel Branch**, and **Kernel Config**
3. Run the workflow — it will compile the kernel and include it in the artifacts

### Option 2: Use your own prebuilt kernel RPM

1. Run a `custom_build` workflow to build the kernel
2. Download the `kernel-sheng.zip` artifact from the Actions run
3. Create a release with any tag name you like (e.g. `my-kernel-v1`)
4. Upload the `kernel-sheng.zip` to that release (file **must** be named `kernel-sheng.zip`)
5. Set **Kernel Source** to `prebuilt`, **Kernel Prebuilt Source** to `own`
6. Enter your tag name in **Kernel Branch**
7. Run the workflow — it will download the kernel RPM from your release

---

## Packages

| Package | Description |
|---------|-------------|
| [firmware-xiaomi-sheng](https://github.com/ianchb/sheng-firmware) | Device firmware blobs (WiFi, Bluetooth, DSP, etc.) |
| [sheng-devauth](https://github.com/ianchb/sheng_devauth) | Device authorization daemon |
| [xiaomi-mipps-auth](https://github.com/ianchb/xiaomi-mipps-auth) | MIPPS authentication for fast charging |
| [xiaomi-charger-mode](https://github.com/ianchb/xiaomi-charger-mode) | Charging screen when charger connected while device is off |
| [xiaomi-sheng-thp](https://github.com/ianchb/xiaomi-sheng-thp) | Touch data processing for finger and stylus |
| [xiaomi-pen-status](https://github.com/ianchb/xiaomi-pen-status) | Stylus connection/battery status display |
| [xiaomi-sheng-fingerprint](https://github.com/ianchb/xiaomi-sheng-fingerprint) | FPC1553 fingerprint sensor support (libfprint + fprintd) |
| [xiaomi-sheng-keyboard-helper](https://github.com/ianchb/xiaomi-sheng-keyboard-helper) | Keyboard microphone indicator and angle-based input control |
| [xiaomi-sheng-keyboard-backlight](https://github.com/slhssb/xiaomi-sheng-keyboard-backlight) | Keyboard backlight brightness control |
| [fastrpc](https://github.com/qualcomm/fastrpc) | Qualcomm FastRPC for DSP communication |
| [libssc](https://codeberg.org/DylanVanAssche/libssc) | Qualcomm Sensor Core userspace library |
| [iio-sensor-proxy](https://github.com/hadess/iio-sensor-proxy) | IIO sensor proxy daemon |
| [sheng-sensors](#) | Device-specific sensor configuration and udev rules |
| [alsa-xiaomi-sheng](#) | ALSA UCM2 audio configuration |

---

## Flashing to Your Device

### Prerequisites

- Device with an **unlocked bootloader**
- **TWRP** recovery installed
- `fastboot` properly set up on your computer

> **Warning**  
> The following steps modify device partitions and may brick your device or cause data loss. Back up your important data and make sure you understand each command.

### Partition Setup

1. **Dual boot (keep existing OS)**  
   Inside TWRP, use `parted` to shrink the `userdata` partition and create a new partition at the end, named e.g. `linux`.

2. **Single boot (replace OS completely)**  
   Use the `userdata` partition directly for Fedora (erasing all previous data).

### Flashing the Images

The commands below assume:
- You will boot Fedora using **slot B**
- The Fedora partition is named **linux**

```bash
# 1. Erase dtbo
fastboot erase dtbo_b

# 2. Flash the boot image
fastboot flash boot_b boot.img

# 3. Flash the root filesystem to the linux partition
fastboot flash linux rootfs.img

# 4. Reboot
fastboot reboot
```

After rebooting, the device should start from slot B and boot into Fedora.

---

## Credits

This project benefits from the following outstanding work and community support:

- **map220v** – for TWRP, the mainline kernel port and many device-specific adaptations that make Linux run on the Xiaomi Pad 6S Pro (sheng)
- **ianchb** – for maintaining the [debian-sheng](https://github.com/ianchb/debian-sheng) project, userspace drivers and various device-specific packages, from which this project is derived
- **slhssb** – for the keyboard backlight driver (xiaomi-sheng-keyboard-backlight)

---

## Related Projects

- [debian-sheng](https://github.com/ianchb/debian-sheng) - Debian version for Xiaomi Pad 6S Pro
- [sm8550-mainline](https://github.com/ianchb/sm8550-mainline) - Mainline kernel for SM8550
- [sheng-firmware](https://github.com/ianchb/sheng-firmware) - Device firmware files
