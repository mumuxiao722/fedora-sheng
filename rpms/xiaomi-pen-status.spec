# Copyright (C) 2026 mumuxiao722 <zy349931@163.com>
# Licensed under the GPL-3.0-or-later. See LICENSE for details.

%undefine __debug_package
%undefine _debugsource_packages
Name:           xiaomi-pen-status
Version:        0.2.3
Release:        1%{?dist}
Summary:        Stylus status display for Xiaomi Pad 6S Pro

License:        GPLv2
URL:            https://github.com/ianchb/xiaomi-pen-status
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtnetworkauth-devel
BuildRequires:  qt6-qtbase-private-devel
Requires:       qt6-qtbase
Requires:       qt6-qtsvg
Requires:       xiaomi-sheng-thp
Requires:       xdg-desktop-portal

%description
Shows stylus connection and battery status, and automatically attempts
the initial Bluetooth connection for Xiaomi Pad 6S Pro.

%prep
%autosetup -n xiaomi-pen-status-%{version}

%build
qmake6
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
install -m 755 xiaomi-pen-status %{buildroot}/usr/bin/
install -m 644 xiaomi-pen-status.desktop %{buildroot}/usr/share/applications/

%files
%license LICENSE
/usr/bin/xiaomi-pen-status
/usr/share/applications/xiaomi-pen-status.desktop

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
