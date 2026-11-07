---
title: "Open Source License & Credits"
description: "GNU GPL v3.0 licensing, third-party open-source attributions, and PT Mega Tama Enerco corporate trademark policy."
category: "Operations & Deployment"
order: 7
updatedAt: "2026-11-07"
---

## Open-Source Software License (`GPL-3.0-or-later`)

Copyright © 2026 **PT Mega Tama Enerco** ([org.megatama-enerco.com](https://org.megatama-enerco.com)).

All original scripts, `PKGBUILD` recipes, configuration files, and modifications in the **EnercoOS** repository are free and open-source software licensed under the **GNU General Public License v3.0 or later (`GPL-3.0-or-later`)**.

You are free to inspect, modify, redistribute, and build upon the source code under the terms of the GNU GPL v3.0.

---

## Third-Party Open-Source Acknowledgements

EnercoOS stands on the shoulders of the open-source community. We gratefully acknowledge and credit the following upstream projects and authors whose work powers this distribution:

| Component | Upstream Project & Authors | License | Role in EnercoOS |
| :--- | :--- | :--- | :--- |
| **Arch Linux & `archiso`** | [Arch Linux Project](https://archlinux.org) / [archiso](https://gitlab.archlinux.org/archlinux/archiso) | `GPL-2.0-only` / `GPL-3.0-or-later` | Base distribution, package ecosystem, and live ISO build tooling |
| **Linux Kernel (`linux` / `linux-zen`)** | [Linus Torvalds & Linux Kernel Contributors](https://www.kernel.org) | `GPL-2.0-only` | Operating system kernel and hardware drivers |
| **Hyprland, `hyprlock`, `hypridle`** | [Vaxry & Hypr Development](https://github.com/hyprwm/Hyprland) | `BSD-3-Clause` | Dynamic tiling/floating Wayland compositor, Lua config engine, and idle/lock management |
| **Quickshell (`quickshell`)** | [Outfoxxed & Quickshell Contributors](https://github.com/quickshell-mirror/quickshell) | `LGPL-3.0-only` / `GPL-3.0-only` | Qt6/QML Wayland desktop shell toolkit |
| **MacShell & MacLock** | [0-ss/MacShell](https://github.com/0-ss/MacShell) (`0-ss`, `vsoultann`) | `GPL-3.0-or-later` | Liquid Glass QML top menu bar, dock, search, notifications, and lock screen (customized with PT Mega Tama Enerco branding in `pkgs/enerco-macshell`) |
| **MacOS-Like Icon Theme** | [Scrimas/MacOS-Like](https://github.com/Scrimas/MacOS-Like) (`Scrimas`) | `GPL-3.0-or-later` | High-DPI vector application and system icon theme (`pkgs/macos-like-icon-theme`) |
| **Open Runde & Inter Fonts** | [Laurids Kern (`open-runde`)](https://github.com/lauridskern/open-runde) / [Rasmus Andersson (`Inter`)](https://rsms.me/inter/) | `OFL-1.1` | UI typography for the desktop shell and system interfaces |
| **Calamares Installer** | [Calamares Team](https://github.com/calamares/calamares) | `GPL-3.0-or-later` | Graphical system installer framework (`pkgs/calamares`) |
| **CachyOS Sysctl & Udev Tuning** | [CachyOS Team](https://github.com/CachyOS/CachyOS-Settings) | `GPL-3.0-only` | Kernel sysctl, I/O scheduler, and ZRAM tuning parameters (`pkgs/enerco-enterprise-tools`) |
| **Capitaine Cursors** | [Keefer Rourke (`capitaine-cursors`)](https://github.com/keeferrourke/capitaine-cursors) | `LGPL-3.0-only` | Vector cursor theme |
| **Desktop & System Stack** | `SDDM`, `Weston`, `PipeWire`, `WirePlumber`, `NetworkManager`, `BlueZ`, `Blueman`, `Rofi`, `Kitty`, `Thunar`, `LibreOffice`, `Chromium`, `Evince`, `Loupe`, `Mousepad` | Respective Upstream OSS Licenses (`GPL`, `LGPL`, `MPL-2.0`, `BSD`, `MIT`) | Display management, audio, networking, Bluetooth, and office productivity applications |

All upstream packages distributed within an EnercoOS ISO image retain their original upstream licenses, copyright notices, and source attribution in `/usr/share/licenses/`.

---

## Corporate Branding & Trademark Notice

- **PT Mega Tama Enerco**, the **PT Mega Tama Enerco (`M`)** corporate emblem (`enerco-logo.svg`), **EnercoOS**, and **MTERP** are trademarks or service marks of **PT Mega Tama Enerco**.
- **Linux®** is the registered trademark of Linus Torvalds in the U.S. and other countries.
- **Arch Linux™** is a recognized trademark of Arch Linux Project / Levente Polyák.
- **Apple®**, **macOS®**, **MacBook®**, **AppleCare®**, **Finder®**, and **Spotlight®** are registered trademarks of Apple Inc. **EnercoOS and PT Mega Tama Enerco are independent and are not affiliated with, endorsed by, or sponsored by Apple Inc. or the Arch Linux Project.** All third-party trademark symbols and logos have been excluded from the EnercoOS user interface in favor of pure PT Mega Tama Enerco corporate branding.
