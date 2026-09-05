Name:           iio-sensor-proxy
Version:        3.9
Release:        6%{?dist}
Summary:        IIO sensors to D-Bus proxy (SSC patched)

License:        GPLv2+
URL:            https://gitlab.freedesktop.org/hadess/iio-sensor-proxy
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0) >= 2.76
BuildRequires:  pkgconfig(gudev-1.0) >= 237
BuildRequires:  pkgconfig(polkit-gobject-1) >= 0.91
BuildRequires:  pkgconfig(libssc) >= 0.2.1
BuildRequires:  systemd-rpm-macros

%description
iio-sensor-proxy with Qualcomm SSC support patches. Provides D-Bus interface
for IIO sensors including accelerometer, gyroscope, light, and proximity sensors.
Patched version for Xiaomi Pad 6S Pro.

%prep
%autosetup -n %{name}-%{version}

%build
%meson \
    -Dssc-support=enabled \
    -Dsystemdsystemunitdir=%{_unitdir}
%meson_build

%install
%meson_install

%post
%systemd_post iio-sensor-proxy.service

%preun
%systemd_preun iio-sensor-proxy.service

%files
%license COPYING
%doc README.md
%{_bindir}/monitor-sensor
%{_libexecdir}/iio-sensor-proxy
%{_datadir}/dbus-1/system-services/org.freedesktop.IOSensorProxy.service
%{_datadir}/polkit-1/actions/org.freedesktop.IOSensorProxy.policy
%{_unitdir}/iio-sensor-proxy.service
%{_udevrulesdir}/80-iio-sensor-proxy.rules

%changelog
