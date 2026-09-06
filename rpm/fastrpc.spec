%undefine __debug_package
%undefine _debugsource_packages
%define _debug_package %{nil}
%define _build_id_links none
Name:           fastrpc
Version:        1.0.2
Release:        1%{?dist}
Summary:        Qualcomm FastRPC userspace library

License:        BSD-3-Clause
URL:            https://github.com/qualcomm/fastrpc
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0
Source1:        adsprpcd-sensorspd.service

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  libyaml-devel
BuildRequires:  libbsd-devel
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
    --with-systemdsystemunitdir=/usr/lib/systemd/system
make %{?_smp_mflags}

%install
%make_install
rm -f %{buildroot}/usr/bin/dsp_check
rm -f %{buildroot}/usr/bin/fastrpc_test
rm -rf %{buildroot}/usr/include
rm -rf %{buildroot}/usr/lib/fastrpc_test
rm -rf %{buildroot}/usr/share/fastrpc_test
rm -rf %{buildroot}/usr/share/man
rm -f %{buildroot}/usr/lib/libadsp_default_listener.la
rm -f %{buildroot}/usr/lib/libadsprpc.la
rm -f %{buildroot}/usr/lib/libcdsp_default_listener.la
rm -f %{buildroot}/usr/lib/libcdsprpc.la
rm -f %{buildroot}/usr/lib/libsdsp_default_listener.la
rm -f %{buildroot}/usr/lib/libsdsprpc.la
rm -f %{buildroot}/usr/lib/systemd/system/adsprpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/adsprpcd_audiopd.service
rm -f %{buildroot}/usr/lib/systemd/system/cdsp1rpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/cdsprpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/gdsp0rpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/gdsp1rpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/sdsprpcd.service
install -Dpm 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/adsprpcd-sensorspd.service

%post
%systemd_post adsprpcd-sensorspd.service

%preun
%systemd_preun adsprpcd-sensorspd.service

%postun
%systemd_postun_with_restart adsprpcd-sensorspd.service

%files
%doc README.md
%attr(755, root, root) /usr/bin/adsprpcd
%attr(755, root, root) /usr/bin/cdsprpcd
%attr(755, root, root) /usr/bin/sdsprpcd
%attr(755, root, root) /usr/bin/gdsprpcd
/usr/lib/libadsprpc.so.1.0.0
/usr/lib/libadsprpc.so.1
/usr/lib/libadsprpc.so
/usr/lib/libcdsprpc.so.1.0.0
/usr/lib/libcdsprpc.so.1
/usr/lib/libcdsprpc.so
/usr/lib/libsdsprpc.so.1.0.0
/usr/lib/libsdsprpc.so.1
/usr/lib/libsdsprpc.so
/usr/lib/libadsp_default_listener.so.1.0.0
/usr/lib/libadsp_default_listener.so.1
/usr/lib/libadsp_default_listener.so
/usr/lib/libcdsp_default_listener.so.1.0.0
/usr/lib/libcdsp_default_listener.so.1
/usr/lib/libcdsp_default_listener.so
/usr/lib/libsdsp_default_listener.so.1.0.0
/usr/lib/libsdsp_default_listener.so.1
/usr/lib/libsdsp_default_listener.so
/usr/lib/systemd/system/adsprpcd-sensorspd.service

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
