# EnercoOS — Enterprise Workstation Distribution

[![License: GPL v3+](https://img.shields.io/badge/License-GPL%20v3%2B-blue.svg)](LICENSE)
[![Architecture: x86_64](https://img.shields.io/badge/Arch-x86__64%20UEFI%2FBIOS-0071e3.svg)](profiledef.sh)
[![Portal: org.megatama-enerco.com](https://img.shields.io/badge/Portal-org.megatama--enerco.com-312e59.svg)](https://org.megatama-enerco.com)

**EnercoOS** is an open-source, production-grade Arch Linux enterprise workstation distribution developed by **PT Mega Tama Enerco** ([org.megatama-enerco.com](https://org.megatama-enerco.com)).

It combines a modern **Enerco Liquid Glass** Wayland desktop powered by **Hyprland** and **MacShell (Quickshell)** with out-of-the-box **MTERP ERP** integration ([mterp.megatama-enerco.com](https://mterp.megatama-enerco.com)), automated **Calamares** disk installation, hardware-aware GPU/VM session management, and enterprise kernel/security hardening.

---

## 1. Key Capabilities

- **Enerco Liquid Glass Desktop (`Hyprland` + `MacShell`):**
  - Native Qt6/QML Wayland shell (`qs -c MacShell`) providing the top menu bar (`MacBar`), auto-hiding dock (`MacDock`), application/clipboard/emoji search (`MacSpot`), notification center & OSD (`MacNotif`), and frosted-glass screen locker (`MacLock`).
  - Pure **PT Mega Tama Enerco** visual identity with zero third-party trademark glyphs.
- **Enterprise ERP & Office Productivity Suite:**
  - Dedicated **MTERP ERP** Wayland web app launcher (`enerco-mterp` -> `https://mterp.megatama-enerco.com`), **LibreOffice Fresh**, **Evince** PDF viewer, **Loupe** image viewer, **Mousepad** text editor, **Thunar** file manager, and **Kitty** terminal.
- **Smart Hardware & Hypervisor Session Wrapper (`enerco-session`):**
  - Automatically detects bare-metal GPUs (Intel, AMD, NVIDIA) vs. virtualized hypervisors (VirtualBox, VMware, QEMU/KVM, Hyper-V) and applies the appropriate Wayland/DRM/Mesa flags dynamically.
- **Turnkey Graphical Installer (`Calamares 3.3.11`):**
  - Supports UEFI (`systemd-boot` / `GRUB` with EFI fallback) and BIOS installations, multi-kernel (`linux` and `linux-zen`) initramfs generation, automatic live-artifact cleanup, and out-of-the-box target `SDDM` Wayland login.
- **Performance & Endpoint Security:**
  - Dual-kernel support (`linux` + `linux-zen`), ZRAM compressed swap (`zram-generator`), I/O scheduler & SATA/NVMe udev tuning, and `UFW` host firewall pre-configured for enterprise deployments.

---

## 2. Standard Arch Packaging Architecture

EnercoOS packages all custom configurations, branding, desktop shell components, and enterprise tools as standard Arch Linux **`PKGBUILD`** recipes inside [`pkgs/`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs), compiled into [`localrepo/`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/localrepo) via [`scripts/build-packages.sh`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/scripts/build-packages.sh):

| Package | Version | License | Description |
| :--- | :--- | :--- | :--- |
| [`enerco-branding`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-branding/PKGBUILD) | `1.0.0-7` | `GPL-3.0-or-later` | PT Mega Tama Enerco corporate SVG emblems, wallpapers, `/etc/os-release`, and `/etc/issue` |
| [`enerco-macshell`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-macshell/PKGBUILD) | `1.0.0-4` | `GPL-3.0-or-later` | EnercoOS Liquid Glass shell (`MacShell` + `MacLock`), supervisor (`macshell-start`), and corporate branding |
| [`macos-like-icon-theme`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/macos-like-icon-theme/PKGBUILD) | `1.0.0-1` | `GPL-3.0-or-later` | High-DPI vector icon theme (`MacOS-Like` / `MacOS-Like-Dark`) for GTK, Qt, and Quickshell |
| [`enerco-desktop-config`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-desktop-config/PKGBUILD) | `1.0.0-22` | `GPL-3.0-or-later` | Hyprland Lua configuration (`hyprland.lua`), `hypridle`, `hyprlock`, Rofi, Kitty, GTK3/4, Zsh, and SDDM Wayland config |
| [`enerco-enterprise-tools`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-enterprise-tools/PKGBUILD) | `1.0.0-17` | `GPL-3.0-or-later` | `enerco-session`, `enerco-mterp`, `enerco-installer`, `enerco-welcome`, `enerco-lockdown`, ZRAM, udev, and sysctl tuning |
| [`calamares`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/calamares/PKGBUILD) | `3.3.11-2` | `GPL-3.0-or-later` | Qt6/KDE Frameworks 6 compilation of the Calamares system installer |
| [`enerco-calamares-config`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-calamares-config/PKGBUILD) | `1.0.0-19` | `GPL-3.0-or-later` | Calamares module sequence, partitioning, bootloader, systemd service enablement, and PT Mega Tama Enerco branding |

---

## 3. Repository Layout

```text
EnercoOS/
├── .gitattributes                         # Enforces LF line endings for all Linux scripts & configs
├── .gitignore                             # Excludes build workdirs, ISO binaries, and package archives
├── .wslconfig                             # Host WSL 2 memory and swap configuration
├── LICENSE                                # GNU General Public License v3.0
├── README.md                              # Project documentation, credits, and license information
├── build.sh                               # Unified root ISO build entrypoint (makepkg + mkarchiso)
├── profiledef.sh                          # Archiso profile metadata and file permissions
├── packages.x86_64                        # Package manifest for live and installed systems
├── pacman.conf                            # Pacman repository configuration with localrepo mapping
├── efiboot/                               # UEFI systemd-boot entries
├── syslinux/                              # BIOS syslinux bootloader entries
├── pkgs/                                  # Standard Arch PKGBUILD recipes
│   ├── calamares/
│   ├── enerco-branding/
│   ├── enerco-calamares-config/
│   ├── enerco-desktop-config/
│   ├── enerco-enterprise-tools/
│   ├── enerco-macshell/
│   └── macos-like-icon-theme/
├── scripts/
│   ├── build-packages.sh                  # Incremental makepkg & repo-add builder
│   ├── run-qemu.sh                        # Rapid QEMU UEFI test runner
│   └── sync-to-vm.sh                      # Workspace synchronization helper
├── airootfs/                              # Live ISO root filesystem overlay
└── tests/                                 # 185 automated Tier 1–4 E2E verification tests
```

---

## 4. Building & Testing EnercoOS

### Prerequisites (Arch Linux or WSL 2 Arch Linux)
```bash
sudo pacman -Syu --noconfirm archiso base-devel git squashfs-tools libisoburn dosfstools mtools lynx librsvg python
```

### Build the Bootable ISO
```bash
# Build modified packages as non-root user and generate dist/enercoos-YYYY.MM.DD-x86_64.iso
sudo ./build.sh

# Force a full rebuild of all in-tree packages before generating the ISO
sudo ./build.sh --rebuild-pkgs
```

### Run the Automated E2E Test Suite
```bash
python tests/runner.py
```

---

## 5. Default Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Super + Space` | Open **Enerco Search** (`MacSpot` Apps, Files, Clipboard & Emoji) |
| `Super + Return` | Launch **Kitty** Terminal |
| `Super + E` | Open **Thunar** File Manager |
| `Super + B` | Launch **Chromium** Browser |
| `Super + M` | Launch **MTERP ERP** (`https://mterp.megatama-enerco.com`) |
| `Super + I` | Launch **Install EnercoOS** (`Calamares`) |
| `Super + W` / `Super + Q` | Close Active Window |
| `Super + L` | Lock Workstation (`MacLock` / `hyprlock`) |
| `Super + F11` / `F10` / `F9` / `F8` | Switch Display Resolution (`1080p` / `768p` / `800p` / `Auto`) |
| `Super + 1..6` | Switch Workspace `1..6` |

---

## 6. Third-Party Open-Source Acknowledgements

EnercoOS stands on the shoulders of the open-source community. We gratefully acknowledge and credit the following upstream projects and authors whose work powers this distribution:

| Component | Upstream Project / Author | Upstream License | Usage in EnercoOS |
| :--- | :--- | :--- | :--- |
| **Arch Linux & `archiso`** | [Arch Linux Project](https://archlinux.org) / [archiso](https://gitlab.archlinux.org/archlinux/archiso) | `GPL-2.0-only` / `GPL-3.0-or-later` | Base distribution, package ecosystem, and live ISO build tooling |
| **Linux Kernel (`linux` / `linux-zen`)** | [Linus Torvalds & Linux Kernel Contributors](https://www.kernel.org) | `GPL-2.0-only` | Operating system kernel and hardware drivers |
| **Hyprland, `hyprlock`, `hypridle`** | [Vaxry & Hypr Development](https://github.com/hyprwm/Hyprland) | `BSD-3-Clause` | Dynamic tiling/floating Wayland compositor, Lua configuration engine, and idle/lock management |
| **Quickshell (`quickshell`)** | [Outfoxxed & Quickshell Contributors](https://github.com/quickshell-mirror/quickshell) | `LGPL-3.0-only` / `GPL-3.0-only` | Qt6/QML Wayland desktop shell toolkit |
| **MacShell & MacLock** | [0-ss/MacShell](https://github.com/0-ss/MacShell) (`0-ss`, `vsoultann`) | `GPL-3.0-or-later` | Liquid Glass QML top menu bar, dock, search, notifications, and lock screen (customized with PT Mega Tama Enerco branding in [`pkgs/enerco-macshell`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-macshell)) |
| **MacOS-Like Icon Theme** | [Scrimas/MacOS-Like](https://github.com/Scrimas/MacOS-Like) (`Scrimas`) | `GPL-3.0-or-later` | Application and system icon theme packaged in [`pkgs/macos-like-icon-theme`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/macos-like-icon-theme) |
| **Open Runde Font** | [lauridskern/open-runde](https://github.com/lauridskern/open-runde) (Laurids Kern) / [Inter](https://rsms.me/inter/) (Rasmus Andersson) | `OFL-1.1` | Rounded UI typography for the desktop shell |
| **Calamares Installer** | [Calamares Team](https://github.com/calamares/calamares) | `GPL-3.0-or-later` | Graphical system installer framework packaged in [`pkgs/calamares`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/calamares) |
| **CachyOS Sysctl & Udev Tuning** | [CachyOS Team](https://github.com/CachyOS/CachyOS-Settings) | `GPL-3.0-only` | Kernel sysctl, I/O scheduler, and ZRAM performance tuning parameters in [`pkgs/enerco-enterprise-tools`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-enterprise-tools) |
| **Capitaine Cursors** | [keeferrourke/capitaine-cursors](https://github.com/keeferrourke/capitaine-cursors) (Keefer Rourke) | `LGPL-3.0-only` | Vector cursor theme |
| **Desktop & System Stack** | `SDDM`, `Weston`, `PipeWire`, `WirePlumber`, `NetworkManager`, `BlueZ`, `Blueman`, `Rofi`, `Kitty`, `Thunar`, `LibreOffice`, `Chromium`, `Evince`, `Loupe`, `Mousepad` | Respective Upstream OSS Licenses (`GPL`, `LGPL`, `MPL-2.0`, `BSD`, `MIT`) | Display management, audio, networking, Bluetooth, and office productivity applications |

All upstream packages distributed within an EnercoOS ISO image retain their original upstream licenses, copyright notices, and source attribution as recorded in `/usr/share/licenses/` on the live and installed system.

---

## 7. License & Trademark Disclaimer

### Open-Source Software License (`GPL-3.0-or-later`)
Copyright (C) 2026 **PT Mega Tama Enerco** (<https://org.megatama-enerco.com>).

All original scripts, `PKGBUILD` recipes, configuration files, and modifications in this repository are free and open-source software licensed under the **GNU General Public License v3.0 or later (`GPL-3.0-or-later`)**. See the [LICENSE](file:///c:/Users/CorSec/Documents/personal/EnercoOS/LICENSE) file for the full license text.

### Corporate Branding & Third-Party Trademark Notice
- **PT Mega Tama Enerco**, the **PT Mega Tama Enerco (`M`)** corporate emblem ([`enerco-logo.svg`](file:///c:/Users/CorSec/Documents/personal/EnercoOS/pkgs/enerco-branding/enerco-logo.svg)), **EnercoOS**, and **MTERP** are trademarks or service marks of **PT Mega Tama Enerco**.
- **Linux®** is the registered trademark of Linus Torvalds in the U.S. and other countries.
- **Arch Linux™** is a recognized trademark of Arch Linux Project / Levente Polyák.
- **macOS®**, **Apple®**, and **Finder®** (where referenced in upstream technical documentation or compatibility identifiers) are trademarks of Apple Inc., registered in the U.S. and other countries.
- **EnercoOS is an independent open-source enterprise Linux distribution developed by PT Mega Tama Enerco and is not affiliated with, endorsed by, or sponsored by Arch Linux, Apple Inc., or any other third-party trademark holder.**
