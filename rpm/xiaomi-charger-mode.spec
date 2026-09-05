%undefine __debug_package
%undefine _debugsource_packages
Name:           xiaomi-charger-mode
Version:        1.0
Release:        1%{?dist}
Summary:        Xiaomi charger mode display for Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-charger-mode
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildArch:      noarch
Requires:       python3
Requires:       systemd

%description
Shows a simple charging screen and prevents a full system boot when a charger
is connected while the device is powered off for Xiaomi Pad 6S Pro.

%prep
%autosetup -n xiaomi-charger-mode-%{version}

%install
mkdir -p %{buildroot}/usr/libexec
install -m 755 xiaomi-charger-mode %{buildroot}/usr/libexec/

mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 xiaomi-charger-mode.service %{buildroot}/usr/lib/systemd/system/

%post
%systemd_post xiaomi-charger-mode.service

%preun
%systemd_preun xiaomi-charger-mode.service

%postun
%systemd_postun_with_restart xiaomi-charger-mode.service

%files
/usr/libexec/xiaomi-charger-mode
/usr/lib/systemd/system/xiaomi-charger-mode.service

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
