%undefine __debug_package
%undefine _debugsource_packages
%define _debug_package %{nil}
%define _build_id_links none
Name:           sheng-devauth
Version:        1.0
Release:        1%{?dist}
Summary:        Xiaomi keyboard authentication daemon for Pad 6S Pro

License:        Proprietary
URL:            https://github.com/alghiffaryfa19/Linux-xiaomi-sheng
Source0:        %{name}-%{version}.tar.gz
Source1:        sheng-devauth.service
Source2:        sheng-devauth.service.d-qtee.conf

%define _debug_source_subpackages 0

BuildRequires:  gcc
BuildRequires:  make
Requires:       systemd

%description
Service used in pair with kernel driver to authenticate Xiaomi Keyboard
via Qualcomm TEE (TrustZone) for Xiaomi Pad 6S Pro.

%prep
%autosetup -n sheng_devauth-%{version}

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/usr/bin
install -m 755 xiaomi_devauth %{buildroot}/usr/bin/

mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/sheng-devauth.service
mkdir -p %{buildroot}/usr/lib/systemd/system/sheng-devauth.service.d
install -m 644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/sheng-devauth.service.d/qtee.conf

%post
%systemd_post sheng-devauth.service

%preun
%systemd_preun sheng-devauth.service

%postun
%systemd_postun_with_restart sheng-devauth.service

%files
/usr/bin/xiaomi_devauth
/usr/lib/systemd/system/sheng-devauth.service
/usr/lib/systemd/system/sheng-devauth.service.d/qtee.conf

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
