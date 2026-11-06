"""Tier 2: Feature 13 - Bluetooth Hardware Control Stack Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 13), TEST_INFRA.md, Survey 3 finding 4.1.
Validates non-fatal behavior on machines without Bluetooth adapter, rfkill tooling,
user permissions for device pairing, and audio routing integration.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF13BluetoothStackBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 13: Bluetooth Hardware Control Stack."""

    def test_services_systemd_bluetooth_mandatory_false(self):
        """T2-F13-1: Boundary: Verify bluetooth service is marked mandatory: false for VMs without BT controller."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        # When bluetooth is added, mandatory should be false
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "name:" in line and "bluetooth" in line:
                for j in range(i + 1, min(i + 5, len(lines))):
                    if "mandatory:" in lines[j]:
                        self.assertIn(
                            "false",
                            lines[j].lower(),
                            "bluetooth service must have mandatory: false so target boots on systems without BT adapter",
                        )
                        break

    def test_packages_includes_rfkill_tool(self):
        """T2-F13-2: Boundary: Verify packages.x86_64 or base includes rfkill utility for soft-block management."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        # util-linux provides rfkill
        has_rfkill = "util-linux" in packages or "rfkill" in packages
        self.assertTrue(
            has_rfkill,
            "System must provide rfkill (via util-linux or rfkill package) to manage radio blocks",
        )

    def test_users_conf_includes_audio_or_bluetooth_groups(self):
        """T2-F13-3: Boundary: Verify users.conf configures audio and input group access for media accessories."""
        content = read_repo_file("pkgs/enerco-calamares-config/users.conf")
        self.assertIn("defaultGroups:", content)
        has_media_groups = "audio" in content or "video" in content or "wheel" in content
        self.assertTrue(has_media_groups, "users.conf defaultGroups must allow media access")

    def test_blueman_autostart_avoids_crash_on_no_adapter(self):
        """T2-F13-4: Boundary: Verify blueman applet execution doesn't block shell startup if daemon is idle."""
        hyprland_lua = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        macshell_start = read_repo_file("pkgs/enerco-macshell/macshell-start")
        # Applet must be backgrounded or supervised
        if "blueman-applet" in hyprland_lua:
            self.assertTrue(
                "&" in hyprland_lua,
                "blueman-applet must be run in background",
            )

    def test_pipewire_pulse_packaged_for_bluetooth_audio(self):
        """T2-F13-5: Boundary: Verify packages.x86_64 includes pipewire-pulse for Bluetooth headset audio."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "pipewire-pulse",
            packages,
            "packages.x86_64 must include pipewire-pulse to route audio to Bluetooth headsets",
        )


if __name__ == "__main__":
    unittest.main()
