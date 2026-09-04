Name:           sheng-sensors
Version:        20240917
Release:        1%{?dist}
Summary:        Sensor configuration files for Xiaomi Pad 6S Pro

License:        Proprietary
URL:            https://github.com/ianchb/debian-sheng
Source0:        sheng-sensors-files.tar.gz

BuildArch:      noarch
Requires:       iio-sensor-proxy
Requires:       libssc

%description
Proprietary sensor configuration files for Qualcomm Sensor Core (SSC)
framework on Xiaomi Pad 6S Pro. Includes accelerometer, gyroscope,
magnetometer, and proximity sensor configurations.

%prep

%install
mkdir -p %{buildroot}/usr/lib/systemd/system/iio-sensor-proxy.service.d
install -m 644 %{_sourcedir}/10-sheng-sensors.conf %{buildroot}/usr/lib/systemd/system/iio-sensor-proxy.service.d/

mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m 644 %{_sourcedir}/81-sheng-ssc-sensors.rules %{buildroot}/usr/lib/udev/rules.d/

mkdir -p %{buildroot}/usr/share/qcom/conf.d
install -m 644 %{_sourcedir}/sheng.yaml %{buildroot}/usr/share/qcom/conf.d/

mkdir -p %{buildroot}/usr/share/qcom/sm8550/Xiaomi/sheng
cp -r %{_sourcedir}/config %{buildroot}/usr/share/qcom/sm8550/Xiaomi/sheng/
cp -r %{_sourcedir}/registry %{buildroot}/usr/share/qcom/sm8550/Xiaomi/sheng/
cp -r %{_sourcedir}/socinfo %{buildroot}/usr/share/qcom/sm8550/Xiaomi/sheng/
install -m 644 %{_sourcedir}/sns_reg_version %{buildroot}/usr/share/qcom/sm8550/Xiaomi/sheng/

mkdir -p %{buildroot}/usr/share/qcom/sm8550/Xiaomi/sheng/vendor/etc/sensors
install -m 644 %{_sourcedir}/sns_reg_config %{buildroot}/usr/share/qcom/sm8550/Xiaomi/sheng/vendor/etc/sensors/

%post
udevadm control --reload-rules 2>/dev/null || true
systemctl daemon-reload 2>/dev/null || true

%files
/usr/lib/systemd/system/iio-sensor-proxy.service.d/10-sheng-sensors.conf
/usr/lib/udev/rules.d/81-sheng-ssc-sensors.rules
/usr/share/qcom/conf.d/sheng.yaml
/usr/share/qcom/sm8550/Xiaomi/sheng/

%changelog
