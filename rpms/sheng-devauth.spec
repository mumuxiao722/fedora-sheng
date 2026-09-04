Name:           sheng-devauth
Version:        1.0
Release:        1%{?dist}
Summary:        Xiaomi keyboard authentication daemon for Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/sheng_devauth
Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
Requires:       systemd

%description
Service used in pair with kernel driver to authenticate Xiaomi Keyboard
via Qualcomm TEE (TrustZone) for Xiaomi Pad 6S Pro.

%prep
%autosetup -n sheng_devauth-%{version}

%build
make %{?_smp_mflags} CC=%{__cc}

%install
mkdir -p %{buildroot}/usr/bin
install -m 755 xiaomi_devauth %{buildroot}/usr/bin/

mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 sheng-devauth.service %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/usr/lib/systemd/system/sheng-devauth.service.d
install -m 644 sheng-devauth.service.d/qtee.conf %{buildroot}/usr/lib/systemd/system/sheng-devauth.service.d/

%post
%systemd_post sheng-devauth.service

%preun
%systemd_preun sheng-devauth.service

%files
/usr/bin/xiaomi_devauth
/usr/lib/systemd/system/sheng-devauth.service
/usr/lib/systemd/system/sheng-devauth.service.d/

%changelog
