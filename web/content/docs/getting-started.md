---
title: "Overview & System Requirements"
description: "Introduction to EnercoOS 2026 Enterprise Workstation, key architectural capabilities, hardware requirements, and MTERP integration."
category: "Fundamentals"
order: 1
updatedAt: "2026-11-07"
---

## What is EnercoOS?

**EnercoOS** is an open-source (`GPL-3.0-or-later`), production-grade Arch Linux enterprise workstation distribution developed by **PT Mega Tama Enerco** ([org.megatama-enerco.com](https://org.megatama-enerco.com)).

It combines the **Enerco Liquid Glass** Wayland desktop powered by **Hyprland 0.57** and **MacShell (Quickshell 0.3)** with out-of-the-box **MTERP ERP** integration ([mterp.megatama-enerco.com](https://mterp.megatama-enerco.com)), automated **Calamares 3.3.11** disk installation, smart hardware/hypervisor GPU session wrapping (`enerco-session`), and CachyOS-inspired kernel/storage performance tuning.

---

## Core Workstation Capabilities

| Capability | Technical Implementation | Purpose |
| :--- | :--- | :--- |
| **Liquid Glass Desktop Shell** | `Hyprland 0.57.1` + `Quickshell 0.3.2` (`qs -c MacShell`) | Unified Qt6/QML top menu bar (`MacBar`), auto-hiding dock (`MacDock`), instant search (`MacSpot`), notification center (`MacNotif`), and frosted screen lock (`MacLock`) |
| **Pure Corporate Identity** | `enerco-branding` + `enerco-macshell` (`brand-enerco.py`) | Zero third-party trademark symbols; official PT Mega Tama Enerco (`M`) emblem across menu bar, lock screen, and system dialogs |
| **Enterprise ERP Suite** | `enerco-mterp` (Chromium Ozone Wayland App Mode) | Hardware-accelerated dedicated window for `https://mterp.megatama-enerco.com` plus LibreOffice Fresh, Evince, Loupe, Mousepad, Thunar, and Kitty |
| **Smart GPU & Hypervisor Wrapper** | `/usr/local/bin/enerco-session` | Dynamically detects Intel, AMD, and NVIDIA GPUs as well as VirtualBox (`VMSVGA`), VMware, QEMU/KVM, and Hyper-V guests |
| **Turnkey Disk Installer** | `Calamares 3.3.11` + `enerco-calamares-config` | Supports UEFI (`systemd-boot` / `GRUB` with EFI fallback) and BIOS installations with automatic dual-kernel initramfs generation |
| **Endpoint Performance & Security** | Dual kernels (`linux` + `linux-zen`), `zram-generator`, `ufw` | ZRAM zstd compressed swap, BFQ/kyber/none I/O udev rules, sysctl low-latency tuning, and host firewall rules |

---

## System Requirements

### Bare-Metal Workstation (`x86_64`)

- **Architecture:** 64-bit (`x86_64`) Intel Core / Xeon or AMD Ryzen / EPYC processor
- **Firmware:** UEFI 2.3+ (Secure Boot disabled) or Legacy BIOS / CSM
- **Memory (RAM):** Minimum `4 GB` RAM (`8 GB+` recommended for multi-window MTERP + LibreOffice workflows; ZRAM automatically provides compressed swap)
- **Storage:** Minimum `25 GB` NVMe SSD or SATA SSD (`64 GB+` recommended)
- **Graphics:** Intel UHD/Iris Xe/Arc (`iHD`), AMD Radeon (`radeonsi`), or NVIDIA GeForce/RTX (`nvidia-open` / `nouveau`) with Wayland KMS support

### Virtual Machine Guests (VirtualBox / QEMU / VMware)

- **Hypervisors Supported:** Oracle VirtualBox 7.x (`VMSVGA`), QEMU/KVM (`virtio-vga` / `qxl`), VMware Workstation/ESXi, Microsoft Hyper-V
- **VirtualBox Recommended Settings:**
  - **System -> Motherboard:** Enable EFI (`Enable I/O APIC` checked), `4096 MB`+ RAM, `2–4` vCPUs
  - **Display -> Screen:** Graphics Controller set to `VMSVGA`, Video Memory `128 MB` (EnercoOS also includes automatic `pixman` / `llvmpipe` fallback for `16 MB` VRAM guests without 3D acceleration)
  - **Storage:** `32 GB`+ Dynamic VDI/NVMe disk

---

## Live Session vs. Installed System

When booting from the `enercoos-2026.11.07-x86_64.iso` image:

1. **Live Evaluation & Installer Session (`enerco` user):**
   - Automatically logs in on `tty1` via `/etc/profile.d/enerco-autostart.sh` into `/usr/local/bin/enerco-session`.
   - Includes the **Install EnercoOS** (`Calamares`) desktop shortcut, dock pin, and welcome assistant (`enerco-welcome`).
2. **Installed Production Workstation:**
   - During installation, `shellprocess.conf` removes all live-only artifacts (`enerco` live user, autologin drop-ins, and `calamares.desktop` shortcuts), copies both `vmlinuz-linux` and `vmlinuz-linux-zen` kernels into `/boot`, regenerates `mkinitcpio -P`, and enables the `SDDM` Wayland login greeter (`weston --shell=kiosk --renderer=pixman`) for your configured enterprise user account.
