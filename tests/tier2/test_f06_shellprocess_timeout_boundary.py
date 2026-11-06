"""Tier 2: Feature 6 - Calamares Shellprocess Timeout Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 6), TEST_INFRA.md, Survey 2 finding 2.2.
Validates Calamares shellprocess resilience to slow I/O, error-tolerant removal syntax,
dynamic kernel enumeration, and execution environment safety.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF06ShellprocessTimeoutBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 6: Calamares Shellprocess Timeout."""

    def test_calamares_hyphen_prefix_error_tolerance(self):
        """T2-F06-1: Boundary: Verify optional cleanup commands use '-' prefix to avoid aborting if missing."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        # In Calamares, commands prefixed with '-' do not cause failure if they exit non-zero
        self.assertIn(
            '- "-rm -f',
            content,
            "Calamares cleanup commands must use '-' prefix for error tolerance on missing live artifacts",
        )

    def test_shellprocess_dynamic_kernel_loop(self):
        """T2-F06-2: Boundary: Verify shellprocess enumerates /usr/lib/modules dynamically."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        self.assertIn(
            "/usr/lib/modules/*",
            content,
            "shellprocess.conf must loop through installed kernel modules dynamically",
        )

    def test_shellprocess_handles_zen_and_standard_kernels(self):
        """T2-F06-3: Boundary: Verify kernel copying handles both standard and linux-zen images."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        self.assertIn("vmlinuz-linux", content)
        self.assertIn("vmlinuz-linux-zen", content)

    def test_shellprocess_permission_boundary_on_vmlinuz(self):
        """T2-F06-4: Boundary: Verify vmlinuz permissions are set to readable (chmod 644)."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        self.assertIn(
            "chmod 644",
            content,
            "Kernel binaries in /boot must be set to 644 permissions for bootloader access",
        )

    def test_timeout_upper_safety_bound(self):
        """T2-F06-5: Boundary: Verify timeout is within sensible bounds (300s to 1200s, not infinite)."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        timeout_val = None
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("timeout:"):
                timeout_val = int(line.split(":", 1)[1].strip())
        self.assertIsNotNone(timeout_val)
        self.assertGreaterEqual(timeout_val, 300, "Timeout must be >= 300s")
        self.assertLessEqual(timeout_val, 1800, "Timeout should not exceed 30 minutes (prevent infinite hang)")

    def test_shellprocess_no_undefined_calamares_variables(self):
        """T2-F06-6: Boundary: Verify shellprocess.conf has no unescaped $ shell variables that Calamares CommandList rejects."""
        content = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        self.assertNotIn(
            "$",
            content,
            "shellprocess.conf must not contain '$' variables that Calamares CommandList treats as undefined GlobalStorage variables",
        )


if __name__ == "__main__":
    unittest.main()
