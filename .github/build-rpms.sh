#!/bin/bash
set -e

FEDORA_VERSION="${1:-44}"

echo "=== Building RPMs in Fedora ${FEDORA_VERSION} container ==="

# Install build dependencies
dnf install -y \
  rpm-build gcc gcc-c++ make autoconf automake libtool \
  meson ninja-build pkg-config git \
  glib2-devel libqmi-devel libmbim-devel libyaml-devel libbsd-devel \
  protobuf-c-devel protobuf-c-compiler protobuf-compiler python3-devel \
  polkit-devel libgudev-devel systemd-rpm-macros

# Set up rpmbuild directory in workspace
mkdir -p /workspace/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Clone source repos to /tmp
cd /tmp

git clone --depth 1 https://github.com/ianchb/sheng-firmware.git
git clone --depth 1 https://github.com/alghiffaryfa19/Linux-xiaomi-sheng.git --branch sheng --single-branch sheng-devauth-src
git clone --depth 1 https://github.com/ianchb/xiaomi-mipps-auth.git
git clone --depth 1 https://github.com/ianchb/xiaomi-charger-mode.git
git clone --depth 1 https://github.com/ianchb/xiaomi-sheng-thp.git
git clone --depth 1 https://github.com/ianchb/xiaomi-pen-status.git
git clone --depth 1 https://github.com/slhssb/xiaomi-sheng-keyboard-backlight.git
git clone --depth 1 https://github.com/ianchb/xiaomi-sheng-keyboard-helper.git
git clone --depth 1 https://github.com/qualcomm/fastrpc.git
git clone --depth 1 https://codeberg.org/DylanVanAssche/libssc.git
git clone --depth 1 https://gitlab.freedesktop.org/hadess/iio-sensor-proxy.git
git clone --depth 1 https://github.com/ianchb/xiaomi-sheng-fingerprint.git
git clone --depth 1 https://github.com/alghiffaryfa19/sheng-sensors-file.git

echo "✓ Source repos cloned"

# Create source tarballs
cd /tmp

# firmware-xiaomi-sheng
mv sheng-firmware sheng-firmware-1.0
tar -czf /workspace/rpmbuild/SOURCES/firmware-xiaomi-sheng-1.0.tar.gz sheng-firmware-1.0/

# sheng-devauth (rename dir to match %autosetup -n sheng_devauth-1.0)
mv sheng-devauth-src/sheng-devauth sheng_devauth-1.0
tar -czf /workspace/rpmbuild/SOURCES/sheng-devauth-1.0.tar.gz sheng_devauth-1.0/
mv sheng_devauth-1.0 sheng-devauth-src/

# xiaomi-mipps-auth
mv xiaomi-mipps-auth xiaomi-mipps-auth-1.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-mipps-auth-1.0.tar.gz xiaomi-mipps-auth-1.0/

# xiaomi-charger-mode
mv xiaomi-charger-mode xiaomi-charger-mode-1.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-charger-mode-1.0.tar.gz xiaomi-charger-mode-1.0/

# xiaomi-sheng-thp
mv xiaomi-sheng-thp xiaomi-sheng-thp-0.4.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-thp-0.4.0.tar.gz xiaomi-sheng-thp-0.4.0/

# xiaomi-pen-status
mv xiaomi-pen-status xiaomi-pen-status-1.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-pen-status-1.0.tar.gz xiaomi-pen-status-1.0/

# xiaomi-sheng-keyboard-backlight
mv xiaomi-sheng-keyboard-backlight xiaomi-sheng-keyboard-backlight-1.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-keyboard-backlight-1.0.tar.gz xiaomi-sheng-keyboard-backlight-1.0/

# xiaomi-sheng-keyboard-helper
mv xiaomi-sheng-keyboard-helper xiaomi-sheng-keyboard-helper-1.0
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-keyboard-helper-1.0.tar.gz xiaomi-sheng-keyboard-helper-1.0/

# xiaomi-sheng-fingerprint
mv xiaomi-sheng-fingerprint xiaomi-sheng-fingerprint-0.1.4
tar -czf /workspace/rpmbuild/SOURCES/xiaomi-sheng-fingerprint-0.1.4.tar.gz xiaomi-sheng-fingerprint-0.1.4/

# sheng-sensors (flatten directory)
cd /tmp/sheng-sensors-file
tar -czf /workspace/rpmbuild/SOURCES/sheng-sensors-20240917.tar.gz .
cd /tmp

# alsa-xiaomi-sheng (flatten directory)
cd /workspace/alsa-xiaomi-sheng
tar -czf /workspace/rpmbuild/SOURCES/alsa-xiaomi-sheng-1.0.tar.gz .
cd /tmp

# fastrpc (need parent dir for %autosetup)
mv fastrpc fastrpc-1.0.2
tar -czf /workspace/rpmbuild/SOURCES/fastrpc-1.0.2.tar.gz fastrpc-1.0.2/

# libssc (need parent dir for %autosetup)
mv libssc libssc-0.4.4
tar -czf /workspace/rpmbuild/SOURCES/libssc-0.4.4.tar.gz libssc-0.4.4/

# iio-sensor-proxy (need parent dir for %autosetup)
mv iio-sensor-proxy iio-sensor-proxy-3.9
tar -czf /workspace/rpmbuild/SOURCES/iio-sensor-proxy-3.9.tar.gz iio-sensor-proxy-3.9/

# Copy special source files (Source1, Patch0, etc.)
cp /workspace/patches/adsprpcd-sensorspd.service /workspace/rpmbuild/SOURCES/
cp /workspace/patches/wait_for_qmi_service.patch /workspace/rpmbuild/SOURCES/

echo "✓ Source tarballs created"

# Build RPMs
cd /workspace/rpms

# Build libssc FIRST - thp/keyboard-helper/iio-sensor-proxy need its headers
echo "=== Building libssc ==="
rpmbuild -ba libssc.spec
# Install libssc so subsequent builds can find it
dnf install -y /workspace/rpmbuild/RPMS/aarch64/libssc-0.4.4-*.rpm
dnf install -y /workspace/rpmbuild/RPMS/aarch64/libssc-devel-*.rpm

echo "=== Building fastrpc ==="
rpmbuild -ba fastrpc.spec

echo "=== Building xiaomi-sheng-thp ==="
rpmbuild -ba xiaomi-sheng-thp.spec

echo "=== Building xiaomi-sheng-keyboard-helper ==="
rpmbuild -ba xiaomi-sheng-keyboard-helper.spec

echo "=== Building iio-sensor-proxy ==="
rpmbuild -ba iio-sensor-proxy.spec

echo "=== Building firmware-xiaomi-sheng ==="
rpmbuild -ba firmware-xiaomi-sheng.spec

echo "=== Building sheng-devauth ==="
rpmbuild -ba sheng-devauth.spec

echo "=== Building xiaomi-mipps-auth ==="
rpmbuild -ba xiaomi-mipps-auth.spec

echo "=== Building xiaomi-charger-mode ==="
rpmbuild -ba xiaomi-charger-mode.spec

echo "=== Building xiaomi-sheng-keyboard-backlight ==="
rpmbuild -ba xiaomi-sheng-keyboard-backlight.spec

echo "=== Building sheng-sensors ==="
rpmbuild -ba sheng-sensors.spec

echo "=== Building alsa-xiaomi-sheng ==="
rpmbuild -ba alsa-xiaomi-sheng.spec

echo "✓ RPM build complete"
ls -la /workspace/rpmbuild/RPMS/
