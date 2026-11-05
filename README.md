# EnercoOS: Arch-Based Enterprise Distribution

EnercoOS is a custom, production-grade Arch Linux distribution engineered for **PT Mega Tama Enerco**. It merges the elegance and productivity of a macOS-style Wayland interface (**Hyprland + Waybar + Rofi + SDDM**) with enterprise manageability, the **Calamares** graphical system installer, and native execution of the **MTERP** enterprise management console.

---

## 1. System Architecture

```
┌────────────────────────────────────────────────────────┐
│ WINDOWS 11 HOST (VS Code / Git Repo Authoring)          │
│  ├── Workspace: C:\Users\...\EnercoOS                  │
│  │     │                                               │
│  │     ▼ (fast editing & file sync)                    │
│  ├── WSL 2 (Arch or Ubuntu)                            │
│  │     └── Repository sync, linting, packaging assets  │
│  │                                                     │
│  └── VM Hypervisor (Hyper-V / VirtualBox / VMware)     │
│        ├── Build VM (Arch Linux, nested loop/kernel)   │
│        │     ├── Standard Packaging: makepkg & repo-add│
│        │     └── ISO Generation: mkarchiso             │
│        └── Test VM (UEFI x86_64)                       │
│              └── Boots: enercoos-x86_64.iso            │
└────────────────────────────────────────────────────────┘
```

> **Why the WSL + Native Arch VM Split?**  
> `mkarchiso` creates multiple nested loop devices (`/dev/loop*`), raw block mounts, and strict chroot OverlayFS layers that can trigger permission or driver stalls in WSL's virtualized microkernel. Compiling the final image inside a native Arch VM guarantees 100% upstream kernel parity.

---

## 2. Standard Arch Packaging Philosophy

Unlike naive ISOs that dump loose files directly into `airootfs`, EnercoOS strictly adheres to **standard Arch Linux packaging**:
- Custom assets, configurations, and tools are maintained as standard **`PKGBUILD`** recipes inside `pkgs/`.
- `scripts/build-packages.sh` builds these with `makepkg -sf` (or `extra-x86_64-build` in a clean chroot) and registers them with `repo-add` into `localrepo/enerco-local.db.tar.gz`.
- `mkarchiso` pulls them like any official package, and the installed target system can track, verify, and update them through `pacman`.

### In-Tree Packages

| Package | Role | Key Components |
| :--- | :--- | :--- |
| **`enerco-branding`** | OS Identity & Art | `/usr/lib/os-release`, `/etc/issue`, Sonoma/Sequoia wallpapers, enterprise SVG logos |
| **`enerco-desktop-config`** | Cupertino Wayland UI | Hyprland config (blur, rounded corners), Waybar menu bar, Rofi spotlight, Kitty terminal, SDDM theme |
| **`enerco-enterprise-tools`** | Endpoint Tools & ERP | `mterp.desktop` (Chromium PWA), `enerco-session` (smart GPU detector), `enerco-lockdown`, `enerco-welcome` |
| **`calamares`** | System Installer | Standard upstream Qt6 source compilation of Calamares 3.3.x |
| **`enerco-calamares-config`** | Installer Branding | Enterprise branding, automated partitioning, user provisioning, systemd services setup |

---

## 3. Directory Layout

```text
EnercoOS/
├── .gitignore
├── .wslconfig                             # Host WSL2 memory and CPU configuration
├── README.md                              # Complete documentation
├── build.sh                               # Unified root build entrypoint
├── profiledef.sh                          # Archiso profile definitions & file permissions
├── packages.x86_64                        # Upstream & local package manifests
├── pacman.conf                            # Pacman mirrors + localrepo entry
├── efiboot/                               # UEFI bootloader configurations
│   └── loader/
│       ├── loader.conf
│       └── entries/
│           ├── 01-enercoos-x86_64-linux.conf
│           └── 02-enercoos-x86_64-nomodeset.conf
├── syslinux/                              # BIOS fallback bootloader configuration
├── localrepo/                             # Local package repository populated by build-packages.sh
├── pkgs/                                  # Standard Arch PKGBUILD recipes
│   ├── calamares/
│   ├── enerco-branding/
│   ├── enerco-desktop-config/
│   ├── enerco-enterprise-tools/
│   └── enerco-calamares-config/
├── scripts/
│   ├── build-packages.sh                  # makepkg & repo-add package pipeline
│   ├── run-qemu.sh                        # Rapid QEMU UEFI test runner
│   └── sync-to-vm.sh                      # rsync helper to sync repository to Build VM
└── airootfs/                              # Minimal live-only system overlay
    ├── etc/
    │   ├── hostname, locale.conf, vconsole.conf
    │   ├── sudoers.d/00-liveuser
    │   └── systemd/system/enerco-live-setup.service
    └── usr/local/bin/enerco-live-init     # Live environment provisioning
```

