---
title: "Arch Packaging & PKGBUILD Architecture"
description: "Deep dive into EnercoOS's modular Arch Linux PKGBUILD repository structure, localrepo indexing, smart session wrapper, and automated E2E test suite."
category: "Engineering"
order: 4
updatedAt: "2026-11-07"
---

## Modular In-Tree `PKGBUILD` Design

Rather than cluttering `airootfs/` with untracked loose files, EnercoOS packages all custom branding, desktop shell components, installer configurations, and enterprise tools as standard Arch Linux **`PKGBUILD`** recipes inside `pkgs/`.

When `sudo ./build.sh` runs, it drops privileges to a non-root builder user and executes `scripts/build-packages.sh`, which compiles each package via `makepkg` and indexes the resulting `.pkg.tar.zst` archives into `localrepo/enerco-local.db.tar.gz`.

| Package Directory | Version | Installed Paths & Role |
| :--- | :--- | :--- |
| `pkgs/enerco-branding` | `1.0.0-8` | `/usr/share/backgrounds/enerco-mac.png`, `/usr/share/pixmaps/enerco-logo.svg`, `/etc/os-release`, `/etc/issue` |
| `pkgs/enerco-macshell` | `1.0.0-5` | `/etc/skel/.config/quickshell/MacShell`, `/etc/xdg/quickshell/MacShell`, `/usr/local/bin/macshell-start`, `/usr/local/bin/maclock`, `brand-enerco.py` corporate branding |
| `pkgs/macos-like-icon-theme` | `1.0.0-1` | `/usr/share/icons/MacOS-Like` and `/usr/share/icons/MacOS-Like-Dark` vector icon themes |
| `pkgs/enerco-desktop-config` | `1.0.0-23` | `/etc/skel/.config/hypr/hyprland.lua`, `/etc/sddm.conf.d/10-enerco.conf`, `/usr/share/wayland-sessions/enerco.desktop`, Kitty, Rofi, GTK3/4, Zsh configs |
| `pkgs/enerco-enterprise-tools` | `1.0.0-17` | `/usr/local/bin/enerco-session`, `enerco-mterp`, `enerco-installer`, `enerco-welcome`, `enerco-lockdown`, ZRAM (`zram-generator.conf`), udev I/O rules, and CachyOS sysctl tuning |
| `pkgs/calamares` | `3.3.11-2` | Native Qt6 / KDE Frameworks 6 compilation of the Calamares graphical system installer |
| `pkgs/enerco-calamares-config` | `1.0.0-19` | `/etc/calamares/settings.conf`, `modules/*.conf` (`partition`, `users`, `displaymanager`, `services-systemd`, `shellprocess`), and `/etc/calamares/branding/enerco/` |

---

## Smart Session Wrapper (`enerco-session`)

Both the live ISO (`enerco-autostart.sh`) and the installed SDDM Wayland session (`/usr/share/wayland-sessions/enerco.desktop`) launch Hyprland through `/usr/local/bin/enerco-session`.

`enerco-session` inspects `systemd-detect-virt`, `lspci`, and `/sys/class/dmi/id/` at login:

```bash
# Virtual Machine optimizations (VirtualBox VMSVGA / VMware SVGA / QEMU VirtIO)
if [[ "${VIRT_TYPE}" =~ (oracle|vmware|microsoft|qemu|kvm) ]]; then
    export WLR_NO_HARDWARE_CURSORS=1
    export WLR_RENDERER_ALLOW_SOFTWARE=1
    export AQ_NO_MODIFIERS=1
    export LIBGL_ALWAYS_SOFTWARE=1
fi
```

- **On VirtualBox / VMware / QEMU:** Automatically enables software rendering fallbacks (`LIBGL_ALWAYS_SOFTWARE=1`, `AQ_NO_MODIFIERS=1`, `WLR_NO_HARDWARE_CURSORS=1`) so Hyprland and Quickshell render smoothly even with 3D acceleration disabled.
- **On Bare-Metal NVIDIA / Intel / AMD GPUs:** Applies hardware VA-API and DRM modifiers (`GBM_BACKEND=nvidia-drm` on NVIDIA, `LIBVA_DRIVER_NAME=iHD` on Intel) for full 60–144Hz GPU acceleration.

---

## Automated 4-Tier Verification Suite (`tests/`)

Every configuration contract in EnercoOS is guarded by **185 automated Python E2E tests** across four tiers:

```bash
python tests/runner.py
```

- **Tier 1 (`tests/tier1/`):** Core functional contracts (16 features × 5+ tests).
- **Tier 2 (`tests/tier2/`):** Boundary, security, and regression tests (e.g., ensuring no undefined Calamares `$` variables in `shellprocess.conf`, no `layer-shell` conflict in `sddm-enerco.conf`, and LF line endings in `.gitattributes`).
- **Tier 3 (`tests/tier3/`):** Cross-feature integration checks (`Calamares` ↔ `SDDM` ↔ `enerco-session` ↔ `MacShell`).
- **Tier 4 (`tests/tier4/`):** End-to-end build pipeline, live session, installation, and post-install boot scenarios.
