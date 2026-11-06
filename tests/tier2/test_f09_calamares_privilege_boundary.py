"""Tier 2: Feature 9 - Calamares Launcher Privilege & Desktop Cleanup Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 9), TEST_INFRA.md, Survey 2 finding 3.3/3.4.
Validates multi-socket Wayland display resolution, xhost root authorization,
target skel cleanliness, and non-interactive privilege bounds.
"""

import unittest
from tests.config import (
    get_repo_path,
    read_repo_file,
    repo_file_exists,
)


class TestF09CalamaresPrivilegeBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 9: Calamares Launcher Privilege & Desktop Cleanup."""

    def test_installer_resolves_wayland_0_and_wayland_1_sockets(self):
        """T2-F09-1: Boundary: Verify enerco-installer handles both wayland-0 and wayland-1 socket names."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-installer")
        self.assertIn("wayland-0", content, "enerco-installer must handle wayland-0 socket")
        self.assertIn("wayland-1", content, "enerco-installer must handle wayland-1 socket")

    def test_installer_authorizes_root_via_xhost_safely(self):
        """T2-F09-2: Boundary: Verify enerco-installer uses xhost +si:localuser:root with error suppression."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-installer")
        self.assertIn("xhost +si:localuser:root", content, "enerco-installer must authorize local root display access")
        self.assertIn("2>/dev/null", content, "xhost authorization must not fail script if Xwayland is not active")

    def test_target_skel_desktop_directory_cleanliness(self):
        """T2-F09-3: Boundary: Verify airootfs/etc/skel/Desktop does not contain an installer shortcut."""
        skel_desktop = get_repo_path("airootfs/etc/skel/Desktop/calamares.desktop")
        self.assertFalse(
            skel_desktop.exists(),
            "airootfs/etc/skel/Desktop/calamares.desktop must NOT exist (only liveuser should have desktop installer)",
        )

    def test_calamares_desktop_has_valid_categories(self):
        """T2-F09-4: Boundary: Verify calamares.desktop specifies valid Freedesktop Categories (System;)."""
        content = read_repo_file("pkgs/enerco-calamares-config/calamares.desktop")
        self.assertIn("Categories=System;", content, "calamares.desktop must have Categories=System;")
        self.assertIn("Terminal=false", content, "calamares.desktop must set Terminal=false")

    def test_liveuser_sudoers_file_permission_boundary(self):
        """T2-F09-5: Boundary: Verify sudoers configuration files use strict security format."""
        content = read_repo_file("airootfs/etc/sudoers.d/00-liveuser")
        self.assertTrue(
            "NOPASSWD:" in content,
            "00-liveuser must explicitly specify NOPASSWD for automated live installer execution",
        )


if __name__ == "__main__":
    unittest.main()
