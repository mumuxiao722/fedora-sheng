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
    --with-sysusersdir=/usr/lib/sysusers.d \
    --disable-test
make %{?_smp_mflags}

%install
%make_install
# Remove test files, headers, man pages (not needed for production)
rm -rf %{buildroot}/usr/bin/dsp_check %{buildroot}/usr/bin/fastrpc_test 2>/dev/null || true
rm -rf %{buildroot}/usr/include 2>/dev/null || true
rm -rf %{buildroot}/usr/lib64/fastrpc_test 2>/dev/null || true
rm -rf %{buildroot}/usr/share/fastrpc_test 2>/dev/null || true
rm -rf %{buildroot}/usr/share/man 2>/dev/null || true
# Remove unversioned symlinks (keep versioned .so.1.0.0 only)
rm -f %{buildroot}/usr/lib64/libadsprpc.so 2>/dev/null || true
rm -f %{buildroot}/usr/lib64/libcdsprpc.so 2>/dev/null || true
rm -f %{buildroot}/usr/lib64/libsdsprpc.so 2>/dev/null || true
rm -f %{buildroot}/usr/lib64/libadsp_default_listener.so 2>/dev/null || true
rm -f %{buildroot}/usr/lib64/libcdsp_default_listener.so 2>/dev/null || true
rm -f %{buildroot}/usr/lib64/libsdsp_default_listener.so 2>/dev/null || true
# Remove libtool archives and skel/stub libraries
rm -f %{buildroot}/usr/lib64/*.la 2>/dev/null || true
rm -rf %{buildroot}/usr/lib64/lib*skel* 2>/dev/null || true
rm -rf %{buildroot}/usr/lib64/lib*stub* 2>/dev/null || true
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
/usr/lib64/libadsprpc.so*
/usr/lib64/libcdsprpc.so*
/usr/lib64/libsdsprpc.so*
/usr/lib64/libadsp_default_listener.so*
/usr/lib64/libcdsp_default_listener.so*
/usr/lib64/libsdsp_default_listener.so*
/usr/lib/systemd/system/*.service
/usr/lib/udev/rules.d/*.rules
/usr/lib/sysusers.d/*.conf

%changelog
