Name:           firmware-xiaomi-sheng
Version:        1.0
Release:        1%{?dist}
Summary:        Firmware blobs for Xiaomi Pad 6s Pro

License:        Proprietary
URL:            https://github.com/ianchb/sheng-firmware
Source0:        %{url}/archive/%{version}.tar.gz

BuildArch:      noarch
Conflicts:      linux-firmware

%description
Firmware blobs and configuration files for Xiaomi Pad 6s Pro (sheng).
Includes WiFi, Bluetooth, DSP, and other device-specific firmware.

%prep
%autosetup -n sheng-firmware-%{version}

%install
mkdir -p %{buildroot}/usr/lib/firmware
cp -r * %{buildroot}/usr/lib/firmware/

%files
/usr/lib/firmware/*

%changelog
