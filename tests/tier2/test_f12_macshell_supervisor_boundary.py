"""Tier 2: Feature 12 - MacShell Supervisor & Waybar Fallback Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 12), TEST_INFRA.md, Survey 3 finding 3.
Validates single-instance guards, configuration seeding idempotence, symbolic link resilience,
timeout boundaries, and user state directory handling.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF12MacShellSupervisorBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 12: MacShell Supervisor & Waybar Fallback."""

    def test_single_instance_process_guard(self):
        """T2-F12-1: Boundary: Verify macshell-start detects already-running MacShell and exits cleanly."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        self.assertIn("pgrep", content, "macshell-start must use pgrep to check if already running")
        self.assertIn("exit 0", content, "macshell-start must exit 0 if another instance is active")

    def test_configuration_seeding_idempotence(self):
        """T2-F12-2: Boundary: Verify macshell-start seeds default configs without overwriting user changes (-n)."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        # cp -n or if [ ! -f ] prevents overwriting customized dock pinned.json
        self.assertTrue(
            "cp -n" in content or "if [ ! -f" in content,
            "macshell-start must preserve user customizations by not unconditionally overwriting config files",
        )

    def test_symlink_creation_force_atomic(self):
        """T2-F12-3: Boundary: Verify symlink creation uses -sfn to handle broken existing symlinks."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        self.assertIn(
            "ln -sfn",
            content,
            "macshell-start must use 'ln -sfn' to cleanly update symlinks without failure",
        )

    def test_wayland_display_polling_upper_bound(self):
        """T2-F12-4: Boundary: Verify display socket loop has an upper bound (<= 50 iterations / 5s)."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        self.assertIn("sleep 0.1", content, "Polling interval should be 0.1s")
        self.assertTrue(
            "-lt 50" in content or "-lt 60" in content or "-lt 100" in content,
            "Polling loop must have finite upper limit to prevent infinite hang if compositor crashes",
        )

    def test_user_state_directory_creation(self):
        """T2-F12-5: Boundary: Verify macshell-start ensures user state and config directories exist."""
        content = read_repo_file("pkgs/enerco-macshell/macshell-start")
        self.assertIn("mkdir -p", content, "macshell-start must create directories with mkdir -p")
        self.assertIn(".config/quickshell", content)


if __name__ == "__main__":
    unittest.main()
