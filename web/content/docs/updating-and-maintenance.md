---
title: "System Updates & Workstation Maintenance"
description: "Comprehensive guide for updating EnercoOS workstations with pacman, upgrading to native MacShell Spotlight & universal macOS window traffic lights on installed devices, managing dual kernels, and inspecting diagnostics."
category: "Operations & Administration"
order: 5
updatedAt: "2026-11-10"
---

## 1. Upgrading Installed Devices (Spotlight, Window Controls, Software Update)

Existing EnercoOS workstations can be updated to the latest release—gaining the **native Liquid Glass Spotlight**, **universal macOS window traffic lights**, and the **macOS Software Update center**—without reinstalling the operating system.

### Option A: Offline Update from USB Drive (Recommended for Air-Gapped Workstations)

If your installed workstation is offline, you can update directly using any USB drive:

1. Copy the updated package files (`localrepo/*.pkg.tar.zst` or from the live USB) to a flash drive.
2. Insert the USB flash drive into the installed workstation.
3. Open **Software Update** from the Apple menu (`M` logo → **Software Update…**) or run `enerco-update` in terminal:
   ```bash
   enerco-update
   ```
4. `enerco-update` automatically detects the packages on the USB drive (`/run/media/...`), runs `pacman -U`, migrates your user configuration, and live-reloads MacShell without rebooting!

You can also run a direct one-liner in terminal:
```bash
sudo pacman -U /run/media/$USER/*/*.pkg.tar.zst && enerco-update
```

---

### Option B: Online One-Click Software Update

If your workstation is connected to the internet or enterprise network:

1. Click the Apple menu (`M` logo in the top-left) → **Software Update…**.
2. Click **Install Now**.
3. EnercoOS will download the latest packages, migrate configs, and reload the desktop automatically.

---

### Option C: Step-by-Step Manual Upgrade

### Step 1: Upgrade System Packages & Install `cliphist`

Open **Terminal** (`Super + Return` or `kitty`) and update your packages:

```bash
# Synchronize repositories and upgrade all core packages
sudo pacman -Syu

# Install cliphist (required for Spotlight clipboard history with thumbnail previews)
sudo pacman -S --needed cliphist
```

> [!NOTE]
> Ensure `enerco-macshell >= 1.0.0-6` and `enerco-desktop-config >= 1.0.0-24` are installed. Check with:
> `pacman -Q enerco-macshell enerco-desktop-config`

---

### Step 2: Switch to Native Liquid Glass Spotlight

To switch from legacy Rofi to the native Liquid Glass Spotlight in your existing user profile:

```bash
# Set launcher to empty string in MacBar configuration (enables native MacSpot)
sed -i 's/"launcher": "rofi -show drun"/"launcher": ""/' ~/.config/macbar/settings.json

# If not present, add it directly:
# jq '.launcher = ""' ~/.config/macbar/settings.json > /tmp/s.json && mv /tmp/s.json ~/.config/macbar/settings.json
```

In `~/.config/macdock/pinned.json`, replace `"rofi"` with `"chromium"` so the dock displays standard apps:

```bash
sed -i 's/"rofi"/"chromium"/' ~/.config/macdock/pinned.json
```

---

### Step 3: Enable Universal macOS Traffic Lights (`WindowDecor`)

Create or update `~/.config/macbar/windecor.json` to enable macOS titlebars and traffic lights on all windows:

```bash
mkdir -p ~/.config/macbar
cat << 'EOF' > ~/.config/macbar/windecor.json
{
  "enabled": true,
  "showTitle": true,
  "radius": 10,
  "excludeClasses": [
    "org.quickshell",
    "quickshell"
  ]
}
EOF
```

Configure **Kitty Terminal** so it cleanly integrates with the new macOS window frames:

```bash
mkdir -p ~/.config/kitty
grep -q "hide_window_decorations" ~/.config/kitty/kitty.conf 2>/dev/null || \
  echo "hide_window_decorations yes" >> ~/.config/kitty/kitty.conf
```

---

### Step 4: Update Hyprland Keybindings & Layer Rules

In `~/.config/hypr/hyprland.lua`, ensure the Spotlight and clipboard shortcuts are bound:

```lua
-- Application Launchers
local menu = "qs -c MacShell ipc call spotlight toggle"
hl.bind(mainMod .. " + space",      hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + V",          hl.dsp.exec_cmd("qs -c MacShell ipc call spotlight clipboard"))
hl.bind(mainMod .. " + PERIOD",     hl.dsp.exec_cmd("qs -c MacShell ipc call spotlight emoji"))
hl.bind(mainMod .. " + SHIFT + V",  hl.dsp.window.float({ action = "toggle" }))
hl.bind("ALT + Tab",                hl.dsp.exec_cmd("qs -c MacShell ipc call switcher next"))
hl.bind(mainMod .. " + Tab",        hl.dsp.exec_cmd("qs -c MacShell ipc call switcher next"))

-- Layer Rules
hl.layer_rule({ name = "blur-macspot", match = { namespace = "macspot" }, blur = true, ignore_alpha = 0.05 })
hl.layer_rule({ name = "macwindecor",  match = { namespace = "macwindecor" }, no_anim = true })
```

---

### Step 5: Reload Desktop Services (No Reboot Required)

Apply all configuration updates immediately without restarting your machine:

```bash
# Reload Hyprland keybindings and layer rules
hyprctl reload

# Restart MacShell to load the WindowDecor layer and native Spotlight
pkill -f quickshell || true
setsid /usr/local/bin/macshell-start >/dev/null 2>&1 &
```

You can now use `Super + Space` for Spotlight, `Super + V` for Clipboard History, and click or drag the traffic lights on any window.

---

## 2. Standard Package Management (`pacman`)

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
