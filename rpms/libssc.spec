Name:           libssc
Version:        0.4.4
Release:        1%{?dist}
Summary:        Library to expose Qualcomm Sensor Core sensors

License:        LGPL-2.1-or-later
URL:            https://codeberg.org/DylanVanAssche/libssc
Source0:        %{url}/archive/v%{version}.tar.gz
Patch0:         wait_for_qmi_service.patch

BuildRequires:  meson >= 1.4.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0) >= 2.56
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(qmi-glib-1) >= 1.33.4
BuildRequires:  pkgconfig(libprotobuf-c)
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-c-compiler

%description
libssc userspace library for Qualcomm SSC (Sensor Signal Conditioner).
Provides access to accelerometer, gyroscope, magnetometer, and other sensors
via QMI protocol.

%prep
%autosetup -n libssc-%{version} -p1

%build
%meson
%meson_build

%install
%meson_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_bindir}/ssccli
%{_libdir}/libssc.so.2*
%{_libdir}/pkgconfig/libssc.pc

%changelog
