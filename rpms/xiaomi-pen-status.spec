%undefine __debug_package
%undefine _debugsource_packages
Name:           xiaomi-pen-status
Version:        0.2.3
Release:        1%{?dist}
Summary:        Stylus status display for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-pen-status
Source0:        git+https://github.com/ianchb/xiaomi-pen-status.git#tag=v%{version}

%define _debug_source_subpackages 0

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qmake6
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtnetworkauth-devel
BuildRequires:  qt6-qtbase-private-devel
Requires:       qt6-qtbase
Requires:       qt6-qtsvg
Requires:       xiaomi-sheng-thp

%description
Shows stylus connection and battery status, and automatically attempts
the initial Bluetooth connection for Xiaomi Pad 6S Pro.

%prep
%autosetup

%build
qmake6
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/bin
install -m 755 xiaomi-pen-status %{buildroot}/usr/bin/

%files
%license LICENSE
/usr/bin/xiaomi-pen-status

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
