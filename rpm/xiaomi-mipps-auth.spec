%undefine __debug_package
%undefine _debugsource_packages
Name:           xiaomi-mipps-auth
Version:        1.0
Release:        1%{?dist}
Summary:        Xiaomi MIPPS authentication for 120W fast charging

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-mipps-auth
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildArch:      noarch
Requires:       python3
Requires:       systemd
Requires:       udev

%description
Automatically negotiates MIPPS when a charger is connected, enabling fast
charging up to 120W and providing charging notifications for Xiaomi Pad 6S Pro.

%prep
%autosetup -n xiaomi-mipps-auth-%{version}

%install
mkdir -p %{buildroot}/usr/libexec
install -m 755 xiaomi-mipps-auth %{buildroot}/usr/libexec/

mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 xiaomi-mipps-auth.service %{buildroot}/usr/lib/systemd/system/

mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m 644 90-xiaomi-mipps-auth.rules %{buildroot}/usr/lib/udev/rules.d/

%post
%systemd_post xiaomi-mipps-auth.service
udevadm control --reload-rules

%preun
%systemd_preun xiaomi-mipps-auth.service

%files
/usr/libexec/xiaomi-mipps-auth
/usr/lib/systemd/system/xiaomi-mipps-auth.service
/usr/lib/udev/rules.d/90-xiaomi-mipps-auth.rules

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
