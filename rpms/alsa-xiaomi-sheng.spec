%undefine __debug_package
%undefine _debugsource_packages
Name:           alsa-xiaomi-sheng
Version:        1.0
Release:        1%{?dist}
Summary:        ALSA Use Case Configuration for Xiaomi Pad 6S Pro

License:        LGPL-2.1-or-later
URL:            https://github.com/ianchb/debian-sheng
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildArch:      noarch
Requires:       alsa-ucm-conf

%description
ALSA Use Case Manager (UCM2) configuration for Xiaomi Pad 6S Pro.
Provides audio routing for speakers, headphones, and DisplayPort audio.

%prep
tar -xf %{SOURCE0}

%install
mkdir -p %{buildroot}/usr/share/alsa/ucm2/conf.d/sm8550
install -m 644 usr/share/alsa/ucm2/Xiaomi/sheng/Xiaomi-Pad6SPro.conf %{buildroot}/usr/share/alsa/ucm2/conf.d/sm8550/

mkdir -p %{buildroot}/usr/share/alsa/ucm2/Xiaomi/sheng
install -m 644 usr/share/alsa/ucm2/Xiaomi/sheng/Xiaomi-Pad6SPro.conf %{buildroot}/usr/share/alsa/ucm2/Xiaomi/sheng/
install -m 644 usr/share/alsa/ucm2/Xiaomi/sheng/HiFi.conf %{buildroot}/usr/share/alsa/ucm2/Xiaomi/sheng/

%files
/usr/share/alsa/ucm2/conf.d/sm8550/Xiaomi-Pad6SPro.conf
/usr/share/alsa/ucm2/Xiaomi/sheng/Xiaomi-Pad6SPro.conf
/usr/share/alsa/ucm2/Xiaomi/sheng/HiFi.conf

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
