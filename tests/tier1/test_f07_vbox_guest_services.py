"""Tier 1: Feature 7 - Target VirtualBox Guest Services Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 7), TEST_INFRA.md, Survey 2 finding 3.1.
Validates Calamares services-systemd.conf inclusion of vboxservice, packages.x86_64 guest utils,
and enablement in target systemd sequence.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF07VBoxGuestServices(unittest.TestCase):
    """Tier 1 test suite for Feature 7: Target VirtualBox Guest Services."""

    def test_services_systemd_conf_includes_vboxservice(self):
        """T1-F07-1: Verify pkgs/enerco-calamares-config/services-systemd.conf enables vboxservice."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/services-systemd.conf"),
            "pkgs/enerco-calamares-config/services-systemd.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        self.assertTrue(
            "vboxservice" in content or "vboxservice.service" in content,
            "services-systemd.conf must include vboxservice unit to support target VirtualBox VMs",
        )

    def test_packages_x86_64_includes_virtualbox_guest_utils(self):
        """T1-F07-2: Verify packages.x86_64 contains virtualbox-guest-utils."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "virtualbox-guest-utils",
            packages,
            "packages.x86_64 must include virtualbox-guest-utils for VM integration",
        )

    def test_vboxservice_unit_is_enabled_action(self):
        """T1-F07-3: Verify vboxservice unit in services-systemd.conf specifies action: enable."""
        content = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        # Check that vboxservice has action: "enable"
        lines = content.splitlines()
        found_vbox = False
        action_enable = False
        for i, line in enumerate(lines):
            if "name:" in line and "vboxservice" in line:
                found_vbox = True
                # Check next few lines for action: "enable"
                for j in range(i + 1, min(i + 5, len(lines))):
                    if "action:" in lines[j] and "enable" in lines[j]:
                        action_enable = True
                        break
        self.assertTrue(
            found_vbox and action_enable,
            "vboxservice must be defined with action: 'enable' in services-systemd.conf",
        )

    def test_calamares_settings_executes_services_systemd(self):
        """T1-F07-4: Verify Calamares settings.conf includes services-systemd in execution sequence."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/settings.conf"),
            "pkgs/enerco-calamares-config/settings.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/settings.conf")
        self.assertIn(
            "services-systemd",
            content,
            "settings.conf sequence must execute services-systemd module",
        )

    def test_live_airootfs_guest_modules_or_services(self):
        """T1-F07-5: Verify live environment supports virtualbox guest kernel modules/services."""
        # Check packages or mkinitcpio presets
        content = read_repo_file("packages.x86_64")
        self.assertTrue(
            "virtualbox-guest-utils" in content,
            "Live environment must have virtualbox-guest-utils packaged for hypervisor integration",
        )


if __name__ == "__main__":
    unittest.main()
