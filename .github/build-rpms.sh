#!/bin/bash
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

# Set up rpmbuild directory
mkdir -p /workspace/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy spec files
cp /workspace/rpms/*.spec /workspace/rpmbuild/SPECS/

# Copy extra source files (Source1, Source2, Patch0)
cp /workspace/patches/adsprpcd-sensorspd.service /workspace/rpmbuild/SOURCES/
cp /workspace/patches/wait_for_qmi_service.patch /workspace/rpmbuild/SOURCES/
cp /workspace/patches/sheng-devauth.service /workspace/rpmbuild/SOURCES/
cp /workspace/patches/sheng-devauth.service.d-qtee.conf /workspace/rpmbuild/SOURCES/

# Create tarball for alsa-xiaomi-sheng (local files, no git repo)
cd /workspace/alsa-xiaomi-sheng
tar -czf /workspace/rpmbuild/SOURCES/alsa-xiaomi-sheng-1.0.tar.gz .
cd /workspace

# Override firmware Source0 if custom repo/branch specified
if [ "$FIRMWARE_REPO" != "https://github.com/ianchb/sheng-firmware" ] || [ "$FIRMWARE_BRANCH" != "master" ]; then
  sed -i "s|Source0:.*|Source0: git+${FIRMWARE_REPO}.git#branch=${FIRMWARE_BRANCH}|" \
    /workspace/rpmbuild/SPECS/firmware-xiaomi-sheng.spec
  echo "✓ Firmware Source0 overridden: ${FIRMWARE_REPO} @ ${FIRMWARE_BRANCH}"
fi

echo "✓ Spec files and sources prepared"

# Build RPMs
cd /workspace/rpms
export RPM_TOPDIR=/workspace/rpmbuild

# Build libssc FIRST - thp/keyboard-helper/iio-sensor-proxy need its headers
echo "=== Building libssc ==="
rpmbuild --define "_topdir $RPM_TOPDIR" -ba libssc.spec
# Install libssc so subsequent builds can find it
dnf install -y /workspace/rpmbuild/RPMS/aarch64/libssc-0.4.4-*.rpm
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

echo "✓ RPM build complete"
ls -la /workspace/rpmbuild/RPMS/
