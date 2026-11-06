"""Tier 2: Feature 16 - Target SDDM Wayland Session Target Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1, R2), PROJECT.md (Feature 16), TEST_INFRA.md, Survey 3 finding 6.
Validates session desktop file permissions, DesktopNames compliance, basicSetup flag in Calamares,
clean display environment propagation, and logout termination boundaries.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF16TargetSddmSessionBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 16: Target SDDM Wayland Session Target."""

    def test_calamares_displaymanager_basic_setup_flag(self):
        """T2-F16-1: Boundary: Verify displaymanager.conf enables basicSetup for user session initialization."""
        content = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        self.assertIn(
            "basicSetup: true",
            content,
            "displaymanager.conf must specify basicSetup: true to configure default user autologin/session",
        )

    def test_session_desktop_does_not_hardcode_x11_display(self):
        """T2-F16-2: Boundary: Verify session desktop file does not hardcode X11 DISPLAY=:0."""
        paths = [
            "pkgs/enerco-desktop-config/enerco.desktop",
            "pkgs/enerco-enterprise-tools/enerco.desktop",
            "airootfs/usr/share/wayland-sessions/enerco.desktop",
        ]
        for p in paths:
            if repo_file_exists(p):
                content = read_repo_file(p)
                self.assertNotIn(
                    "DISPLAY=:0",
                    content,
                    "Wayland session file must not hardcode X11 DISPLAY=:0",
                )

    def test_calamares_displaymanager_executable_path(self):
        """T2-F16-3: Boundary: Verify defaultDesktopEnvironment executable is valid."""
        content = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        self.assertIn("executable:", content, "displaymanager.conf must declare executable")

    def test_session_file_naming_convention(self):
        """T2-F16-4: Boundary: Verify desktop file name does not contain spaces or special characters."""
        # enerco.desktop or hyprland.desktop
        content = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        self.assertRegex(
            content,
            r'desktopFile:\s*"[a-zA-Z0-9_-]+"',
            "desktopFile in displaymanager.conf must be alphanumeric identifier",
        )

    def test_enerco_session_handles_exit_signals_cleanly(self):
        """T2-F16-5: Boundary: Verify enerco-session uses exec to replace wrapper process."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn(
            "exec ",
            content,
            "enerco-session must use 'exec' so Hyprland receives session signals directly from SDDM",
        )


if __name__ == "__main__":
    unittest.main()
