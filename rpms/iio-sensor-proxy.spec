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
BuildRequires:  glib2-devel >= 2.76
BuildRequires:  libgudev-devel >= 237
BuildRequires:  polkit-devel >= 0.91
BuildRequires:  libssc-devel >= 0.2.1
BuildRequires:  systemd-rpm-macros

%description
iio-sensor-proxy with Qualcomm SSC support patches. Provides D-Bus interface
for IIO sensors including accelerometer, gyroscope, light, and proximity sensors.
Patched version for Xiaomi Pad 6S Pro.

%prep
%autosetup -n %{name}-%{version}

%build
meson setup build --prefix=/usr --libdir=/usr/lib64 --buildtype=plain \
    -Dssc-support=enabled \
    -Dsystemdsystemunitdir=/usr/lib/systemd/system
meson compile -C build

%install
DESTDIR=%{buildroot} meson install -C build

%post
%systemd_post iio-sensor-proxy.service

%preun
%systemd_preun iio-sensor-proxy.service

%files
%license COPYING
%doc README.md
/usr/bin/monitor-sensor
/usr/libexec/iio-sensor-proxy
/usr/share/dbus-1/system-services/org.freedesktop.IOSensorProxy.service
/usr/share/polkit-1/actions/org.freedesktop.IOSensorProxy.policy
/usr/lib/systemd/system/iio-sensor-proxy.service
/usr/lib/udev/rules.d/80-iio-sensor-proxy.rules

%changelog
