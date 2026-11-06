"""Tier 1: Feature 10 - Bootloader Kernel Parameters & Target Mirrors Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 10), TEST_INFRA.md, Survey 2 finding 4.
Validates Calamares grubcfg.conf defaults, bootloader EFI settings, partition layout,
pacman repository definitions, and active mirrorlist/keyring provisioning.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF10BootloaderMirrors(unittest.TestCase):
    """Tier 1 test suite for Feature 10: Bootloader Kernel Parameters & Target Mirrors."""

    def test_grubcfg_kernel_command_line(self):
        """T1-F10-1: Verify grubcfg.conf sets clean enterprise kernel parameters (quiet splash)."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/grubcfg.conf"),
            "pkgs/enerco-calamares-config/grubcfg.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/grubcfg.conf")
        self.assertIn("GRUB_CMDLINE_LINUX_DEFAULT", content)
        self.assertIn("quiet", content, "Kernel cmdline must include 'quiet'")
        self.assertIn("splash", content, "Kernel cmdline must include 'splash'")

    def test_bootloader_conf_efi_fallback_enabled(self):
        """T1-F10-2: Verify bootloader.conf enables installEFIFallback for VirtualBox compatibility."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/bootloader.conf"),
            "pkgs/enerco-calamares-config/bootloader.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/bootloader.conf")
        self.assertIn("efiBootLoader:", content)
        self.assertIn(
            "installEFIFallback: true",
            content,
            "bootloader.conf must enable installEFIFallback to ensure VirtualBox NVRAM boot persistence",
        )

    def test_partition_conf_defines_efi_system_partition(self):
        """T1-F10-3: Verify partition.conf configures EFI system partition with adequate sizing."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-calamares-config/partition.conf"),
            "pkgs/enerco-calamares-config/partition.conf must exist",
        )
        content = read_repo_file("pkgs/enerco-calamares-config/partition.conf")
        self.assertIn("efiSystemPartition:", content, "partition.conf must specify efiSystemPartition")
        self.assertIn("efiSystemPartitionSize:", content, "partition.conf must define EFI partition size")

    def test_pacman_target_mirrors_and_keyring_provisioned(self):
        """T1-F10-4: Verify packages.x86_64 or airootfs provisions archlinux-keyring/reflector/mirrorlist."""
        content = read_repo_file("packages.x86_64")
        has_keyring = "archlinux-keyring" in content
        has_reflector = "reflector" in content
        has_mirrorlist = repo_file_exists("airootfs/etc/pacman.d/mirrorlist")
        self.assertTrue(
            has_keyring or has_reflector or has_mirrorlist,
            "System must provide archlinux-keyring, reflector, or active mirrorlist for post-install updates",
        )

    def test_pacman_conf_core_and_extra_channels(self):
        """T1-F10-5: Verify pacman.conf includes core and extra channels pointing to mirrorlist."""
        self.assertTrue(repo_file_exists("pacman.conf"), "pacman.conf must exist")
        content = read_repo_file("pacman.conf")
        self.assertIn("[core]", content, "pacman.conf must define [core]")
        self.assertIn("[extra]", content, "pacman.conf must define [extra]")
        self.assertIn("/etc/pacman.d/mirrorlist", content, "pacman.conf must include /etc/pacman.d/mirrorlist")


if __name__ == "__main__":
    unittest.main()
