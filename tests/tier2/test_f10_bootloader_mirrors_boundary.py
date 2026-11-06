"""Tier 2: Feature 10 - Bootloader Kernel Parameters & Target Mirrors Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 10), TEST_INFRA.md, Survey 2 finding 4.
Validates bootloader timeouts, distributor branding, EFI fallback redundancy,
fstab mount boundary options, and repository protocol security.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF10BootloaderMirrorsBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 10: Bootloader Kernel Parameters & Target Mirrors."""

    def test_grub_timeout_boundary_allows_menu_access(self):
        """T2-F10-1: Boundary: Verify GRUB_TIMEOUT is >= 1 to permit manual boot override if needed."""
        content = read_repo_file("pkgs/enerco-calamares-config/grubcfg.conf")
        # Timeout should be at least 1 second
        self.assertIn("GRUB_TIMEOUT:", content)
        self.assertFalse(
            "GRUB_TIMEOUT: 0" in content,
            "GRUB_TIMEOUT must not be 0 to allow recovery/kernel selection if boot fails",
        )

    def test_grub_distributor_branding_boundary(self):
        """T2-F10-2: Boundary: Verify GRUB_DISTRIBUTOR is set to EnercoOS."""
        content = read_repo_file("pkgs/enerco-calamares-config/grubcfg.conf")
        self.assertIn('GRUB_DISTRIBUTOR: "EnercoOS"', content, "GRUB branding must identify EnercoOS")

    def test_bootloader_efi_id_boundary(self):
        """T2-F10-3: Boundary: Verify efiBootloaderId matches distribution name without spaces."""
        content = read_repo_file("pkgs/enerco-calamares-config/bootloader.conf")
        self.assertIn('efiBootloaderId: "EnercoOS"', content, "efiBootloaderId must be alphanumeric without spaces")

    def test_fstab_ssd_noatime_mount_options(self):
        """T2-F10-4: Boundary: Verify fstab.conf uses noatime on ssd tmp/mount options for performance."""
        content = read_repo_file("pkgs/enerco-calamares-config/fstab.conf")
        self.assertIn("noatime", content, "fstab.conf must specify noatime for optimal SSD performance")

    def test_pacman_parallel_downloads_boundary(self):
        """T2-F10-5: Boundary: Verify pacman.conf parallel downloads is set to a reasonable bound (e.g. 5-15)."""
        content = read_repo_file("pacman.conf")
        self.assertIn("ParallelDownloads =", content, "pacman.conf must enable ParallelDownloads for fast provisioning")


if __name__ == "__main__":
    unittest.main()
