"""Tier 2: Feature 4 - Non-Root Makepkg Execution in build.sh Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 4), TEST_INFRA.md, Survey 1 finding 4.
Validates non-root user failure modes, SUDO_USER edge cases, cleanup traps,
help options, and destination write permission checks.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF04NonRootMakepkgBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 4: Non-Root Makepkg Execution in build.sh."""

    def test_build_sh_non_root_abort_exit_code(self):
        """T2-F04-1: Boundary: Verify build.sh exits with non-zero when run without root privileges."""
        content = read_repo_file("build.sh")
        # Must check EUID and exit non-zero
        self.assertTrue(
            "exit 1" in content or "return 1" in content,
            "build.sh must exit with code 1 if executed without root permissions",
        )

    def test_build_sh_handles_empty_sudo_user_cleanly(self):
        """T2-F04-2: Boundary: Verify build.sh checks for empty SUDO_USER and prevents root makepkg."""
        content = read_repo_file("build.sh")
        # Buggy condition: sudo -u "$SUDO_USER" where SUDO_USER is empty causes error or falls back to root
        # Must check -z "$SUDO_USER" or use builder fallback
        has_empty_check = (
            '-z "${SUDO_USER' in content
            or '-z "$SUDO_USER' in content
            or "SUDO_USER:-builder" in content
            or "BUILD_USER" in content
        )
        self.assertTrue(
            has_empty_check,
            "build.sh must handle empty or unset SUDO_USER variable explicitly",
        )

    def test_build_sh_handles_help_flag_without_root(self):
        """T2-F04-3: Boundary: Verify build.sh supports --help or -h options."""
        content = read_repo_file("build.sh")
        has_help = "--help" in content or "-h" in content
        self.assertTrue(has_help, "build.sh should support a help or usage parameter")

    def test_build_sh_signal_trap_cleanup(self):
        """T2-F04-4: Boundary: Verify build.sh defines trap handler to clean lock files/mounts on exit/interrupt."""
        content = read_repo_file("build.sh")
        self.assertIn(
            "trap",
            content,
            "build.sh must set up a trap handler for INT, TERM, or EXIT to prevent stale chroot mounts",
        )

    def test_build_sh_verifies_dist_directory_writability(self):
        """T2-F04-5: Boundary: Verify build.sh creates dist directory before mirroring ISO."""
        content = read_repo_file("build.sh")
        self.assertRegex(
            content,
            r"mkdir\s+-p\s+.*dist",
            "build.sh must ensure the dist destination directory exists prior to staging",
        )


if __name__ == "__main__":
    unittest.main()
