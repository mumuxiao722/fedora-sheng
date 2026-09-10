# Copyright (C) 2026 mumuxiao722 <zy349931@163.com>
# Licensed under the GPL-3.0-or-later. See LICENSE for details.

%undefine __debug_package
%undefine _debugsource_packages
Name:           sheng-audio-fix
Version:        1.0
Release:        1%{?dist}
Summary:        SM8550 sound card bring-up for Xiaomi Pad 6S Pro (sheng)

License:        GPL-3.0-or-later
URL:            https://github.com/mumuxiao722/fedora-sheng
Source0:        %{name}-%{version}.tar.gz

%define _debug_source_subpackages 0

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Requires:       kmod
Requires:       systemd

%description
Loads the SM8550 ALSA codec stack (soundwire-qcom, wcd938x, lpass macros) and
re-binds the sc8280xp machine driver so the sound card registers after boot.
Fixes "Dummy Output"/no sound on Xiaomi Pad 6S Pro (sheng) Fedora rootfs.

%prep
%autosetup -n sheng-audio-fix-%{version}

%build
# nothing to build, pure file installation

%install
install -D -m 0755 usr/libexec/sm8550-audio-init.sh \
    %{buildroot}%{_libexecdir}/sm8550-audio-init.sh
install -D -m 0644 etc/modules-load.d/sm8550-audio.conf \
    %{buildroot}/etc/modules-load.d/sm8550-audio.conf
install -D -m 0644 etc/systemd/system/sm8550-audio-init.service \
    %{buildroot}%{_unitdir}/sm8550-audio-init.service

%post
%systemd_post sm8550-audio-init.service

%preun
%systemd_preun sm8550-audio-init.service

%postun
%systemd_postun_with_restart sm8550-audio-init.service

%files
%{_libexecdir}/sm8550-audio-init.sh
/etc/modules-load.d/sm8550-audio.conf
%{_unitdir}/sm8550-audio-init.service

%changelog
* Fri Sep 11 2026 opencode <opencode@localhost> - 1.0-1
- Merge SM8550 sound card bring-up (soundwire/wcd938x/lpass modules + oneshot init)