"""Tier 2: Feature 8 - Dynamic Hardware Acceleration Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1, R2), PROJECT.md (Feature 8), TEST_INFRA.md, Survey 2 finding 3.2.
Validates virtualization detection fallback behavior, lspci error resilience,
socket readiness timeouts, and isolation of software cursor workarounds.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF08DynamicAccelBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 8: Dynamic Hardware Acceleration Architecture."""

    def test_virt_detect_command_failure_fallback(self):
        """T2-F08-1: Boundary: Verify enerco-session handles missing systemd-detect-virt with safe fallback."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn(
            "systemd-detect-virt 2>/dev/null || echo",
            content,
            "enerco-session must redirect stderr and fallback to echo on detect-virt failure",
        )

    def test_lspci_command_failure_fallback(self):
        """T2-F08-2: Boundary: Verify enerco-session handles missing lspci command with safe fallback."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn("lspci 2>/dev/null", content, "enerco-session must redirect lspci stderr to /dev/null")
        self.assertTrue(
            "|| echo" in content or "|| true" in content or '|| echo ""' in content,
            "enerco-session must provide fallback echo if lspci pipeline fails",
        )

    def test_wayland_socket_polling_timeout_bound(self):
        """T2-F08-3: Boundary: Verify background launcher polling loop has a bounded timeout."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        # In enerco-session: for i in {1..60}; do ... sleep 0.2
        self.assertIn("{1..60}", content, "Background launcher loop must be bounded to ~12 seconds")
        self.assertIn("sleep 0.2", content, "Polling interval should be reasonably fast (e.g. 0.2s)")

    def test_wlr_no_hardware_cursors_scoped_to_vm_or_nvidia(self):
        """T2-F08-4: Boundary: Verify WLR_NO_HARDWARE_CURSORS is NOT unconditionally set on modern Intel/AMD."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        # In enerco-session, WLR_NO_HARDWARE_CURSORS is set inside the VM or NVIDIA blocks,
        # but NOT in the global defaults (lines 20-27).
        lines = content.splitlines()
        global_block = "\n".join(lines[18:27])
        self.assertNotIn(
            "WLR_NO_HARDWARE_CURSORS",
            global_block,
            "WLR_NO_HARDWARE_CURSORS must not be set globally; hardware cursors improve performance on Intel/AMD",
        )

    def test_hyprland_wrapper_fallback_command(self):
        """T2-F08-5: Boundary: Verify enerco-session falls back to direct Hyprland invocation if start-hyprland is absent."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn("command -v start-hyprland", content)
        self.assertIn("exec Hyprland", content, "enerco-session must fallback to exec Hyprland if start-hyprland wrapper is missing")


if __name__ == "__main__":
    unittest.main()
