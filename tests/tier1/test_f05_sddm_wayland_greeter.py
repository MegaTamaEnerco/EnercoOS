"""Tier 1: Feature 5 - SDDM Wayland Greeter Compositor Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1, R2), PROJECT.md (Feature 5), TEST_INFRA.md, Survey 2 finding 2.1.
Validates SDDM Wayland configuration, inclusion of greeter compositor (weston/cage/labwc) in packages,
desktop configuration packaging, and Calamares displaymanager setup.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF05SddmWaylandGreeter(unittest.TestCase):
    """Tier 1 test suite for Feature 5: SDDM Wayland Greeter Compositor."""

    def test_packages_list_includes_wayland_compositor(self):
        """T1-F05-1: Verify packages.x86_64 includes a Wayland greeter compositor (weston/cage/labwc)."""
        self.assertTrue(repo_file_exists("packages.x86_64"), "packages.x86_64 must exist")
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        # To avoid SDDM Wayland greeter crash loop, weston, cage, or labwc must be packaged
        has_compositor = any(p in packages for p in ["weston", "cage", "labwc"])
        self.assertTrue(
            has_compositor,
            "packages.x86_64 must include a Wayland compositor (e.g. 'weston') to prevent SDDM crash loop",
        )

    def test_sddm_config_specifies_wayland_display_server(self):
        """T1-F05-2: Verify sddm-enerco.conf sets DisplayServer=wayland."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-desktop-config/sddm-enerco.conf"),
            "pkgs/enerco-desktop-config/sddm-enerco.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")
        self.assertIn("DisplayServer=wayland", content, "SDDM must be configured with DisplayServer=wayland")

    def test_sddm_config_wayland_compositor_command(self):
        """T1-F05-3: Verify sddm-enerco.conf configures CompositorCommand or Wayland greeter environment."""
        content = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")
        self.assertIn("[Wayland]", content, "sddm-enerco.conf must contain [Wayland] section")
        # Must configure CompositorCommand or valid Wayland session directory
        has_cmd_or_dir = "CompositorCommand=" in content or "SessionDir=/usr/share/wayland-sessions" in content
        self.assertTrue(has_cmd_or_dir, "SDDM configuration must configure Wayland compositor or sessions")

    def test_desktop_config_pkgbuild_installs_sddm_dropin(self):
        """T1-F05-4: Verify pkgs/enerco-desktop-config/PKGBUILD installs SDDM configuration drop-in."""
        content = read_repo_file("pkgs/enerco-desktop-config/PKGBUILD")
        self.assertTrue(
            "sddm-enerco.conf" in content or "sddm.conf.d" in content,
            "PKGBUILD must install sddm configuration drop-in into /etc/sddm.conf.d/",
        )

    def test_calamares_displaymanager_enables_sddm(self):
        """T1-F05-5: Verify Calamares displaymanager.conf selects sddm as target display manager."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/displaymanager.conf"),
            "pkgs/enerco-calamares-config/displaymanager.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        self.assertIn("displaymanagers:", content, "displaymanager.conf must define displaymanagers list")
        self.assertIn("sddm", content, "displaymanager.conf must configure sddm as the primary display manager")


if __name__ == "__main__":
    unittest.main()
