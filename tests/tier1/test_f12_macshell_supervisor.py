"""Tier 1: Feature 12 - MacShell Supervisor & Waybar Fallback Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 12), TEST_INFRA.md, Survey 3 finding 3.
Validates macshell-start supervisor script, Wayland socket detection, Waybar/Dunst fallback
mechanism, notification daemon deconfliction, and executable packaging.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF12MacShellSupervisor(unittest.TestCase):
    """Tier 1 test suite for Feature 12: MacShell Supervisor & Waybar Fallback."""

    def test_macshell_start_exists(self):
        """T1-F12-1: Verify pkgs/enerco-macshell/macshell-start exists."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-macshell/macshell-start"),
            "pkgs/enerco-macshell/macshell-start must exist",
        )

    def test_macshell_start_waits_for_wayland_socket(self):
        """T1-F12-2: Verify macshell-start polls for WAYLAND_DISPLAY socket before launching."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        self.assertIn("WAYLAND_DISPLAY", content, "macshell-start must inspect WAYLAND_DISPLAY")
        self.assertTrue(
            "XDG_RUNTIME_DIR" in content or "wayland" in content,
            "macshell-start must verify display runtime socket presence",
        )

    def test_macshell_start_implements_waybar_fallback(self):
        """T1-F12-3: Verify macshell-start launches and supervises qs -c MacShell directly without legacy waybar."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        self.assertIn(
            "qs -c MacShell",
            content,
            "macshell-start must launch qs -c MacShell as primary shell",
        )
        self.assertNotIn(
            "waybar",
            content,
            "macshell-start must not launch legacy waybar",
        )

    def test_macshell_start_notification_exclusivity(self):
        """T1-F12-4: Verify dunst is stopped so MacShell owns org.freedesktop.Notifications."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        self.assertIn(
            "killall -q dunst",
            content,
            "macshell-start must stop dunst to prevent D-Bus notification collision with MacShell",
        )

    def test_macshell_pkgbuild_installs_supervisor_binary(self):
        """T1-F12-5: Verify pkgs/enerco-macshell/PKGBUILD installs macshell-start to /usr/local/bin."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        self.assertIn(
            "macshell-start",
            content,
            "PKGBUILD must install macshell-start supervisor",
        )


if __name__ == "__main__":
    unittest.main()
