# Guide: Upgrading Installed EnercoOS Workstations

This guide provides step-by-step instructions for upgrading existing EnercoOS installations to use the **native Liquid Glass MacShell Spotlight** and the **universal macOS window controls (traffic lights)** across every application—including Terminal (`kitty`), Chromium, and standard windows—without reinstalling the OS.

---

## Prerequisites
- Working EnercoOS workstation with internet connectivity or access to the updated `enerco-local` repository.
- Root or sudo privileges.

---

## Step 1: Upgrade System Packages
Open your terminal (`Super + Return` or `kitty`) and run:

```bash
# 1. Update package database and upgrade all system packages
sudo pacman -Syu

# 2. Install cliphist for Spotlight's clipboard history daemon
sudo pacman -S --needed cliphist
```

Verify that you are running the updated desktop shell packages:
```bash
pacman -Q enerco-macshell enerco-desktop-config
```
Expected versions:
- `enerco-macshell >= 1.0.0-6`
- `enerco-desktop-config >= 1.0.0-24`

---

## Step 2: Switch to Native MacShell Spotlight
In older profiles, `~/.config/macbar/settings.json` routed search to `rofi -show drun`. Change `"launcher"` to an empty string to activate the native QML Spotlight:

```bash
# Set launcher to empty string
sed -i 's/"launcher": "rofi -show drun"/"launcher": ""/' ~/.config/macbar/settings.json

# If launcher key is missing, add it:
python3 -c "
import json, os
p = os.path.expanduser('~/.config/macbar/settings.json')
if os.path.exists(p):
    with open(p) as f: d = json.load(f)
    d['launcher'] = ''
    with open(p, 'w') as f: json.dump(d, f, indent=2)
"
```

Update your Dock pinned apps in `~/.config/macdock/pinned.json` to replace `"rofi"` with `"chromium"`:

```bash
sed -i 's/"rofi"/"chromium"/' ~/.config/macdock/pinned.json
```

---

## Step 3: Enable macOS Traffic Lights & Window Decorations
Create `~/.config/macbar/windecor.json` to enable window chrome across all applications:

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

Configure **Kitty Terminal** to eliminate duplicate Wayland CSD:

```bash
mkdir -p ~/.config/kitty
grep -q "hide_window_decorations" ~/.config/kitty/kitty.conf 2>/dev/null || \
  echo "hide_window_decorations yes" >> ~/.config/kitty/kitty.conf
```

---

## Step 4: Update Hyprland Keybindings & Layer Rules
Edit `~/.config/hypr/hyprland.lua` (or `~/.config/hypr/hyprland.conf`) to ensure the updated bindings are active:

```lua
-- Application Launchers
local menu = "qs -c MacShell ipc call spotlight toggle"
hl.bind(mainMod .. " + space",      hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + V",          hl.dsp.exec_cmd("qs -c MacShell ipc call spotlight clipboard"))
hl.bind(mainMod .. " + PERIOD",     hl.dsp.exec_cmd("qs -c MacShell ipc call spotlight emoji"))
hl.bind(mainMod .. " + SHIFT + V",  hl.dsp.window.float({ action = "toggle" }))
hl.bind("ALT + Tab",                hl.dsp.exec_cmd("qs -c MacShell ipc call switcher next"))
hl.bind(mainMod .. " + Tab",        hl.dsp.exec_cmd("qs -c MacShell ipc call switcher next"))

-- Layer Rules for MacShell
hl.layer_rule({ name = "blur-macspot", match = { namespace = "macspot" }, blur = true, ignore_alpha = 0.05 })
hl.layer_rule({ name = "macwindecor",  match = { namespace = "macwindecor" }, no_anim = true })
```

---

## Step 5: Reload Desktop Services Live
Apply all configuration changes immediately without rebooting:

```bash
# 1. Reload Hyprland compositor bindings and layer rules
hyprctl reload

# 2. Restart Quickshell / MacShell supervisor
pkill -f quickshell || true
setsid /usr/local/bin/macshell-start >/dev/null 2>&1 &
```

---

## Verification
- Press `Super + Space`: Native Liquid Glass **Enerco Search** modal opens.
- Press `Super + V`: Native **Clipboard History** opens with image thumbnail previews.
- Press `Super + .`: Native **Emoji Picker** opens.
- Open **Kitty Terminal** (`Super + Return`): Notice the macOS titlebar with red, amber, and green traffic lights at the top.
- Click the red light to close, amber to minimize, green to maximize/fullscreen.
- Drag the titlebar to move the window; double-click the titlebar to maximize or restore.
