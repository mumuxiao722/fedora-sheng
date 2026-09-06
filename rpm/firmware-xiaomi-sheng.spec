%undefine __debug_package
%undefine _debugsource_packages
Name:           firmware-xiaomi-sheng
Version:        1.0
Release:        1%{?dist}
Summary:        Firmware blobs for Xiaomi Pad 6s Pro

License:        Proprietary
URL:            https://github.com/ianchb/sheng-firmware
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildArch:      noarch
Conflicts:      linux-firmware
%define __strip /bin/true

%description
Firmware blobs and configuration files for Xiaomi Pad 6s Pro (sheng).
Includes WiFi, Bluetooth, DSP, and other device-specific firmware.

%prep
%autosetup -n sheng-firmware-%{version}

%install
mkdir -p %{buildroot}/lib/firmware
cp -r * %{buildroot}/lib/firmware/
mkdir -p %{buildroot}/lib/firmware/ath12k/WCN7850/hw2.0
cp %{buildroot}/lib/firmware/ath12k/WCN7850/hw2.0/board-2.bin \
   %{buildroot}/lib/firmware/ath12k/WCN7850/hw2.0/board.bin 2>/dev/null || true

%files
/lib/firmware/*

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
