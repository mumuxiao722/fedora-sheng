%undefine __debug_package
%undefine _debugsource_packages
Name:           xiaomi-sheng-keyboard-helper
Version:        1.0
Release:        1%{?dist}
Summary:        Keyboard helper for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-sheng-keyboard-helper
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glib2-devel
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
make install DESTDIR=%{buildroot}

%post
%systemd_post xiaomi-sheng-keyboard-helper-angle.service
%systemd_user_post xiaomi-sheng-keyboard-helper-micmute.service
udevadm control --reload-rules

%preun
%systemd_preun xiaomi-sheng-keyboard-helper-angle.service
%systemd_user_preun xiaomi-sheng-keyboard-helper-micmute.service

%files
/usr/libexec/xiaomi-sheng-keyboard-helper
/usr/lib/systemd/system/xiaomi-sheng-keyboard-helper-angle.service
/usr/lib/systemd/user/xiaomi-sheng-keyboard-helper-micmute.service
/usr/lib/udev/rules.d/90-xiaomi-sheng-keyboard-helper.rules

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
