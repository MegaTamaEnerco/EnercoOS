"""Tier 1: Feature 9 - Calamares Launcher Privilege & Desktop Cleanup Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R1), PROJECT.md (Feature 9), TEST_INFRA.md, Survey 2 finding 3.3/3.4.
Validates prevention of installer desktop icon leakage to target user skeletons,
privilege elevation in enerco-installer, sudoers policy, and live media detection in enerco-welcome.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF09CalamaresPrivilege(unittest.TestCase):
    """Tier 1 test suite for Feature 9: Calamares Launcher Privilege & Desktop Cleanup."""

    def test_calamares_desktop_not_installed_to_skel(self):
        """T1-F09-1: Verify pkgs/enerco-calamares-config/PKGBUILD does not install to /etc/skel/Desktop."""
        content = read_repo_file("pkgs/enerco-calamares-config/PKGBUILD")
        # Leakage bug: install -Dm755 "${srcdir}/calamares.desktop" "${pkgdir}/etc/skel/Desktop/calamares.desktop"
        self.assertNotIn(
            "etc/skel/Desktop/calamares.desktop",
            content,
            "calamares.desktop must not be installed into /etc/skel/Desktop (it leaks to target users)",
        )

    def test_calamares_desktop_exec_points_to_enerco_installer(self):
        """T1-F09-2: Verify calamares.desktop entry uses /usr/local/bin/enerco-installer."""
        content = read_repo_file("pkgs/enerco-calamares-config/calamares.desktop")
        self.assertIn(
            "Exec=/usr/local/bin/enerco-installer",
            content,
            "calamares.desktop must invoke /usr/local/bin/enerco-installer",
        )

    def test_enerco_installer_preserves_display_environment(self):
        """T1-F09-3: Verify enerco-installer wrapper preserves Wayland display environment with sudo -E."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-enterprise-tools/enerco-installer"),
            "pkgs/enerco-enterprise-tools/enerco-installer must exist",
        )
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-installer")
        self.assertIn("sudo -E", content, "enerco-installer must use sudo -E to preserve Wayland display socket")
        self.assertIn("WAYLAND_DISPLAY", content, "enerco-installer must forward WAYLAND_DISPLAY")

    def test_liveuser_sudoers_grants_nopasswd(self):
        """T1-F09-4: Verify airootfs/etc/sudoers.d/00-liveuser grants NOPASSWD to enerco live user."""
        self.assertTrue(
            repo_file_exists("airootfs/etc/sudoers.d/00-liveuser"),
            "airootfs/etc/sudoers.d/00-liveuser must exist",
        )
        content = read_repo_file("airootfs/etc/sudoers.d/00-liveuser")
        self.assertTrue(
            "enerco ALL=(ALL:ALL) NOPASSWD: ALL" in content or "NOPASSWD" in content,
            "00-liveuser must allow passwordless execution for live installer session",
        )

    def test_enerco_welcome_detects_live_environment_properly(self):
        """T1-F09-5: Verify enerco-welcome checks for live ISO media (/run/archiso) before showing installer button."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-enterprise-tools/enerco-welcome"),
            "pkgs/enerco-enterprise-tools/enerco-welcome must exist",
        )
        content = read_repo_file("pkgs/enerco-enterprise-tools/enerco-welcome")
        # Defect in survey 2: uses os.path.exists("/usr/local/bin/enerco-installer") which exists on target!
        # Should check /run/archiso
        self.assertIn(
            "/run/archiso",
            content,
            "enerco-welcome must check for /run/archiso (live environment) before showing Install button",
        )


if __name__ == "__main__":
    unittest.main()
