#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="enercoos"
iso_label="ENERCO_$(date +%Y%m)"
iso_publisher="PT Mega Tama Enerco <https://org.megatama-enerco.com>"
iso_application="EnercoOS Enterprise Workstation"
iso_version="$(date +%Y.%m.%d)"
install_dir="arch"
build_modes=('iso')
bootmodes=('bios.syslinux' 'uefi.systemd-boot')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M' '-Xdict-size' '1M')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/etc/sudoers.d"]="0:0:750"
  ["/etc/sudoers.d/00-liveuser"]="0:0:440"
  ["/etc/profile.d/enerco-autostart.sh"]="0:0:755"
  ["/etc/zprofile"]="0:0:644"
  ["/usr/local/bin/enerco-live-init"]="0:0:755"
  ["/usr/local/bin/nautilus"]="0:0:755"
  ["/home/enerco"]="1000:1000:755"
)