---

## 4. Setup & Build Guide

### Step 1: Configure Windows 11 & WSL 2

1. Copy `.wslconfig` to your Windows user directory:
   ```powershell
   Copy-Item .wslconfig $env:USERPROFILE\.wslconfig
   wsl --shutdown
   ```
2. In WSL 2, clone or sync this repository into your native ext4 home directory:
   ```bash
   mkdir -p ~/enercoos-dev
   cp -r /mnt/c/Users/CorSec/Documents/personal/EnercoOS/* ~/enercoos-dev/
   ```

### Step 2: Configure the Dedicated Arch Build VM

Set up a standard Arch Linux Virtual Machine (Hyper-V, VirtualBox, or VMware):
- **RAM**: 6GB - 8GB
- **vCPUs**: 4 Cores
- **Disk**: 40GB+
- **Firmware**: UEFI

Install build dependencies inside the VM:
```bash
sudo pacman -Syu --noconfirm archiso base-devel git qemu-desktop edk2-ovmf squashfs-tools ninja cmake
```

### Step 3: Build Packages & Generate the ISO

1. Sync the project repository to your Build VM (or clone directly):
   ```bash
   ./scripts/sync-to-vm.sh archvm.local arch ~/EnercoOS
   ```
2. Log into the Arch VM and run the automated build script:
   ```bash
   cd ~/EnercoOS
   sudo ./build.sh
   ```

The script automatically:
1. Compiles and indexes all `pkgs/` into `localrepo/enerco-local.db.tar.gz`.
2. Generates the clean `pacman.conf` mapping.
3. Executes `mkarchiso` to build `dist/enercoos-YYYY.MM.DD-x86_64.iso`.

---

## 5. Verification & Testing

### Option A: Instant QEMU UEFI Emulation
Inside the Arch Build VM, launch the test runner:
```bash
./scripts/run-qemu.sh
```

### Option B: Bare-Metal or VirtualBox Client Testing
Copy the generated ISO to your Windows Downloads folder:
```bash
cp dist/enercoos-*.iso /mnt/c/Users/CorSec/Downloads/
```
Attach to a VirtualBox / Hyper-V machine with **UEFI enabled** and boot:
1. Verify auto-login into the `enerco` live session with Hyprland.
2. Confirm the **EnercoOS Welcome Dialog** appears.
3. Test **MTERP Console** launcher (`SUPER + E`).
4. Launch **Install EnercoOS** (`SUPER + I` or desktop icon) to test Calamares installation.

---

## 6. Desktop Shortcuts & Keybindings

| Keybinding | Action |
| :--- | :--- |
| `SUPER + SPACE` | **Spotlight Launcher** (Rofi application & command search) |
| `SUPER + RETURN` | **Terminal** (Kitty with Cascadia Code & Cupertino Dark) |
| `SUPER + E` | **MTERP Console** (Enterprise ERP in pure Wayland PWA mode) |
| `SUPER + I` | **Calamares Installer** (System installation wizard) |
| `SUPER + F` | **File Manager** (Thunar) |
| `SUPER + Q` | Close active window |
| `SUPER + M` | Exit Hyprland session |
| `SUPER + SHIFT + S` | Interactive screenshot to clipboard (`grim + slurp`) |
| `SUPER + 1..5` | Switch workspace |

