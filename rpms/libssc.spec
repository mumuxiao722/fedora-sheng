Name:           libssc
Version:        0.4.4
Release:        1%{?dist}
Summary:        Library to expose Qualcomm Sensor Core sensors

License:        LGPL-2.1-or-later
URL:            https://codeberg.org/DylanVanAssche/libssc
Source0:        %{name}-%{version}.tar.gz

%define _debug_package 0
Patch0:         wait_for_qmi_service.patch

BuildRequires:  meson >= 1.4.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  glib2-devel >= 2.56
BuildRequires:  libqmi-devel >= 1.33.4
BuildRequires:  libqmi-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  protobuf-c-compiler
BuildRequires:  protobuf-compiler
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description
libssc userspace library for Qualcomm SSC (Sensor Signal Conditioner).
Provides access to accelerometer, gyroscope, magnetometer, and other sensors
via QMI protocol. Patched version for Xiaomi Pad 6S Pro.

%prep
%autosetup -n libssc-%{version} -p1

%build
meson setup build --prefix=/usr --libdir=/usr/lib64 --buildtype=plain
meson compile -C build

%install
DESTDIR=%{buildroot} meson install -C build
# Remove test binary
rm -f %{buildroot}/usr/libexec/installed-tests/libssc/ssc-server
rm -rf %{buildroot}/usr/libexec/installed-tests
# Remove Python mock server (not needed on device)
rm -rf %{buildroot}/usr/lib/python3*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
/usr/bin/ssccli
/usr/lib64/libssc.so.2
/usr/lib64/libssc.so

%package devel
Summary:        Development files for libssc
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and pkg-config for developing applications that use libssc.

%files devel
/usr/include/libssc/libssc.h
/usr/include/libssc/libssc-sensor.h
/usr/include/libssc/libssc-sensor-accelerometer.h
/usr/include/libssc/libssc-sensor-compass.h
/usr/include/libssc/libssc-sensor-gyroscope.h
/usr/include/libssc/libssc-sensor-light.h
/usr/include/libssc/libssc-sensor-magnetometer.h
/usr/include/libssc/libssc-sensor-proximity.h
/usr/include/libssc/libssc-version-private.h
/usr/include/libssc/ssc-common.pb-c.h
/usr/include/libssc/ssc-sensor-accelerometer.pb-c.h
/usr/include/libssc/ssc-sensor-gyroscope.pb-c.h
/usr/include/libssc/ssc-sensor-light.pb-c.h
/usr/include/libssc/ssc-sensor-magnetometer.pb-c.h
/usr/include/libssc/ssc-sensor-proximity.pb-c.h
/usr/include/libssc/ssc-sensor-rotationvector.pb-c.h
/usr/include/libssc/ssc-sensor-suid.pb-c.h
/usr/lib64/pkgconfig/libssc.pc

%changelog
