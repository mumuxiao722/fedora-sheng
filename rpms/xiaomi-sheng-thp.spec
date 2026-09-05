Name:           xiaomi-sheng-thp
Version:        0.4.0
Release:        1%{?dist}
Summary:        Touch processing for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-sheng-thp
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libssc)
Requires:       systemd

%description
Processes touch data for finger input and stylus support on Xiaomi Pad 6S Pro.
Supports NT36532E touch controller with multitouch and stylus input.

%prep
%autosetup -n xiaomi-sheng-thp-%{version}

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/libexec/xiaomi-sheng-thp
install -m 755 xiaomi-sheng-thp %{buildroot}/usr/libexec/xiaomi-sheng-thp/

mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 xiaomi-sheng-thp.service %{buildroot}/usr/lib/systemd/system/

%post
%systemd_post xiaomi-sheng-thp.service

%preun
%systemd_preun xiaomi-sheng-thp.service

%files
/usr/libexec/xiaomi-sheng-thp/xiaomi-sheng-thp
/usr/lib/systemd/system/xiaomi-sheng-thp.service

%changelog
