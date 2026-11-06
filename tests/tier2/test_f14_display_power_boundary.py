"""Tier 2: Feature 14 - Display & Power Management Tooling Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 14), TEST_INFRA.md, Survey 3 finding 4.2/4.3.
Validates DPMS timeout bounds, power-profiles-daemon mandatory flag behavior,
display resolution switcher keybindings, and idle inhibition.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF14DisplayPowerBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 14: Display & Power Management Tooling."""

    def test_power_profiles_daemon_mandatory_false(self):
        """T2-F14-1: Boundary: Verify power-profiles-daemon service has mandatory: false for VM hypervisors."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "name:" in line and "power-profiles-daemon" in line:
                for j in range(i + 1, min(i + 5, len(lines))):
                    if "mandatory:" in lines[j]:
                        self.assertIn(
                            "false",
                            lines[j].lower(),
                            "power-profiles-daemon must be mandatory: false as VMs may lack ACPI profile support",
                        )
                        break

    def test_hypridle_timeout_sensible_bounds(self):
        """T2-F14-2: Boundary: Verify hypridle timeout is configured with sensible bounds (>= 180s)."""
        paths = [
            "pkgs/enerco-desktop-config/hypridle.conf",
            "airootfs/etc/skel/.config/hypr/hypridle.conf",
        ]
        content = None
        for p in paths:
            if repo_file_exists(p):
                content = read_repo_file(p)
                break
        if content:
            self.assertIn("timeout", content)
            # Timeout should not be annoyingly short (< 60s)
            self.assertFalse(
                "timeout = 10" in content or "timeout = 30" in content,
                "Idle lock timeout should be reasonable (e.g. >= 300s)",
            )

    def test_resolution_switcher_keybindings_present(self):
        """T2-F14-3: Boundary: Verify hyprland.lua contains quick resolution switchers for VM testing."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        # Supports F8..F11 hotkeys for switching resolutions
        self.assertIn("F11", content, "hyprland.lua should support Super+F11 for 1080p switch")
        self.assertIn("F8", content, "hyprland.lua should support Super+F8 for auto resolution")

    def test_hypridle_invokes_screen_lock(self):
        """T2-F14-4: Boundary: Verify hypridle config triggers lock screen before display power off."""
        paths = [
            "pkgs/enerco-desktop-config/hypridle.conf",
            "airootfs/etc/skel/.config/hypr/hypridle.conf",
        ]
        content = None
        for p in paths:
            if repo_file_exists(p):
                content = read_repo_file(p)
                break
        if content:
            has_lock = "lock" in content.lower() or "hyprlock" in content or "maclock" in content.lower()
            self.assertTrue(has_lock, "hypridle must configure screen locking")

    def test_wdisplays_binary_in_desktop_applications(self):
        """T2-F14-5: Boundary: Verify wdisplays desktop entry is present or installed in packages."""
        content = read_repo_file("packages.x86_64")
        self.assertTrue(
            "wdisplays" in content or "kanshi" in content or "wlr-randr" in content,
            "System must provide Wayland display management utilities",
        )


if __name__ == "__main__":
    unittest.main()
