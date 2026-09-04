Name:           xiaomi-sheng-keyboard-helper
Version:        1.0
Release:        1%{?dist}
Summary:        Keyboard helper for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-sheng-keyboard-helper
Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
Requires:       systemd
Requires:       xiaomi-sheng-thp

%description
Supports the microphone indicator on the official keyboard and disables
keyboard input based on the hinge angle for Xiaomi Pad 6S Pro.

%prep
%autosetup -n xiaomi-sheng-keyboard-helper-%{version}

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/libexec
install -m 755 xiaomi-sheng-keyboard-helper %{buildroot}/usr/libexec/

mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 xiaomi-sheng-keyboard-helper-angle.service %{buildroot}/usr/lib/systemd/system/
install -m 644 xiaomi-sheng-keyboard-helper-micmute.service %{buildroot}/usr/lib/systemd/user/

mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m 644 90-xiaomi-sheng-keyboard-helper.rules %{buildroot}/usr/lib/udev/rules.d/

%post
%systemd_post xiaomi-sheng-keyboard-helper-angle.service
%systemd_user_post xiaomi-sheng-keyboard-helper-micmute.service
udevadm control --reload-rules 2>/dev/null || true

%preun
%systemd_preun xiaomi-sheng-keyboard-helper-angle.service
%systemd_user_preun xiaomi-sheng-keyboard-helper-micmute.service

%files
/usr/libexec/xiaomi-sheng-keyboard-helper
/usr/lib/systemd/system/xiaomi-sheng-keyboard-helper-angle.service
/usr/lib/systemd/user/xiaomi-sheng-keyboard-helper-micmute.service
/usr/lib/udev/rules.d/90-xiaomi-sheng-keyboard-helper.rules

%changelog
