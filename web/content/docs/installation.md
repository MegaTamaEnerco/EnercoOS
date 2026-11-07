---
title: "Calamares Installation Guide"
description: "Step-by-step instructions for flashing the EnercoOS ISO, booting in UEFI or BIOS mode, partitioning disks, and completing Calamares installation."
category: "Fundamentals"
order: 2
updatedAt: "2026-11-07"
---

## 1. Verify & Flash the Installation Media

After downloading the latest ISO from the [Releases](/releases) page (`enercoos-2026.11.07-x86_64.iso`), verify its integrity before flashing to a USB drive:

```bash
# Linux
sha256sum enercoos-2026.11.07-x86_64.iso

# Windows PowerShell
Get-FileHash .\enercoos-2026.11.07-x86_64.iso -Algorithm SHA256
```

### Flashing to a USB Drive (Bare Metal)

- **Linux (`dd`):**
  ```bash
  sudo dd bs=4M if=enercoos-2026.11.07-x86_64.iso of=/dev/sdX status=progress oflag=sync
  ```
- **Windows / Cross-Platform:**
  - Use **Rufus** (select **DD Image mode** when prompted) or **Ventoy** / **BalenaEtcher**.

---

## 2. Booting into the EnercoOS Live Environment

Insert the bootable USB (or attach the `.iso` to your VirtualBox / QEMU optical drive) and boot the machine:

1. Select **EnercoOS Enterprise Workstation (x86_64, Linux Zen)** (default) or **Standard Linux Kernel** from the `systemd-boot` (UEFI) or `Syslinux` (BIOS) menu.
2. The system will automatically start `NetworkManager`, `VBoxService` (if inside VirtualBox), and launch the **Enerco Liquid Glass** desktop session.
3. Click **Install EnercoOS** in the **EnercoOS Welcome** dialog, on the Desktop/Dock, or press `Super + I` to launch **Calamares**.

---

## 3. Completing the Calamares Installer

Calamares (`3.3.11`) guides you through six streamlined steps:

1. **Welcome:** Confirms system language and checks minimum disk capacity, power status, and architecture.
2. **Location & Timezone:** Select your region and timezone (e.g., `Asia/Jakarta` for WIB).
3. **Keyboard Layout:** Choose your physical keyboard layout (default `English (US)`).
4. **Partitions:**
   - **Erase Disk (Recommended for clean workstations):** Automatically creates a `512 MiB` `FAT32` EFI System Partition (`/boot/efi`), an `ext4` root filesystem (`/`), and swap space.
   - **Manual Partitioning:** Ensure `/boot/efi` is mounted as `fat32` with the `boot` / `esp` flag on UEFI systems.
5. **Users:**
   - Enter your full name, username (e.g., `admin`), workstation hostname (e.g., `mte-workstation-01`), and password.
   - Your user is automatically added to `wheel`, `video`, `audio`, `input`, `network`, `storage`, `users`, and `vboxsf`.
6. **Summary & Install:**
   - Click **Install Now**. Calamares unpacks `airootfs.sfs`, configures `fstab`, copies both `vmlinuz-linux` and `vmlinuz-linux-zen` kernels into `/boot`, runs `mkinitcpio -P`, configures `SDDM` (`enerco.desktop`), enables `NetworkManager`, `vboxservice`, `irqbalance`, and `systemd-zram-setup@zram0`, and installs the `GRUB` bootloader.

---

## 4. First Boot After Installation

1. When Calamares reaches **All done**, check **Restart now** (and remove the installation ISO/USB if needed).
2. The workstation boots into **GRUB** (`EnercoOS Enterprise Workstation`) and starts the **SDDM Wayland Greeter**.
3. Enter your password and press `Enter` to launch your persistent **Enerco Liquid Glass** session (`enerco-session` -> `Hyprland` + `MacShell`).
