Name:           kernel-sheng
Version:        %{_kernel_version}
Release:        1
Summary:        Kernel for Xiaomi Pad 6S Pro (sheng)
License:        GPLv2
URL:            %{_kernel_repo}
Source0:        kernel-sheng-%{version}.tar.gz

%undefine __debug_package
%undefine _debugsource_packages
%define _build_id_links none

%description
Prebuilt kernel for Xiaomi Pad 6S Pro.

%prep

%build

%install
mkdir -p %{buildroot}/boot
mkdir -p %{buildroot}/lib/modules
cp -a boot/* %{buildroot}/boot/
cp -a lib/modules/* %{buildroot}/lib/modules/

%files
/boot/Image.gz
/boot/sm8550-xiaomi-sheng.dtb
/boot/config-*
/boot/Image.gz-dtb_sheng
/lib/modules/*

%changelog
* %(date "+%%a %%b %%d %%Y") Fedora Sheng Build <build@sheng> - %{version}-%{release}
- Automated kernel build for Xiaomi Pad 6S Pro
