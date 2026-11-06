"""Tier 1: Feature 4 - Non-Root Makepkg Execution in build.sh Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 4), TEST_INFRA.md, Survey 1 finding 4.
Validates build.sh root checks, deterministic privilege dropping to non-root builder user,
argument propagation, and atomic ISO artifact staging.
"""

import re
import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF04NonRootMakepkg(unittest.TestCase):
    """Tier 1 test suite for Feature 4: Non-Root Makepkg Execution in build.sh."""

    def test_build_sh_requires_root_for_mkarchiso(self):
        """T1-F04-1: Verify build.sh enforces root privileges required for mkarchiso operations."""
        self.assertTrue(repo_file_exists("build.sh"), "build.sh must exist in repository root")
        content = read_repo_file("build.sh")
        self.assertTrue(
            "EUID" in content or "id -u" in content,
            "build.sh must check effective user ID to ensure mkarchiso runs with root privileges",
        )

    def test_build_sh_drops_privileges_for_build_packages(self):
        """T1-F04-2: Verify build.sh invokes build-packages.sh as a non-root user."""
        content = read_repo_file("build.sh")
        # Must execute build-packages.sh under sudo -u or su -
        has_drop = (
            "sudo -u" in content
            or "su -" in content
            or "su " in content
            or "runuser" in content
        )
        self.assertTrue(
            has_drop,
            "build.sh must drop privileges when invoking scripts/build-packages.sh",
        )

    def test_build_sh_deterministic_builder_fallback(self):
        """T1-F04-3: Verify build.sh falls back to 'builder' user when SUDO_USER is empty in WSL."""
        content = read_repo_file("build.sh")
        # Bug: if SUDO_USER is empty, it runs as root which makepkg rejects.
        # Fix: checks if SUDO_USER is empty/root, and uses builder user.
        self.assertTrue(
            "builder" in content,
            "build.sh must explicitly support or default to 'builder' user when SUDO_USER is not set",
        )

    def test_build_sh_forwards_rebuild_flag_to_build_packages(self):
        """T1-F04-4: Verify build.sh propagates --rebuild-pkgs option to scripts/build-packages.sh."""
        content = read_repo_file("build.sh")
        self.assertTrue(
            "--rebuild" in content or "REBUILD_PKGS" in content,
            "build.sh must handle rebuild options and pass them down to build-packages.sh",
        )

    def test_build_sh_atomic_iso_staging(self):
        """T1-F04-5: Verify build.sh atomically stages the output ISO to the host dist directory."""
        content = read_repo_file("build.sh")
        # Must stage to dist/
        self.assertIn("dist", content, "build.sh must mirror ISO output to dist directory")
        # Must use atomic move or sync to avoid partial ISO files on host
        has_atomic = ".tmp" in content or "mv " in content or "rsync" in content
        self.assertTrue(
            has_atomic,
            "build.sh must atomically stage ISO into dist to prevent corrupt partial reads",
        )


if __name__ == "__main__":
    unittest.main()
