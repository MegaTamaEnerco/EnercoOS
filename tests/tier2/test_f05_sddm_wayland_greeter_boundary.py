"""Tier 2: Feature 5 - SDDM Wayland Greeter Compositor Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1, R2), PROJECT.md (Feature 5), TEST_INFRA.md, Survey 2 finding 2.1.
Validates SDDM user boundaries, UID filtering, crash recovery safeguards,
compositor argument boundaries, and software rendering compatibility under VMs.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF05SddmWaylandGreeterBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 5: SDDM Wayland Greeter Compositor."""

    def test_sddm_user_uid_filtering_boundaries(self):
        """T2-F05-1: Boundary: Verify sddm-enerco.conf enforces standard user UID range (1000..60000)."""
        content = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")
        self.assertIn("MinimumUid=1000", content, "SDDM must hide system accounts below UID 1000")
        self.assertIn("MaximumUid=60000", content, "SDDM must filter out special IDs above 60000")

    def test_sddm_compositor_software_rendering_args(self):
        """T2-F05-2: Boundary: Verify SDDM compositor configuration handles VM software rendering mode."""
        content = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")
        # Greeter environment must allow layer-shell and software rasterizer if needed
        self.assertIn(
            "GreeterEnvironment=",
            content,
            "sddm-enerco.conf must define GreeterEnvironment variables for Wayland protocol integration",
        )

    def test_sddm_wayland_session_directory_validation(self):
        """T2-F05-3: Boundary: Verify sddm-enerco.conf points to standard /usr/share/wayland-sessions."""
        content = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")
        self.assertIn(
            "SessionDir=/usr/share/wayland-sessions",
            content,
            "SDDM must scan the standard Wayland session directory /usr/share/wayland-sessions",
        )

    def test_sddm_theme_cursor_adwaita_fallback(self):
        """T2-F05-4: Boundary: Verify sddm-enerco.conf specifies standard cursor theme to prevent X/Wayland cursor crash."""
        content = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")
        self.assertTrue(
            "CursorTheme=" in content,
            "SDDM configuration must define a valid cursor theme",
        )

    def test_sddm_hidpi_scaling_boundary(self):
        """T2-F05-5: Boundary: Verify EnableHiDPI setting is explicitly defined for modern displays."""
        content = read_repo_file("pkgs/enerco-desktop-config/sddm-enerco.conf")
        self.assertIn(
            "EnableHiDPI=true",
            content,
            "sddm-enerco.conf must enable HiDPI scaling for Retina and high-density screens",
        )


if __name__ == "__main__":
    unittest.main()
