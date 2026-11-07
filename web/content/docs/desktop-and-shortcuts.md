---
title: "Liquid Glass Desktop & Shortcuts"
description: "Complete guide to the EnercoOS Liquid Glass Wayland shell (MacShell + Hyprland), display resolution hotkeys, and enterprise keyboard shortcuts."
category: "User Guide"
order: 3
updatedAt: "2026-11-07"
---

## The Enerco Liquid Glass Architecture

EnercoOS uses a pure **Qt6 / QML Wayland shell** (`qs -c MacShell` via `Quickshell 0.3.2`) running on top of **Hyprland 0.57.1** (configured via `/etc/skel/.config/hypr/hyprland.lua`). Legacy status bars (`waybar`) and redundant notification daemons have been completely removed so the entire desktop runs inside a single unified Quickshell process:

- **Top Menu Bar (`MacBar`):** Displays the **PT Mega Tama Enerco (`M`)** system menu, active application global menu (`File`, `Edit`, `View`, `Window`, `Help`), workspace indicator, system tray, Wi-Fi/Bluetooth/Audio controls, battery status, Control Center popover, and clock.
- **Floating Auto-Hide Dock (`MacDock`):** Liquid Glass dock with icon magnification, live window thumbnail previews, running app indicators, and Trash management.
- **Enerco Search (`MacSpot`):** Instant application launcher, file finder, clipboard history manager, and emoji picker (`Super + Space`).
- **Frosted Screen Locker (`MacLock`):** Hardware-accelerated Wayland session lock (`Super + L` or `/usr/local/bin/maclock`).

---

## Default Keyboard Shortcuts (`hyprland.lua`)

Here is the complete keyboard reference configured out of the box in `~/.config/hypr/hyprland.lua`:

| Shortcut | Action | Command / Dispatcher |
| :--- | :--- | :--- |
| `Super + Space` | Open **Enerco Search** (`MacSpot`) | `qs -c MacShell ipc call spotlight toggle \|\| rofi -show drun` |
| `Super + .` (Period) | Open **Emoji Picker** | `qs -c MacShell ipc call spotlight emoji` |
| `Super + Z` | Open **Desktop & Dock Settings** | `qs -c MacShell ipc call settings toggle` |
| `Super + Return` | Launch **Kitty** Terminal | `kitty` |
| `Super + E` | Open **Thunar** File Manager | `thunar` |
| `Super + B` | Launch **MTERP Enterprise Portal** | `/usr/local/bin/enerco-mterp` (`https://mterp.megatama-enerco.com`) |
| `Super + I` | Launch **Install EnercoOS** (`Calamares`) | `/usr/local/bin/enerco-installer` |
| `Super + W` / `Super + Q` | Close Active Window | `hl.dsp.window.close()` |
| `Super + V` | Toggle Floating Window Mode | `hl.dsp.window.float({ action = "toggle" })` |
| `Super + J` | Toggle Split Direction | `hl.dsp.layout("togglesplit")` |
| `Super + D` | Show Desktop (Special Workspace) | `hyprctl dispatch togglespecialworkspace` |
| `Super + Tab` | Switch Open Windows | `rofi -show window` |
| `Super + L` | Lock Workstation Screen | `/usr/local/bin/maclock` |
| `Super + Shift + S` | Area Screenshot to Clipboard | `grim -g "$(slurp)" - \| wl-copy` |
| `Super + Shift + W` | Restart MacShell Supervisor | `/usr/local/bin/macshell-start &` |
| `Super + M` | Exit Hyprland Session | `hl.dsp.exit()` |

---

## Display & Virtual Machine Resolution Hotkeys

When running in VirtualBox, QEMU, or multi-monitor setups, you can switch the active display resolution on the fly without opening a terminal:

| Shortcut | Target Resolution | Hyprland Keyword |
| :--- | :--- | :--- |
| `Super + F11` | **1920 × 1080 @ 60Hz** (Full HD) | `hyprctl keyword monitor ',1920x1080@60,auto,1'` |
| `Super + F10` | **1366 × 768 @ 60Hz** (Laptop HD) | `hyprctl keyword monitor ',1366x768@60,auto,1'` |
| `Super + F9` | **1280 × 800 @ 60Hz** (Compact WXGA) | `hyprctl keyword monitor ',1280x800@60,auto,1'` |
| `Super + F8` | **Native / Preferred Monitor Mode** | `hyprctl keyword monitor ',preferred,auto,1'` |

---

## Workspace & Hardware Media Keys

- **Switch Workspace `1–10`:** `Super + 1` through `Super + 0`
- **Move Window to Workspace `1–10`:** `Super + Shift + 1` through `Super + Shift + 0`
- **Mouse Drag / Resize Window:** Hold `Super` + **Left Click Drag** (move) or **Right Click Drag** (resize)
- **Audio Volume (`PipeWire` / `WirePlumber`):** `XF86AudioRaiseVolume`, `XF86AudioLowerVolume`, `XF86AudioMute`, `XF86AudioMicMute`
- **Backlight Brightness (`brightnessctl`):** `XF86MonBrightnessUp`, `XF86MonBrightnessDown`
