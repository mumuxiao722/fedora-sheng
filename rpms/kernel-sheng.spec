Name:           kernel-sheng
Version:        %{_kernel_version}
Release:        1.fc%{_fedora_version}
Summary:        Kernel for Xiaomi Pad 6S Pro (sheng)
License:        GPLv2
URL:            %{_kernel_repo}
Source0:        kernel-sheng-%{version}.tar.gz

BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  lld
BuildRequires:  make
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  openssl-devel
BuildRequires:  elfutils-devel
BuildRequires:  bc
BuildRequires:  zstd
BuildRequires:  dtc
BuildRequires:  perl-interpreter
BuildRequires:  perl-Carp
BuildRequires:  perl-devel
BuildRequires:  glibc-static

%undefine __debug_package
%undefine _debugsource_packages
%define _build_id_links none

%description
Linux kernel built for Xiaomi Pad 6S Pro (sheng) with mainline support.

%prep
%autosetup -n linux -p1
cp %{_kernel_config} .config

%build
make -j$(nproc) ARCH=arm64 LLVM=1

%install
KVER="$(make kernelrelease -s)"

# Image + DTB
install -Dm644 arch/arm64/boot/Image.gz %{buildroot}/boot/Image.gz
install -Dm644 arch/arm64/boot/dts/qcom/sm8550-xiaomi-sheng.dtb %{buildroot}/boot/sm8550-xiaomi-sheng.dtb
install -Dm644 .config %{buildroot}/boot/config-${KVER}

# Modules
make -j$(nproc) ARCH=arm64 LLVM=1 \
    INSTALL_MOD_PATH=%{buildroot} \
    modules_install

# Combined Image.gz-dtb for mkbootimg
cat arch/arm64/boot/Image.gz \
    arch/arm64/boot/dts/qcom/sm8550-xiaomi-sheng.dtb \
    > %{buildroot}/boot/Image.gz-dtb_sheng

%files
/boot/Image.gz
/boot/sm8550-xiaomi-sheng.dtb
/boot/config-*
/boot/Image.gz-dtb_sheng
/lib/modules/*

%changelog
* %(date "+%%a %%b %%d %%Y") Fedora Sheng Build <build@sheng> - %{version}-%{release}
- Automated kernel build for Xiaomi Pad 6S Pro
