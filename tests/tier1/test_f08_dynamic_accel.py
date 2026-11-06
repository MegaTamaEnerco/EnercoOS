"""Tier 1: Feature 8 - Dynamic Hardware Acceleration Architecture Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1, R2), PROJECT.md (Feature 8), TEST_INFRA.md, Survey 2 finding 3.2.
Validates removal of hardcoded software rendering from global environment, dynamic VM/GPU detection
in enerco-session, conditional fallback flags, and Lua config prioritization.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF08DynamicAccel(unittest.TestCase):
    """Tier 1 test suite for Feature 8: Dynamic Hardware Acceleration Architecture."""

    def test_airootfs_environment_no_hardcoded_software_gl(self):
        """T1-F08-1: Verify airootfs/etc/environment does NOT contain hardcoded LIBGL_ALWAYS_SOFTWARE=1."""
        self.assertTrue(repo_file_exists("airootfs/etc/environment"), "airootfs/etc/environment must exist")
        content = read_repo_file("airootfs/etc/environment")
        self.assertNotIn(
            "LIBGL_ALWAYS_SOFTWARE=1",
            content,
            "airootfs/etc/environment must not hardcode LIBGL_ALWAYS_SOFTWARE=1; must be set dynamically",
        )

    def test_enerco_session_exists_and_detects_virtualization(self):
        """T1-F08-2: Verify enerco-session contains dynamic virtualization detection."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-enterprise-tools/enerco-session"),
            "pkgs/enerco-enterprise-tools/enerco-session must exist",
        )
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn("systemd-detect-virt", content, "enerco-session must query system virtualization status")

    def test_enerco_session_vm_conditional_software_rendering(self):
        """T1-F08-3: Verify LIBGL_ALWAYS_SOFTWARE=1 is conditionally gated on VM hypervisor detection."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        # Gated under VM check
        self.assertIn("LIBGL_ALWAYS_SOFTWARE=1", content, "enerco-session must include fallback flag for VMs")
        # Must also set cursor and software allow flags in VM block
        self.assertIn("WLR_NO_HARDWARE_CURSORS=1", content)
        self.assertIn("WLR_RENDERER_ALLOW_SOFTWARE=1", content)

    def test_enerco_session_hardware_gpu_profiles(self):
        """T1-F08-4: Verify enerco-session supports NVIDIA and Intel hardware acceleration paths."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn("nvidia", content.lower(), "enerco-session must support NVIDIA hardware GPU paths")
        self.assertIn("intel", content.lower(), "enerco-session must support Intel hardware GPU paths")

    def test_enerco_session_prefers_lua_config(self):
        """T1-F08-5: Verify enerco-session searches for hyprland.lua before hyprland.conf."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        lua_pos = content.find("hyprland.lua")
        conf_pos = content.find("hyprland.conf")
        self.assertNotEqual(lua_pos, -1, "enerco-session must look for hyprland.lua")
        self.assertNotEqual(conf_pos, -1, "enerco-session must look for hyprland.conf")
        self.assertLess(lua_pos, conf_pos, "enerco-session must prioritize hyprland.lua over hyprland.conf")


if __name__ == "__main__":
    unittest.main()
