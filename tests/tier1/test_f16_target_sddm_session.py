"""Tier 1: Feature 16 - Target SDDM Wayland Session Target Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1, R2), PROJECT.md (Feature 16), TEST_INFRA.md, Survey 3 finding 6.
Validates packaging of /usr/share/wayland-sessions/enerco.desktop, Exec invocation of enerco-session,
Calamares default desktop environment selection, and Freedesktop session compliance.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF16TargetSddmSession(unittest.TestCase):
    """Tier 1 test suite for Feature 16: Target SDDM Wayland Session Target."""

    def test_calamares_displaymanager_targets_enerco_session(self):
        """T1-F16-1: Verify displaymanager.conf selects enerco desktop session rather than generic hyprland."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/displaymanager.conf"),
            "pkgs/enerco-calamares-config/displaymanager.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        # Bug: desktopFile: "hyprland" launches raw hyprland bypassing enerco-session
        self.assertIn(
            'desktopFile: "enerco"',
            content,
            "displaymanager.conf must configure desktopFile: 'enerco' so SDDM executes enerco-session",
        )

    def test_enerco_wayland_session_desktop_exists(self):
        """T1-F16-2: Verify enerco.desktop session file exists in desktop config or enterprise tools."""
        has_session_file = (
            repo_file_exists("pkgs/enerco-desktop-config/enerco.desktop")
            or repo_file_exists("pkgs/enerco-enterprise-tools/enerco.desktop")
            or repo_file_exists("airootfs/usr/share/wayland-sessions/enerco.desktop")
        )
        self.assertTrue(
            has_session_file,
            "enerco.desktop must exist in pkgs/enerco-desktop-config, pkgs/enerco-enterprise-tools, or airootfs",
        )

    def test_enerco_session_desktop_executes_enerco_session(self):
        """T1-F16-3: Verify enerco.desktop invokes /usr/local/bin/enerco-session."""
        # Check wherever the file exists
        paths = [
            "pkgs/enerco-desktop-config/enerco.desktop",
            "pkgs/enerco-enterprise-tools/enerco.desktop",
            "airootfs/usr/share/wayland-sessions/enerco.desktop",
        ]
        content = None
        for p in paths:
            if repo_file_exists(p):
                content = read_repo_file(p)
                break
        self.assertIsNotNone(content, "enerco.desktop session definition must be available")
        self.assertTrue(
            "Exec=/usr/local/bin/enerco-session" in content or "Exec=enerco-session" in content,
            "enerco.desktop must execute enerco-session wrapper",
        )

    def test_enerco_session_desktop_metadata(self):
        """T1-F16-4: Verify enerco.desktop has valid Freedesktop Type and Name."""
        paths = [
            "pkgs/enerco-desktop-config/enerco.desktop",
            "pkgs/enerco-enterprise-tools/enerco.desktop",
            "airootfs/usr/share/wayland-sessions/enerco.desktop",
        ]
        content = None
        for p in paths:
            if repo_file_exists(p):
                content = read_repo_file(p)
                break
        self.assertIsNotNone(content, "enerco.desktop session definition must be available")
        self.assertIn("Type=Application", content, "Session entry must be Type=Application")
        self.assertIn("Name=", content, "Session entry must have Name property")

    def test_pkgbuild_installs_wayland_session(self):
        """T1-F16-5: Verify PKGBUILD installs enerco.desktop into /usr/share/wayland-sessions/."""
        desktop_pkgbuild = read_repo_file("pkgs/enerco-desktop-config/PKGBUILD")
        tools_pkgbuild = read_repo_file("pkgs/enerco-enterprise-tools/PKGBUILD")
        has_install = (
            "wayland-sessions" in desktop_pkgbuild
            or "wayland-sessions" in tools_pkgbuild
            or "enerco.desktop" in desktop_pkgbuild
            or "enerco.desktop" in tools_pkgbuild
        )
        self.assertTrue(
            has_install,
            "Package build recipe must install enerco.desktop to /usr/share/wayland-sessions/",
        )


if __name__ == "__main__":
    unittest.main()
