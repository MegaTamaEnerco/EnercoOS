"""Tier 1: Feature 6 - Calamares Shellprocess Timeout Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 6), TEST_INFRA.md, Survey 2 finding 2.2.
Validates Calamares shellprocess.conf timeout configuration (>= 300s), chroot setting,
live artifact cleanup commands, and mkinitcpio execution.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF06ShellprocessTimeout(unittest.TestCase):
    """Tier 1 test suite for Feature 6: Calamares Shellprocess Timeout."""

    def test_shellprocess_conf_exists(self):
        """T1-F06-1: Verify pkgs/enerco-calamares-config/shellprocess.conf exists."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/shellprocess.conf"),
            "pkgs/enerco-calamares-config/shellprocess.conf must exist",
        )

    def test_shellprocess_timeout_at_least_300_seconds(self):
        """T1-F06-2: Verify shellprocess timeout is >= 300s to avoid mkinitcpio VM timeouts."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        # Extract timeout value
        timeout_val = None
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("timeout:"):
                try:
                    timeout_val = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
        self.assertIsNotNone(timeout_val, "timeout field must be defined in shellprocess.conf")
        self.assertGreaterEqual(
            timeout_val,
            300,
            f"shellprocess.conf timeout ({timeout_val}s) must be at least 300s to build 4 kernel initramfs images",
        )

    def test_shellprocess_dont_chroot_is_false(self):
        """T1-F06-3: Verify shellprocess executes within target chroot (dontChroot: false)."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        self.assertRegex(
            content,
            r"dontChroot:\s*false",
            "shellprocess.conf must have dontChroot: false to operate on the installed target filesystem",
        )

    def test_shellprocess_cleans_live_artifacts(self):
        """T1-F06-4: Verify shellprocess script cleans live user and live autologin units."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        # Must remove liveuser artifacts
        self.assertIn("enerco-live-setup.service", content, "Must clean enerco-live-setup.service from target")
        self.assertIn("autologin.conf", content, "Must clean autologin.conf from target getty")

    def test_shellprocess_executes_mkinitcpio(self):
        """T1-F06-5: Verify shellprocess script runs mkinitcpio -P to build initramfs."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        self.assertIn("mkinitcpio -P", content, "shellprocess script must run mkinitcpio -P across installed kernels")


if __name__ == "__main__":
    unittest.main()
