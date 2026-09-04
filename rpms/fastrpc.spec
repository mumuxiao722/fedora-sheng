Name:           fastrpc
Version:        1.0.2
Release:        1%{?dist}
Summary:        Qualcomm FastRPC userspace library

License:        BSD-3-Clause
URL:            https://github.com/qualcomm/fastrpc
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
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
%configure \
    --with-systemdsystemunitdir=%{_unitdir} \
    --with-udevrulesdir=%{_udevrulesdir} \
    --with-sysusersdir=%{_sysusersdir}
make %{?_smp_mflags}

%install
%make_install
install -Dpm 644 %{SOURCE1} %{buildroot}%{_unitdir}/adsprpcd-sensorspd.service

%post
%systemd_post adsprpcd-sensorspd.service
%sysusers_create_compat %{SOURCE1}

%preun
%systemd_preun adsprpcd-sensorspd.service

%files
%license LICENSE
%doc README.md
%{_bindir}/adsprpcd
%{_bindir}/cdsprpcd
%{_bindir}/sdsprpcd
%{_libdir}/libadsprpc.so.*
%{_libdir}/libcdsprpc.so.*
%{_libdir}/libsdsprpc.so.*
%{_unitdir}/adsprpcd-sensorspd.service
%{_udevrulesdir}/*.rules
%{_sysusersdir}/*.conf

%changelog
