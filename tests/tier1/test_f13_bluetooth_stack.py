"""Tier 1: Feature 13 - Bluetooth Hardware Control Stack Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 13), TEST_INFRA.md, Survey 3 finding 4.1.
Validates packaging of BlueZ daemon, BlueZ utilities, Blueman GUI manager, and systemd service enablement.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF13BluetoothStack(unittest.TestCase):
    """Tier 1 test suite for Feature 13: Bluetooth Hardware Control Stack."""

    def test_packages_includes_bluez(self):
        """T1-F13-1: Verify packages.x86_64 includes bluez Bluetooth daemon."""
        self.assertTrue(repo_file_exists("packages.x86_64"), "packages.x86_64 must exist")
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "bluez",
            packages,
            "packages.x86_64 must include bluez daemon for enterprise Bluetooth peripheral support",
        )

    def test_packages_includes_bluez_utils(self):
        """T1-F13-2: Verify packages.x86_64 includes bluez-utils for CLI management."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "bluez-utils",
            packages,
            "packages.x86_64 must include bluez-utils (providing bluetoothctl)",
        )

    def test_packages_includes_blueman(self):
        """T1-F13-3: Verify packages.x86_64 includes blueman GTK GUI manager."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "blueman",
            packages,
            "packages.x86_64 must include blueman for graphical Bluetooth device pairing and management",
        )

    def test_target_systemd_enables_bluetooth_service(self):
        """T1-F13-4: Verify services-systemd.conf or systemd presets enable bluetooth service."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        has_bluetooth = "bluetooth" in content or "bluetooth.service" in content
        self.assertTrue(
            has_bluetooth,
            "services-systemd.conf must enable bluetooth service on target systems",
        )

    def test_desktop_environment_blueman_integration(self):
        """T1-F13-5: Verify blueman-applet or tray integration exists in desktop autostart."""
        # Check hyprland.lua, enerco-session, or macshell autostarts
        hyprland_lua = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        macshell_start = read_repo_file("pkgs/enerco-macshell/macshell-start")
        has_applet = "blueman" in hyprland_lua or "blueman" in macshell_start
        self.assertTrue(
            has_applet,
            "Desktop autostart must integrate blueman-applet into the system tray",
        )


if __name__ == "__main__":
    unittest.main()
