Name:           xiaomi-sheng-fingerprint
Version:        0.1.4
Release:        1%{?dist}
Summary:        FPC1553 fingerprint sensor support for Xiaomi Pad 6S Pro

License:        LGPL-2.1-or-later
URL:            https://github.com/ianchb/xiaomi-sheng-fingerprint
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson >= 0.50.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(glib-2.0) >= 2.56
BuildRequires:  pkgconfig(gusb-2.0) >= 0.4.9
BuildRequires:  pkgconfig(libfprint-2) >= 1.94.0
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

# Install systemd service files
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 systemd/fprintd.service.d/*.conf %{buildroot}/usr/lib/systemd/system/ 2>/dev/null || true

# Install udev rules
mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m 644 udev/*.rules %{buildroot}/usr/lib/udev/rules.d/ 2>/dev/null || true

# Fix rpath
patchelf --set-rpath '$ORIGIN' %{buildroot}/usr/lib/xiaomi-sheng-fingerprint/libfpc1553-qtee.so 2>/dev/null || true

%post
%systemd_post fprintd.service 2>/dev/null || true

%preun
%systemd_preun fprintd.service 2>/dev/null || true

%files
%license LICENSE
%doc README.md
/usr/lib/xiaomi-sheng-fingerprint/libfpc1553-qtee.so
/usr/lib/udev/rules.d/*.rules
/usr/lib/systemd/system/*.conf

%changelog
