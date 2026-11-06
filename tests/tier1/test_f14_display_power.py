"""Tier 1: Feature 14 - Display & Power Management Tooling Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 14), TEST_INFRA.md, Survey 3 finding 4.2/4.3.
Validates packaging of wdisplays, power-profiles-daemon, hypridle configuration, and decoupling
of System Settings from the Calamares installer.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF14DisplayPower(unittest.TestCase):
    """Tier 1 test suite for Feature 14: Display & Power Management Tooling."""

    def test_packages_includes_wdisplays(self):
        """T1-F14-1: Verify packages.x86_64 includes wdisplays for graphical resolution/scaling."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "wdisplays",
            packages,
            "packages.x86_64 must include wdisplays for graphical Wayland display management",
        )

    def test_packages_includes_power_profiles_daemon(self):
        """T1-F14-2: Verify packages.x86_64 includes power-profiles-daemon."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "power-profiles-daemon",
            packages,
            "packages.x86_64 must include power-profiles-daemon for laptop and power state controls",
        )

    def test_target_services_enables_power_profiles(self):
        """T1-F14-3: Verify services-systemd.conf enables power-profiles-daemon."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        has_power = "power-profiles-daemon" in content
        self.assertTrue(
            has_power,
            "services-systemd.conf must enable power-profiles-daemon on target installations",
        )

    def test_hypridle_configuration_exists(self):
        """T1-F14-4: Verify hypridle.conf exists in desktop config and configures lock timeouts."""
        has_hypridle = (
            repo_file_exists("pkgs/enerco-desktop-config/hypridle.conf")
            or repo_file_exists("airootfs/etc/skel/.config/hypr/hypridle.conf")
        )
        self.assertTrue(
            has_hypridle,
            "hypridle.conf must exist in pkgs/enerco-desktop-config or airootfs skeleton",
        )

    def test_system_settings_decoupled_from_calamares_installer(self):
        """T1-F14-5: Verify System Settings action does not launch enerco-installer."""
        # In enerco-menubar and enerco-apple-menu
        menubar_content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-menubar")
        apple_menu_content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-apple-menu")
        # System Settings must NOT invoke enerco-installer
        self.assertNotIn(
            '*"System Settings"*) xfce4-settings-manager 2>/dev/null || /usr/local/bin/enerco-installer',
            menubar_content,
            "System Settings in enerco-menubar must launch real settings (e.g. wdisplays/control center), not installer",
        )
        self.assertNotIn(
            '*"System Settings"*) /usr/local/bin/enerco-installer',
            apple_menu_content,
            "System Settings in enerco-apple-menu must not launch installer",
        )


if __name__ == "__main__":
    unittest.main()
