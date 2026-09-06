#!/bin/bash
# Copyright (C) 2026 mumuxiao722 <zy349931@163.com>
# Licensed under the GPL-3.0-or-later. See LICENSE for details.
set -e

FEDORA_VERSION="${1:-44}"
FIRMWARE_REPO="${FIRMWARE_REPO:-https://github.com/ianchb/sheng-firmware}"
FIRMWARE_BRANCH="${FIRMWARE_BRANCH:-master}"

echo "=== Building RPMs in Fedora ${FEDORA_VERSION} ==="
echo "  Firmware: ${FIRMWARE_REPO} @ ${FIRMWARE_BRANCH}"

# Install build dependencies
dnf install -y fedora-repos
dnf install -y \
  rpm-build gcc gcc-c++ make autoconf automake libtool \
  meson ninja-build pkg-config git \
  glib2-devel libqmi-devel libmbim-devel libyaml-devel libbsd-devel \
  protobuf-c-devel protobuf-c-compiler protobuf-compiler python3-devel \
  polkit-devel libgudev-devel systemd systemd-devel systemd-rpm-macros

# Verify critical deps
rpm -q libqmi-devel libbsd-devel libyaml-devel protobuf-c-devel python3-devel glib2-devel polkit-devel libgudev-devel systemd-devel
echo "✓ Build dependencies verified"

# Set up rpmbuild directory in workspace
mkdir -p /workspace/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Clone source repos to /tmp
cd /tmp

git clone --depth 1 --branch "$FIRMWARE_BRANCH" "$FIRMWARE_REPO" sheng-firmware
git clone --depth 1 https://github.com/ianchb/sheng_devauth.git sheng-devauth-src
git clone --depth 1 --branch 0.21 https://github.com/ianchb/xiaomi-mipps-auth.git
git clone --depth 1 --branch 0.20 https://github.com/ianchb/xiaomi-charger-mode.git
git clone --depth 1 --branch v0.3.9 https://github.com/ianchb/xiaomi-sheng-thp.git
git clone --depth 1 --branch v0.2.3 https://github.com/ianchb/xiaomi-pen-status.git
git clone --depth 1 --branch v0.2.0 https://github.com/ianchb/xiaomi-sheng-keyboard-helper.git
git clone --depth 1 --branch v0.1.4 https://github.com/ianchb/xiaomi-sheng-fingerprint.git
git clone --depth 1 https://github.com/slhssb/xiaomi-sheng-keyboard-backlight.git
git clone --depth 1 https://github.com/alghiffaryfa19/sheng-sensors-file.git

git clone --depth 1 --sparse https://github.com/ianchb/debian-sheng.git debian-sheng
cd debian-sheng
git sparse-checkout set alsa-xiaomi-sheng
cd /tmp

git clone --depth 1 --branch v1.0.2 https://github.com/qualcomm/fastrpc.git

git clone https://codeberg.org/DylanVanAssche/libssc.git libssc

git clone --depth 1 --branch 3.9 https://gitlab.freedesktop.org/hadess/iio-sensor-proxy.git

echo "✓ Source repos cloned"

# Create source tarballs
cd /tmp

mv sheng-firmware sheng-firmware-1.0
tar -czf /workspace/rpmbuild/SOURCES/firmware-xiaomi-sheng-1.0.tar.gz sheng-firmware-1.0/

mv sheng-devauth-src sheng_devauth-1.0
tar -czf /workspace/rpmbuild/SOURCES/sheng-devauth-1.0.tar.gz sheng_devauth-1.0/
mv sheng_devauth-1.0 sheng-devauth-src

mv xiaomi-mipps-auth xiaomi-mipps-auth-0.21
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-mipps-auth-0.21.tar.gz xiaomi-mipps-auth-0.21/

mv xiaomi-charger-mode xiaomi-charger-mode-0.20
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-charger-mode-0.20.tar.gz xiaomi-charger-mode-0.20/

mv xiaomi-sheng-thp xiaomi-sheng-thp-0.3.9
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-thp-0.3.9.tar.gz xiaomi-sheng-thp-0.3.9/

mv xiaomi-pen-status xiaomi-pen-status-0.2.3
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-pen-status-0.2.3.tar.gz xiaomi-pen-status-0.2.3/

