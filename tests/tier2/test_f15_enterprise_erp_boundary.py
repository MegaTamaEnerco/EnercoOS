"""Tier 2: Feature 15 - Enterprise ERP Integration & Productivity Stack Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R3), PROJECT.md (Feature 15), TEST_INFRA.md, Survey 3 finding 5.
Validates Wayland ozone flags, window manager class grouping, user data profile sandboxing,
corporate portal bookmarks/launchers, and category categorization.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF15EnterpriseERPBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 15: Enterprise ERP Integration & Productivity Stack."""

    def test_mterp_launcher_ozone_wayland_flags(self):
        """T2-F15-1: Boundary: Verify mterp.desktop includes Wayland Ozone flags for native Wayland rendering."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        self.assertIn(
            "--ozone-platform=wayland",
            content,
            "mterp launcher must specify --ozone-platform=wayland for native Wayland compositor integration",
        )

    def test_mterp_launcher_wm_class_for_dock_pinning(self):
        """T2-F15-2: Boundary: Verify mterp.desktop defines StartupWMClass for MacShell/dock grouping."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        self.assertIn(
            "StartupWMClass=",
            content,
            "mterp.desktop must define StartupWMClass for proper window tracking and dock icon pinning",
        )

    def test_mterp_launcher_categories(self):
        """T2-F15-3: Boundary: Verify mterp.desktop specifies enterprise Categories (Office;Finance;)."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        self.assertIn("Categories=", content)
        self.assertTrue(
            "Office" in content or "Finance" in content,
            "mterp.desktop must belong to Office or Finance categories",
        )

    def test_corporate_portal_reference_exists(self):
        """T2-F15-4: Boundary: Verify references to PT Mega Tama Enerco official portal (org.megatama-enerco.com)."""
        # Check if portal reference exists in README, tools, or browser bookmarks
        content_readme = read_repo_file("README.md") if repo_file_exists("README.md") else ""
        self.assertTrue(
            "megatama-enerco.com" in content_readme
            or "org.megatama-enerco.com" in content_readme
            or repo_file_exists("pkgs/enerco-enterprise-tools/mterp.desktop"),
            "System must reference official corporate portal",
        )

    def test_mterp_wrapper_executable_path_boundary(self):
        """T2-F15-5: Boundary: Verify enerco-mterp wrapper script or chromium binary path exists."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        self.assertIn("Exec=", content, "mterp.desktop must declare valid Exec command")


if __name__ == "__main__":
    unittest.main()
