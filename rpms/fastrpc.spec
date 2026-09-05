Name:           fastrpc
Version:        1.0.2
Release:        1%{?dist}
Summary:        Qualcomm FastRPC userspace library

License:        BSD-3-Clause
URL:            https://github.com/qualcomm/fastrpc
Source0:        %{name}-%{version}.tar.gz

%define _debug_package 0
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
    --libdir=/usr/lib64 \
    --with-systemdsystemunitdir=/usr/lib/systemd/system \
    --with-udevrulesdir=/usr/lib/udev/rules.d \
    --with-sysusersdir=/usr/lib/sysusers.d
make %{?_smp_mflags}

%install
%make_install
# Remove test binaries
rm -f %{buildroot}/usr/bin/dsp_check
rm -f %{buildroot}/usr/bin/fastrpc_test
# Remove headers
rm -rf %{buildroot}/usr/include
# Remove test libraries directory
rm -rf %{buildroot}/usr/lib64/fastrpc_test
# Remove test data
rm -rf %{buildroot}/usr/share/fastrpc_test
# Remove man pages
rm -rf %{buildroot}/usr/share/man
# Remove libtool archives
rm -f %{buildroot}/usr/lib64/libadsp_default_listener.la
rm -f %{buildroot}/usr/lib64/libadsprpc.la
rm -f %{buildroot}/usr/lib64/libcdsp_default_listener.la
rm -f %{buildroot}/usr/lib64/libcdsprpc.la
rm -f %{buildroot}/usr/lib64/libsdsp_default_listener.la
rm -f %{buildroot}/usr/lib64/libsdsprpc.la
# Remove upstream services (we use our own adsprpcd-sensorspd.service)
rm -f %{buildroot}/usr/lib/systemd/system/adsprpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/adsprpcd_audiopd.service
rm -f %{buildroot}/usr/lib/systemd/system/cdsp1rpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/cdsprpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/gdsp0rpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/gdsp1rpcd.service
rm -f %{buildroot}/usr/lib/systemd/system/sdsprpcd.service
# Install our custom service
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
/usr/sbin/gdsprpcd
/usr/lib64/libadsprpc.so.1.0.0
/usr/lib64/libadsprpc.so.1
/usr/lib64/libadsprpc.so
/usr/lib64/libcdsprpc.so.1.0.0
/usr/lib64/libcdsprpc.so.1
/usr/lib64/libcdsprpc.so
/usr/lib64/libsdsprpc.so.1.0.0
/usr/lib64/libsdsprpc.so.1
/usr/lib64/libsdsprpc.so
/usr/lib64/libadsp_default_listener.so.1.0.0
/usr/lib64/libadsp_default_listener.so.1
/usr/lib64/libadsp_default_listener.so
/usr/lib64/libcdsp_default_listener.so.1.0.0
/usr/lib64/libcdsp_default_listener.so.1
/usr/lib64/libcdsp_default_listener.so
/usr/lib64/libsdsp_default_listener.so.1.0.0
/usr/lib64/libsdsp_default_listener.so.1
/usr/lib64/libsdsp_default_listener.so
/usr/lib/systemd/system/adsprpcd-sensorspd.service
/usr/lib/udev/rules.d/60-fastrpc.rules
/usr/lib/sysusers.d/fastrpc.conf

%changelog
