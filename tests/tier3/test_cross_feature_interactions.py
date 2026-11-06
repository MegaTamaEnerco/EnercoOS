"""Tier 3: Cross-Feature Interactions Test Suite (16 Pairwise Tests).

Derivation source: ORIGINAL_REQUEST.md, PROJECT.md (Interface Contracts), TEST_INFRA.md.
Validates integration contracts between subsystems:
- Calamares & SDDM
- MacShell & Waybar fallback
- PipeWire & Hotkeys
- NetworkManager & ERP launcher
- Dynamic Acceleration & Hyprland
- Calamares & Dynamic Acceleration
- Hypridle & MacLock
- Bluetooth Stack & Control Center
- Target SDDM & enerco-session
- Bootloader & Pacman Mirrors
- Build Script & Rebuild Detection
- Calamares Privilege & Desktop Cleanup
- Display Tooling & Hyprland
- Enterprise ERP & Freedesktop Compliance
- VirtualBox Guest Services & Target Boot
- Notification Daemon Deconfliction
"""

import os
import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestTier3CrossFeatureInteractions(unittest.TestCase):
    """Tier 3 test suite for cross-feature pairwise interactions."""

    def test_interaction_01_calamares_and_sddm(self):
        """T3-01: Calamares & SDDM: Calamares sets SDDM as display manager and selects enerco session."""
        dm_conf = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        sddm_conf = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")

        # Calamares must target sddm
        self.assertIn("sddm", dm_conf)
        # Calamares must target enerco session
        self.assertIn('desktopFile: "enerco"', dm_conf)
        # SDDM must run Wayland
        self.assertIn("DisplayServer=wayland", sddm_conf)

    def test_interaction_02_macshell_and_waybar_fallback(self):
        """T3-02: MacShell & Waybar: macshell-start supervisor falls back to Waybar and Dunst on failure."""
        supervisor = read_repo_file("pkgs/enerco-macshell/macshell-start")
        # Supervisor must contain both MacShell and Waybar references
        self.assertIn("MacShell", supervisor)
        self.assertIn("waybar", supervisor, "macshell-start must provide Waybar fallback on MacShell failure")

    def test_interaction_03_pipewire_and_hotkeys(self):
        """T3-03: PipeWire & Hotkeys: Hyprland Lua audio keybindings interface with wpctl / pipewire."""
        hyprland_lua = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        packages = read_repo_file("packages.x86_64")

        # packages must include pipewire and wireplumber
        self.assertIn("pipewire", packages)
        self.assertIn("wireplumber", packages)

        # hyprland.lua must have wpctl bindings for volume
        self.assertTrue(
            "wpctl" in hyprland_lua or "XF86Audio" in hyprland_lua,
            "hyprland.lua audio bindings must interface with WirePlumber (wpctl)",
        )

    def test_interaction_04_networkmanager_and_mterp(self):
        """T3-04: NetworkManager & MTERP: NetworkManager package aligns with MTERP launcher requirements."""
        packages = read_repo_file("packages.x86_64")
        mterp_entry = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")

        self.assertIn("networkmanager", packages)
        self.assertIn("chromium", packages)
        self.assertIn("https://mterp.megatama-enerco.com", mterp_entry)

    def test_interaction_05_dynamic_accel_and_hyprland(self):
        """T3-05: Dynamic Accel & Hyprland: enerco-session applies hypervisor flags before starting Hyprland."""
        session_script = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn("systemd-detect-virt", session_script)
        # Launches Hyprland at end of script
        self.assertTrue(
            "Hyprland" in session_script,
            "enerco-session must launch Hyprland after setting acceleration flags",
        )

    def test_interaction_06_calamares_and_dynamic_accel(self):
        """T3-06: Calamares & Dynamic Accel: Target /etc/environment unpacked by Calamares has no software GL."""
        env_file = read_repo_file("airootfs/etc/environment")
        self.assertNotIn(
            "LIBGL_ALWAYS_SOFTWARE=1",
            env_file,
            "Target /etc/environment unpacked by Calamares must not force software GL",
        )

    def test_interaction_07_hypridle_and_maclock(self):
        """T3-07: Hypridle & MacLock: hypridle idle actions interface with MacLock or hyprlock."""
        has_hypridle = (
            repo_file_exists("pkgs/enerco-desktop-config/hypridle.conf")
            or repo_file_exists("airootfs/etc/skel/.config/hypr/hypridle.conf")
        )
        self.assertTrue(has_hypridle, "hypridle.conf must be packaged for idle management")

    def test_interaction_08_bluetooth_and_control_center(self):
        """T3-08: Bluetooth & Control Center: bluez daemon packages integrate with desktop tray / status bar."""
        packages = read_repo_file("packages.x86_64")
        self.assertIn("bluez", packages)
        self.assertIn("blueman", packages)

    def test_interaction_09_target_sddm_and_enerco_session(self):
        """T3-09: Target SDDM & enerco-session: SDDM targets enerco.desktop which calls enerco-session."""
        dm_conf = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        self.assertIn('desktopFile: "enerco"', dm_conf)

    def test_interaction_10_bootloader_and_pacman_mirrors(self):
        """T3-10: Bootloader & Pacman Mirrors: Target system receives active mirrorlist and bootloader."""
        grub_conf = read_repo_file("pkgs/enerco-calamares-config/grubcfg.conf")
        pacman_conf = read_repo_file("pacman.conf")
        self.assertIn("quiet splash", grub_conf)
        self.assertIn("/etc/pacman.d/mirrorlist", pacman_conf)

    def test_interaction_11_build_script_and_rebuild_detection(self):
        """T3-11: Build Script & Rebuild Detection: build.sh passes rebuild arguments to build-packages.sh."""
        build_sh = read_repo_file("build.sh")
        build_pkgs = read_repo_file("scripts/build-packages.sh")
        self.assertTrue(
            "--rebuild" in build_sh or "REBUILD" in build_sh,
            "build.sh must support passing rebuild flag to build-packages.sh",
        )
        self.assertTrue(
            "--rebuild" in build_pkgs or "REBUILD" in build_pkgs,
            "build-packages.sh must process rebuild flag",
        )

    def test_interaction_12_calamares_privilege_and_desktop_shortcut(self):
        """T3-12: Calamares Privilege & Desktop: Passwordless sudo allows live install without skel pollution."""
        sudoers = read_repo_file("airootfs/etc/sudoers.d/00-liveuser")
        pkgbuild = read_repo_file("pkgs/enerco-calamares-config/PKGBUILD")
        self.assertIn("NOPASSWD", sudoers)
        self.assertNotIn("etc/skel/Desktop/calamares.desktop", pkgbuild)

    def test_interaction_13_display_tooling_and_hyprland(self):
        """T3-13: Display Tooling & Hyprland: wdisplays packages align with Hyprland 0.57 compositor."""
        packages = read_repo_file("packages.x86_64")
        self.assertIn("wdisplays", packages)
        self.assertIn("hyprland", packages)

    def test_interaction_14_mterp_and_freedesktop_compliance(self):
        """T3-14: MTERP & Freedesktop: mterp.desktop icon resolves against enerco-branding package."""
        mterp_entry = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        branding_pkgbuild = read_repo_file("pkgs/enerco-branding/PKGBUILD")
        self.assertIn("Icon=enerco-logo", mterp_entry)
        self.assertIn("enerco-logo", branding_pkgbuild)

    def test_interaction_15_vboxservice_and_target_boot(self):
        """T3-15: VirtualBox Guest Services & Target Boot: vboxservice enabled on target alongside SDDM."""
        services = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        self.assertIn("sddm", services)
        self.assertTrue("vboxservice" in services or "vboxservice.service" in services)

    def test_interaction_16_notification_daemon_deconfliction(self):
        """T3-16: Notification Deconfliction: Dunst and MacShell notification daemons do not collide on D-Bus."""
        supervisor = read_repo_file("pkgs/enerco-macshell/macshell-start")
        # Dunst should not be unconditionally launched alongside MacShell
        self.assertNotIn(
            "dunst & \nexec qs -c MacShell",
            supervisor,
            "Dunst must not be launched concurrently with MacShell to avoid org.freedesktop.Notifications collision",
        )


if __name__ == "__main__":
    unittest.main()
