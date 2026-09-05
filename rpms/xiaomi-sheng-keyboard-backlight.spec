Name:           xiaomi-sheng-keyboard-backlight
Version:        1.0
Release:        1%{?dist}
Summary:        Keyboard backlight control for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/slhssb/xiaomi-sheng-keyboard-backlight
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildArch:      noarch
Requires:       python3
Requires:       systemd

%description
Controls keyboard backlight for Xiaomi Pad 6S Pro official keyboard.
Supports manual/automatic brightness control and saves state across reconnections.

%prep
%autosetup -n xiaomi-sheng-keyboard-backlight-%{version}

%install
mkdir -p %{buildroot}/usr/local/sbin
install -m 755 kbd-backlight %{buildroot}/usr/local/sbin/
install -m 755 kbd-backlight-sync %{buildroot}/usr/local/sbin/

mkdir -p %{buildroot}/etc
install -m 644 kbd-backlight-sync.conf %{buildroot}/etc/

mkdir -p %{buildroot}/usr/lib/systemd/user
install -m 644 kbd-backlight-sync.service %{buildroot}/usr/lib/systemd/user/

mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m 644 90-kbd-backlight.rules %{buildroot}/usr/lib/udev/rules.d/

%post
%systemd_user_post kbd-backlight-sync.service

%preun
%systemd_user_preun kbd-backlight-sync.service

%files
/usr/local/sbin/kbd-backlight
/usr/local/sbin/kbd-backlight-sync
%config(noreplace) /etc/kbd-backlight-sync.conf
/usr/lib/systemd/user/kbd-backlight-sync.service
/usr/lib/udev/rules.d/90-kbd-backlight.rules

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
