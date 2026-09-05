%undefine __debug_package
%undefine _debugsource_packages
%define _debug_package %{nil}
%define _build_id_links none
Name:           xiaomi-sheng-thp
Version:        0.3.9
Release:        1%{?dist}
Summary:        Touch processing for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/xiaomi-sheng-thp
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  glib2-devel
BuildRequires:  libssc-devel
Requires:       systemd

%description
Processes touch data for finger input and stylus support on Xiaomi Pad 6S Pro.
Supports NT36532E touch controller with multitouch and stylus input.

%prep
%autosetup -n xiaomi-sheng-thp-%{version}

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%post
%systemd_post xiaomi-sheng-thp.service

%preun
%systemd_preun xiaomi-sheng-thp.service

%postun
%systemd_postun_with_restart xiaomi-sheng-thp.service

%files
%license LICENSE
%doc README.md
/usr/share/doc/xiaomi-sheng-thp/copyright
/usr/libexec/xiaomi-sheng-thp/xiaomi-sheng-thp
/usr/lib/systemd/system/xiaomi-sheng-thp.service

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