mv xiaomi-sheng-keyboard-backlight xiaomi-sheng-keyboard-backlight-1.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-keyboard-backlight-1.0.tar.gz xiaomi-sheng-keyboard-backlight-1.0/

mv xiaomi-sheng-keyboard-helper xiaomi-sheng-keyboard-helper-0.2.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-keyboard-helper-0.2.0.tar.gz xiaomi-sheng-keyboard-helper-0.2.0/

mv xiaomi-sheng-fingerprint xiaomi-sheng-fingerprint-0.1.4
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-fingerprint-0.1.4.tar.gz xiaomi-sheng-fingerprint-0.1.4/

cd /tmp/sheng-sensors-file
tar -czf /workspace/rpmbuild/SOURCES/sheng-sensors-20240917.tar.gz .
cd /tmp

cp -r /tmp/debian-sheng/alsa-xiaomi-sheng /workspace/alsa-xiaomi-sheng
cd /workspace/alsa-xiaomi-sheng
tar -czf /workspace/rpmbuild/SOURCES/alsa-xiaomi-sheng-1.0.tar.gz .
cd /tmp

mv fastrpc fastrpc-1.0.2
tar -czf /workspace/rpmbuild/SOURCES/fastrpc-1.0.2.tar.gz fastrpc-1.0.2/

mv libssc libssc-0.3.0
tar -czf /workspace/rpmbuild/SOURCES/libssc-0.3.0.tar.gz libssc-0.3.0/

mv iio-sensor-proxy iio-sensor-proxy-3.9
tar -czf /workspace/rpmbuild/SOURCES/iio-sensor-proxy-3.9.tar.gz iio-sensor-proxy-3.9/

# Copy special source files (Source1, Patch0, etc.)
cp /workspace/patches/adsprpcd-sensorspd.service /workspace/rpmbuild/SOURCES/
cp /workspace/patches/wait_for_qmi_service.patch /workspace/rpmbuild/SOURCES/
cp /workspace/patches/sheng-devauth.service /workspace/rpmbuild/SOURCES/
cp /workspace/patches/sheng-devauth.service.d-qtee.conf /workspace/rpmbuild/SOURCES/

echo "✓ Source tarballs created"

# Build RPMs
cd /workspace/rpm
export RPM_TOPDIR=/workspace/rpmbuild

# Build libssc FIRST - thp/keyboard-helper/iio-sensor-proxy need its headers
echo "=== Building libssc ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba libssc.spec
# Install libssc so subsequent builds can find it
dnf install -y /workspace/rpmbuild/RPMS/aarch64/libssc-0.3.0-*.rpm
dnf install -y /workspace/rpmbuild/RPMS/aarch64/libssc-devel-*.rpm

echo "=== Building fastrpc ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba fastrpc.spec

echo "=== Building xiaomi-sheng-thp ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba xiaomi-sheng-thp.spec

echo "=== Building xiaomi-sheng-keyboard-helper ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba xiaomi-sheng-keyboard-helper.spec

echo "=== Building iio-sensor-proxy ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba iio-sensor-proxy.spec

echo "=== Building firmware-xiaomi-sheng ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba firmware-xiaomi-sheng.spec

echo "=== Building sheng-devauth ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba sheng-devauth.spec

echo "=== Building xiaomi-mipps-auth ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba xiaomi-mipps-auth.spec

echo "=== Building xiaomi-charger-mode ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba xiaomi-charger-mode.spec

echo "=== Building xiaomi-sheng-keyboard-backlight ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba xiaomi-sheng-keyboard-backlight.spec

echo "=== Building sheng-sensors ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba sheng-sensors.spec

echo "=== Building alsa-xiaomi-sheng ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba alsa-xiaomi-sheng.spec

echo "=== Building xiaomi-pen-status ==="
  dnf install -y qt6-qtbase-devel qt6-qtsvg-devel qt6-qtnetworkauth-devel qt6-qtbase-private-devel
rpmbuild --define "_topdir $RPM_TOPDIR" -ba xiaomi-pen-status.spec

echo "=== Building xiaomi-sheng-fingerprint ==="
  dnf install -y meson ninja-build glib2-devel libgusb-devel patchelf binutils curl tar xz
rpmbuild --define "_topdir $RPM_TOPDIR" -ba xiaomi-sheng-fingerprint.spec

echo "✓ RPM build complete"
ls -la /workspace/rpmbuild/RPMS/
