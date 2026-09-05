Name:           fastrpc
Version:        1.0.2
Release:        1%{?dist}
Summary:        Qualcomm FastRPC userspace library

License:        BSD-3-Clause
URL:            https://github.com/qualcomm/fastrpc
Source0:        %{name}-%{version}.tar.gz
Source1:        adsprpcd-sensorspd.service

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  libyaml-devel
BuildRequires:  systemd-rpm-macros
Requires:       libyaml
Requires:       systemd

%description
FastRPC implementation for Qualcomm DSP communication. Provides userspace
libraries and daemons for ADSP, CDSP, and SDSP communication.

%prep
%autosetup -n fastrpc-%{version}

%build
autoreconf -is
./configure \
    --prefix=/usr \
    --libdir=/usr/lib64 \
    --with-systemdsystemunitdir=/usr/lib/systemd/system \
    --with-udevrulesdir=/usr/lib/udev/rules.d \
    --with-sysusersdir=/usr/lib/sysusers.d
make %{?_smp_mflags}

%install
%make_install
install -Dpm 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/adsprpcd-sensorspd.service

%post
%systemd_post adsprpcd-sensorspd.service

%preun
%systemd_preun adsprpcd-sensorspd.service

%files
%doc README.md
/usr/sbin/adsprpcd
/usr/sbin/cdsprpcd
/usr/sbin/sdsprpcd
/usr/lib64/libadsprpc.so.*
/usr/lib64/libcdsprpc.so.*
/usr/lib64/libsdsprpc.so.*
/usr/lib/systemd/system/*.service
/usr/lib/udev/rules.d/*.rules
/usr/lib/sysusers.d/*.conf

%changelog
