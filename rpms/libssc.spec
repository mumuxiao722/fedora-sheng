Name:           libssc
Version:        0.4.4
Release:        1%{?dist}
Summary:        Library to expose Qualcomm Sensor Core sensors

License:        LGPL-2.1-or-later
URL:            https://codeberg.org/DylanVanAssche/libssc
Source0:        %{name}-%{version}.tar.gz
Patch0:         wait_for_qmi_service.patch

BuildRequires:  meson >= 1.4.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0) >= 2.56
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(qmi-glib-1) >= 1.33.4
BuildRequires:  pkgconfig(libprotobuf-c)
BuildRequires:  protobuf-c-compiler

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
/usr/bin/ssccli
/usr/lib64/libssc.so.2*

%package devel
Summary:        Development files for libssc
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and pkg-config for developing applications that use libssc.

%files devel
/usr/include/libssc/
/usr/lib64/pkgconfig/libssc.pc

%changelog
