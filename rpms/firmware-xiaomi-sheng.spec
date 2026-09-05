%undefine __debug_package
%undefine _debugsource_packages
Name:           firmware-xiaomi-sheng
Version:        1.0
Release:        1%{?dist}
Summary:        Firmware blobs for Xiaomi Pad 6s Pro

License:        Proprietary
URL:            https://github.com/ianchb/sheng-firmware
Source0:        git+https://github.com/ianchb/sheng-firmware.git#branch=master

%define _debug_source_subpackages 0

BuildArch:      noarch
Conflicts:      linux-firmware
%define __strip /bin/true

%description
Firmware blobs and configuration files for Xiaomi Pad 6s Pro (sheng).
Includes WiFi, Bluetooth, DSP, and other device-specific firmware.

%prep
%autosetup

%install
mkdir -p %{buildroot}/usr/lib/firmware
cp -r * %{buildroot}/usr/lib/firmware/

%files
/usr/lib/firmware/*

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
