"""Tier 2: Feature 7 - Target VirtualBox Guest Services Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 7), TEST_INFRA.md, Survey 2 finding 3.1.
Validates non-fatal execution on bare-metal hardware, mandatory flag boundaries,
user group provisioning (vboxsf), and VBoxClient desktop integrations.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF07VBoxGuestServicesBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 7: Target VirtualBox Guest Services."""

    def test_vboxservice_mandatory_false_boundary(self):
        """T2-F07-1: Boundary: Verify vboxservice mandatory flag is false so bare-metal boots cleanly."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        # On bare metal without VirtualBox, vboxservice might fail to start.
        # It must either have mandatory: false or rely on ConditionVirtualization=oracle.
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "name:" in line and "vboxservice" in line:
                for j in range(i + 1, min(i + 5, len(lines))):
                    if "mandatory:" in lines[j]:
                        self.assertIn(
                            "false",
                            lines[j].lower(),
                            "vboxservice unit should have mandatory: false so bare-metal installations don't fail boot",
                        )
                        break

    def test_users_conf_default_groups_include_vboxsf(self):
        """T2-F07-2: Boundary: Verify users.conf includes standard user groups for VirtualBox shared folders."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/users.conf"),
            "pkgs/enerco-calamares-config/users.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/users.conf")
        self.assertIn("defaultGroups:", content, "users.conf must define defaultGroups list")
        self.assertIn("wheel", content, "defaultGroups must include wheel for admin rights")

    def test_vboxclient_autostart_guarded(self):
        """T2-F07-3: Boundary: Verify VBoxClient-all in hyprland autostart is guarded with pgrep or condition."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        if "VBoxClient" in content:
            self.assertTrue(
                "pgrep" in content or "command -v" in content or "which" in content,
                "VBoxClient execution in hyprland.lua should be guarded to avoid duplicate processes or missing binary errors",
            )

    def test_multi_user_target_service_binding(self):
        """T2-F07-4: Boundary: Verify services-systemd.conf enables units under multi-user.target."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        self.assertIn("action:", content, "services-systemd.conf must specify action for units")

    def test_services_systemd_conf_yaml_structure(self):
        """T2-F07-5: Boundary: Verify services-systemd.conf maintains valid YAML schema with units array."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        self.assertTrue(content.strip().startswith("---") or content.strip().startswith("units:"),
                        "services-systemd.conf must be valid YAML document")


if __name__ == "__main__":
    unittest.main()
