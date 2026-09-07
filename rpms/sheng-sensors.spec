# Copyright (C) 2026 mumuxiao722 <zy349931@163.com>
# Licensed under the GPL-3.0-or-later. See LICENSE for details.

%undefine __debug_package
%undefine _debugsource_packages
Name:           sheng-sensors
Version:        20240917
Release:        1%{?dist}
Summary:        Sensor configuration files for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/alghiffaryfa19/sheng-sensors-file
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildArch:      noarch
Requires:       iio-sensor-proxy
Requires:       libssc

%description
Proprietary sensor configuration files for Qualcomm Sensor Core (SSC)
framework on Xiaomi Pad 6S Pro. Includes accelerometer, gyroscope,
magnetometer, and proximity sensor configurations.

%prep
tar -xf %{SOURCE0}

%install
mkdir -p %{buildroot}/usr/lib/systemd/system/iio-sensor-proxy.service.d
cat > %{buildroot}/usr/lib/systemd/system/iio-sensor-proxy.service.d/10-sheng-sensors.conf << 'EOF'
[Unit]
Wants=adsprpcd-sensorspd.service
After=adsprpcd-sensorspd.service

[Service]
ExecStartPre=/bin/sleep 8
EOF

mkdir -p %{buildroot}/usr/lib/udev/rules.d
cat > %{buildroot}/usr/lib/udev/rules.d/81-sheng-ssc-sensors.rules << 'EOF'
SUBSYSTEM=="misc", KERNEL=="fastrpc-adsp*", ENV{IIO_SENSOR_PROXY_TYPE}+="ssc-accel ssc-proximity", ENV{ACCEL_MOUNT_MATRIX}="0, 1, 0; -1, 0, 0; 0, 0, 1"
EOF

install -d %{buildroot}/usr/share/qcom/conf.d
install -m 644 usr/share/qcom/conf.d/sheng.yaml %{buildroot}/usr/share/qcom/conf.d/

cp -r usr/share/qcom/sm8550 %{buildroot}/usr/share/qcom/

%post
udevadm control --reload-rules
%systemd_post iio-sensor-proxy.service

%postun
%systemd_postun_with_restart iio-sensor-proxy.service

%files
/usr/lib/systemd/system/iio-sensor-proxy.service.d/10-sheng-sensors.conf
/usr/lib/udev/rules.d/81-sheng-ssc-sensors.rules
/usr/share/qcom/conf.d/sheng.yaml
/usr/share/qcom/sm8550/Xiaomi/sheng/

%changelog

* Sat Sep 05 2026 opencode <opencode@localhost> - 0.0.0-1
- Initial package
