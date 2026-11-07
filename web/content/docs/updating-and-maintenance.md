---
title: "System Updates & Workstation Maintenance"
description: "Guide for updating EnercoOS workstations with pacman, managing dual kernels (linux-zen and linux), verifying ZRAM swap, and inspecting session logs."
category: "Operations & Administration"
order: 5
updatedAt: "2026-11-07"
---

## 1. Updating EnercoOS Packages (`pacman`)

EnercoOS uses the standard Arch Linux package manager (`pacman`) alongside the on-system `enerco-local` repository (`/var/cache/enerco-repo`).

### Performing a Full System Upgrade

Open **Kitty Terminal** (`Super + Return`) and run:

```bash
sudo pacman -Syu
```

This synchronizes all enabled repositories (`enerco-local`, `core`, `extra`) and upgrades installed packages in a single atomic transaction.

### Cleaning the Package Cache

To reclaim disk space while keeping the two most recent package versions for safe rollback:

```bash
sudo paccache -rk2
```

---

## 2. Managing Dual Kernels (`linux-zen` & `linux`)

Every EnercoOS workstation installs two kernels into `/boot` and registers both in `GRUB`:

1. **`linux-zen` (`vmlinuz-linux-zen`):** Default low-latency desktop kernel tuned for interactive Wayland responsiveness.
2. **`linux` (`vmlinuz-linux`):** Mainline LTS/fallback kernel for maximum hardware compatibility.

To regenerate all `mkinitcpio` initramfs images and update the GRUB boot menu after modifying `/etc/mkinitcpio.conf` or `/etc/default/grub`:

```bash
sudo mkinitcpio -P
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

---

## 3. Verifying ZRAM Swap & I/O Scheduler Tuning

EnercoOS configures compressed `zstd` in-memory swap via `systemd-zram-generator` (`/etc/systemd/zram-generator.conf`) and applies CachyOS-inspired `udev` I/O scheduler rules (`/etc/udev/rules.d/60-enerco-ioschedulers.rules`).

Check active ZRAM compression ratio and swap status:

```bash
zramctl
swapon --show
```

Check active block device I/O schedulers (`none`/`kyber` on NVMe, `mq-deadline`/`bfq` on SSD/HDD):

```bash
cat /sys/block/*/queue/scheduler
```

---

## 4. Troubleshooting Desktop Session & Display Logs

If a display or GPU issue occurs, `enerco-session` and `enerco-macshell` write structured diagnostics that can be inspected from any terminal or TTY (`Ctrl + Alt + F3`):

| Component | Diagnostic Command |
| :--- | :--- |
| **SDDM Display Manager** | `journalctl -u sddm -b --no-pager` |
| **MacShell Supervisor & Quickshell** | `cat ~/.local/state/enerco-macshell.log` |
| **Hyprland Compositor** | `hyprctl systeminfo` |
| **NetworkManager & DNS** | `nmcli general status && journalctl -u NetworkManager -b` |

To restart the Liquid Glass shell (`MacBar`, `MacDock`, `MacSpot`) inside an active session without logging out:

```bash
enerco-macshell --reload
```
