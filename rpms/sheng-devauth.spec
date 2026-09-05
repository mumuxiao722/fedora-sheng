Name:           sheng-devauth
Version:        1.0
Release:        1%{?dist}
Summary:        Xiaomi keyboard authentication daemon for Pad 6S Pro

License:        Proprietary
URL:            https://github.com/alghiffaryfa19/Linux-xiaomi-sheng
Source0:        %{name}-%{version}.tar.gz

Requires:       systemd

%description
Service used in pair with kernel driver to authenticate Xiaomi Keyboard
via Qualcomm TEE (TrustZone) for Xiaomi Pad 6S Pro.

%prep
%autosetup -n sheng_devauth-%{version}

%install
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 usr/lib/systemd/system/sheng-devauth.service %{buildroot}/usr/lib/systemd/system/

%post
%systemd_post sheng-devauth.service

%preun
%systemd_preun sheng-devauth.service

%files
%{_unitdir}/sheng-devauth.service

%changelog
