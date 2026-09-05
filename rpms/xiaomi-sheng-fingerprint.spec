%undefine __debug_package
%undefine _debugsource_packages
Name:           xiaomi-sheng-fingerprint
Version:        0.1.4
Release:        1%{?dist}
Summary:        FPC1553 fingerprint sensor support for Xiaomi Pad 6S Pro

License:        LGPL-2.1-or-later
URL:            https://github.com/ianchb/xiaomi-sheng-fingerprint
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson >= 0.50.0
BuildRequires:  ninja-build
BuildRequires:  glib2-devel >= 2.56
BuildRequires:  libgusb-devel >= 0.4.9
BuildRequires:  libfprint-devel >= 1.94.0
BuildRequires:  systemd-rpm-macros
BuildRequires:  patchelf
Requires:       fprintd >= 1.94.5
Requires:       firmware-xiaomi-sheng

%description
FPC1553 fingerprint sensor support for Xiaomi Pad 6S Pro using Qualcomm
TEE (TrustZone). Provides libfprint backend and fprintd integration.

%prep
%autosetup -n xiaomi-sheng-fingerprint-%{version} -p1

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/lib/xiaomi-sheng-fingerprint
install -m 755 build/libfpc1553-qtee.so %{buildroot}/usr/lib/xiaomi-sheng-fingerprint/

# Fix rpath
patchelf --set-rpath '$ORIGIN' %{buildroot}/usr/lib/xiaomi-sheng-fingerprint/libfpc1553-qtee.so

%post
%systemd_post fprintd.service

%preun
%systemd_preun fprintd.service

%files
%license LICENSE
%doc README.md
/usr/lib/xiaomi-sheng-fingerprint/libfpc1553-qtee.so

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
