Name:           xiaomi-pen-status
Version:        1.0
Release:        1%{?dist}
Summary:        Stylus status display for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-pen-status
Source0:        %{name}-%{version}.tar.gz

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
%autosetup -n xiaomi-pen-status-%{version}

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
