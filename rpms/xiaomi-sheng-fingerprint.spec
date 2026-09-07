# Copyright (C) 2026 mumuxiao722 <zy349931@163.com>
# Licensed under the GPL-3.0-or-later. See LICENSE for details.

%undefine __debug_package
%undefine _debugsource_packages
Name:           xiaomi-sheng-fingerprint
Version:        0.1.4
Release:        1%{?dist}
Summary:        FPC1553 fingerprint sensor support for Xiaomi Pad 6S Pro

License:        Apache-2.0
URL:            https://github.com/ianchb/xiaomi-sheng-fingerprint
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildRequires:  gcc
BuildRequires:  binutils
BuildRequires:  meson >= 0.50.0
BuildRequires:  ninja-build
BuildRequires:  glib2-devel >= 2.56
BuildRequires:  libgusb-devel >= 0.4.9
BuildRequires:  patchelf
BuildRequires:  curl
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  systemd-rpm-macros
Requires:       fprintd >= 1.94.5
Requires:       firmware-xiaomi-sheng

%description
FPC1553 fingerprint sensor support for Xiaomi Pad 6S Pro using Qualcomm
TEE (TrustZone). Provides libfprint backend and fprintd integration.

%prep
%autosetup -n xiaomi-sheng-fingerprint-%{version} -p1

%build
mkdir -p build/backend build/libfprint

# Build backend library (libfpc1553-qtee.so)
scripts/build-backend.sh build/backend

# Build custom libfprint with FPC1553 driver
scripts/build-libfprint.sh build/backend build/libfprint

%install
mkdir -p %{buildroot}/usr/lib/xiaomi-sheng-fingerprint
mkdir -p %{buildroot}/usr/lib/aarch64-linux-gnu/qtee-listeners
mkdir -p %{buildroot}/usr/libexec
mkdir -p %{buildroot}/usr/lib/systemd/system/fprintd.service.d
mkdir -p %{buildroot}/usr/lib/udev/rules.d

# Install libraries
install -m 0644 build/backend/libfpc1553-qtee.so %{buildroot}/usr/lib/xiaomi-sheng-fingerprint/
install -m 0644 build/libfprint/libfprint-2.so.2.0.0 %{buildroot}/usr/lib/xiaomi-sheng-fingerprint/
ln -s libfprint-2.so.2.0.0 %{buildroot}/usr/lib/xiaomi-sheng-fingerprint/libfprint-2.so.2
ln -s libfprint-2.so.2 %{buildroot}/usr/lib/xiaomi-sheng-fingerprint/libfprint-2.so

# Install prebuilt binaries
install -m 0755 prebuilt/aarch64/qteesupplicant %{buildroot}/usr/libexec/
install -m 0755 prebuilt/aarch64/sfs_config %{buildroot}/usr/libexec/fpc-sfs-config

for listener in prebuilt/aarch64/qtee-listeners/*.so.1.0.0; do
    name=$(basename "$listener")
    install -m 0644 "$listener" %{buildroot}/usr/lib/aarch64-linux-gnu/qtee-listeners/$name
    ln -s "$name" %{buildroot}/usr/lib/aarch64-linux-gnu/qtee-listeners/${name%.0.0}
done

# Install systemd services
install -m 0644 systemd/qteesupplicant.service %{buildroot}/usr/lib/systemd/system/
install -m 0644 systemd/sfsconfig.service %{buildroot}/usr/lib/systemd/system/
install -m 0644 systemd/fprintd.service.d/10-xiaomi-sheng-fpc1553.conf %{buildroot}/usr/lib/systemd/system/fprintd.service.d/

# Install udev rules
install -m 0644 udev/99-qcomtee-fpc.rules %{buildroot}/usr/lib/udev/rules.d/

%post
%systemd_post qteesupplicant.service sfsconfig.service fprintd.service

%preun
%systemd_preun qteesupplicant.service sfsconfig.service fprintd.service

%postun
%systemd_postun_with_restart qteesupplicant.service sfsconfig.service fprintd.service

%files
%license LICENSE
%doc README.md UPSTREAM_CHANGES.md
/usr/lib/xiaomi-sheng-fingerprint/libfpc1553-qtee.so
/usr/lib/xiaomi-sheng-fingerprint/libfprint-2.so.2.0.0
/usr/lib/xiaomi-sheng-fingerprint/libfprint-2.so.2
/usr/lib/xiaomi-sheng-fingerprint/libfprint-2.so
/usr/lib/aarch64-linux-gnu/qtee-listeners/
/usr/libexec/qteesupplicant
/usr/libexec/fpc-sfs-config
/usr/lib/systemd/system/qteesupplicant.service
/usr/lib/systemd/system/sfsconfig.service
/usr/lib/systemd/system/fprintd.service.d/10-xiaomi-sheng-fpc1553.conf
/usr/lib/udev/rules.d/99-qcomtee-fpc.rules

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.1.4-1
- Initial package
