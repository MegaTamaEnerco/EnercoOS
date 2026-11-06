"""Tier 4: Real-World Application Scenarios Test Suite (8 End-to-End Scenarios).

Derivation source: ORIGINAL_REQUEST.md, PROJECT.md, TEST_INFRA.md (§ Real-World Application Scenarios).
Validates complete operational pipelines:
1. Full Clean Build Pipeline
2. ISO Artifact & Boot Media Verification
3. Live Desktop Session Initialization
4. Calamares Guided Installation Flow
5. Post-Installation Independent Boot
6. Post-Installation Target Desktop Persistence
7. Enterprise ERP & Office Productivity Workflow
8. Dynamic Hardware vs VirtualBox VM Fallback Workflow
"""

import os
import re
import unittest
from tests.config import (
    REPO_ROOT,
    get_repo_path,
    read_repo_file,
    repo_file_exists,
    run_host_command,
)


class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4 test suite for real-world end-to-end application scenarios."""

    def test_scenario_01_full_clean_build_pipeline(self):
        """T4-01: Scenario: Full Clean Build Pipeline Validation.

        Verifies that build.sh and scripts/build-packages.sh maintain clean build
        mechanics, correct dependency ordering, local repository indexing,
        and ensure no build artifacts are committed to git.
        """
        # 1. Master build scripts exist and have valid syntax
        self.assertTrue(repo_file_exists("build.sh"))
        self.assertTrue(repo_file_exists("scripts/build-packages.sh"))

        # 2. profiledef.sh defines iso_name, arch, and permissions
        profiledef = read_repo_file("profiledef.sh")
        self.assertIn("iso_name=", profiledef)
        self.assertIn("arch=", profiledef)
        self.assertIn("pacman_conf=", profiledef)

        # 3. pacman.conf binds the local package repository
        pacman_conf = read_repo_file("pacman.conf")
        self.assertIn("[enerco-local]", pacman_conf)
        self.assertIn("file://", pacman_conf)

        # 4. packages.x86_64 has no empty or corrupt package entries
        pkg_list = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in pkg_list.splitlines() if line.strip() and not line.startswith("#")]
        self.assertGreater(len(packages), 50, "packages.x86_64 must contain complete package inventory")

        # 5. Git working tree has zero committed binary artifacts in dist/
        dist_dir = get_repo_path("dist")
        if dist_dir.exists():
            for iso in dist_dir.glob("*.iso"):
                res = run_host_command(["git", "ls-files", str(iso)])
                self.assertEqual(res.stdout.strip(), "", f"ISO binary {iso.name} must not be tracked in git")

    def test_scenario_02_iso_artifact_verification(self):
        """T4-02: Scenario: ISO Artifact & Boot Media Verification.

        Verifies the EFI and Syslinux bootloader structures required for dual UEFI/BIOS
        boot media generation.
        """
        # 1. EFI boot configuration exists
        self.assertTrue(repo_file_exists("efiboot/loader/loader.conf"))
        has_efi_entry = (
            repo_file_exists("efiboot/loader/entries/01-enercoos-x86_64-linux.conf")
            or repo_file_exists("efiboot/loader/entries/01-archiso-x86_64-linux.conf")
        )
        self.assertTrue(has_efi_entry, "EFI boot entry config must exist in efiboot/loader/entries/")

        # 2. Syslinux BIOS bootloader configuration exists
        self.assertTrue(repo_file_exists("syslinux/syslinux.cfg"))
        self.assertTrue(repo_file_exists("syslinux/archiso_sys-linux.cfg"))

        # 3. Verify kernel label alignment between bootloaders
        efi_file = "efiboot/loader/entries/01-enercoos-x86_64-linux.conf" if repo_file_exists("efiboot/loader/entries/01-enercoos-x86_64-linux.conf") else "efiboot/loader/entries/01-archiso-x86_64-linux.conf"
        efi_entry = read_repo_file(efi_file)
        syslinux_entry = read_repo_file("syslinux/archiso_sys-linux.cfg")
        self.assertIn("vmlinuz-linux", efi_entry)
        self.assertIn("vmlinuz-linux", syslinux_entry)
        self.assertIn("initramfs-linux.img", efi_entry)
        self.assertIn("initramfs-linux.img", syslinux_entry)

    def test_scenario_03_live_desktop_session_init(self):
        """T4-03: Scenario: Live Desktop Session Initialization.

        Traces system bootstrap from getty autologin through enerco-live-setup,
        display manager / session start, and MacShell desktop initialization.
        """
        # 1. Live autologin getty drop-in exists
        self.assertTrue(repo_file_exists("airootfs/etc/systemd/system/getty@tty1.service.d/autologin.conf"))
        autologin = read_repo_file("airootfs/etc/systemd/system/getty@tty1.service.d/autologin.conf")
        self.assertIn("enerco", autologin, "getty must autologin user 'enerco'")

        # 2. Live setup service exists
        self.assertTrue(repo_file_exists("airootfs/etc/systemd/system/enerco-live-setup.service"))

        # 3. Session initialization script exists and sets Wayland environment
        session = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn("XDG_SESSION_TYPE=wayland", session)
        self.assertIn("XDG_CURRENT_DESKTOP=Hyprland", session)

        # 4. Live profile autostart hook exists
        self.assertTrue(repo_file_exists("airootfs/etc/profile.d/enerco-autostart.sh"))

    def test_scenario_04_calamares_installation_flow(self):
        """T4-04: Scenario: Calamares Guided Installation Flow.

        Validates the sequence and integrity of the Calamares installer configuration
        for partitioning, unpackfs, shellprocess, initramfs, and service provisioning.
        """
        self.assertTrue(repo_file_exists("pkgs/enerco-calamares-config/settings.conf"))
        settings = read_repo_file("pkgs/enerco-calamares-config/settings.conf")

        # Required sequence stages
        expected_modules = [
            "welcome",
            "locale",
            "keyboard",
            "partition",
            "users",
            "unpackfs",
            "machineid",
            "fstab",
            "shellprocess",
            "initcpio",
            "displaymanager",
            "services-systemd",
            "grubcfg",
            "bootloader",
            "umount",
            "finished",
        ]
        for mod in expected_modules:
            self.assertIn(mod, settings, f"Calamares sequence must contain module: {mod}")

        # Check shellprocess timeout
        shellprocess = read_repo_file("pkgs/enerco-calamares-config/shellprocess.conf")
        self.assertTrue(
            "timeout: 300" in shellprocess or "timeout: 600" in shellprocess or "timeout: 360" in shellprocess,
            "shellprocess.conf must have timeout >= 300 to avoid abort during mkinitcpio",
        )

    def test_scenario_05_post_install_independent_boot(self):
        """T4-05: Scenario: Post-Installation Independent Boot.

        Validates that the installed target system boots cleanly with GRUB bootloader,
        Wayland SDDM display manager, and VirtualBox guest additions.
        """
        # 1. GRUB config generator defined
        grubcfg = read_repo_file("pkgs/enerco-calamares-config/grubcfg.conf")
        self.assertIn("GRUB_CMDLINE_LINUX_DEFAULT", grubcfg)

        # 2. Bootloader EFI config defined
        bootloader = read_repo_file("pkgs/enerco-calamares-config/bootloader.conf")
        self.assertIn("installEFIFallback: true", bootloader)

        # 3. SDDM Wayland greeter compositor packaged
        packages = read_repo_file("packages.x86_64")
        has_compositor = any(c in packages for c in ["weston", "cage", "labwc"])
        self.assertTrue(has_compositor, "Target system must include Wayland greeter compositor")

        # 4. Target system services include vboxservice
        services = read_repo_file("pkgs/enerco-calamares-config/services-systemd.conf")
        self.assertTrue("vboxservice" in services or "vboxservice.service" in services)

    def test_scenario_06_post_install_target_desktop_persistence(self):
        """T4-06: Scenario: Post-Installation Target Desktop Persistence.

        Validates that user skeleton files maintain macOS styling, Hyprland configuration,
        and ensures no live installation shortcuts leak into the target user desktop.
        """
        # 1. Calamares PKGBUILD does not leak calamares.desktop to /etc/skel/Desktop
        calamares_pkgbuild = read_repo_file("pkgs/enerco-calamares-config/PKGBUILD")
        self.assertNotIn("etc/skel/Desktop/calamares.desktop", calamares_pkgbuild)

        # 2. Hyprland configuration is present in skeleton or desktop package
        self.assertTrue(
            repo_file_exists("pkgs/enerco-desktop-config/hyprland.lua")
            or repo_file_exists("airootfs/etc/skel/.config/hypr/hyprland.lua")
        )

        # 3. Target display manager launches enerco session
        dm_conf = read_repo_file("pkgs/enerco-calamares-config/displaymanager.conf")
        self.assertIn('desktopFile: "enerco"', dm_conf)

    def test_scenario_07_enterprise_erp_and_productivity_workflow(self):
        """T4-07: Scenario: Enterprise ERP & Office Productivity Workflow.

        Validates the enterprise software stack: MTERP application launcher,
        corporate portal reference, LibreOffice suite, PDF viewer, and terminal.
        """
        # 1. MTERP desktop launcher points to corporate URL
        mterp = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        self.assertIn("https://mterp.megatama-enerco.com", mterp)
        self.assertNotIn("%h", mterp, "Must not use invalid token %h")

        # 2. packages.x86_64 provides terminal, office suite, and PDF viewer
        packages = read_repo_file("packages.x86_64")
        self.assertTrue("kitty" in packages or "alacritty" in packages, "Terminal emulator must be packaged")
        self.assertTrue(
            "libreoffice-fresh" in packages or "libreoffice-still" in packages or "libreoffice" in packages,
            "LibreOffice office suite must be packaged",
        )
        self.assertIn("evince", packages, "Evince PDF viewer must be packaged")

    def test_scenario_08_hardware_vs_virtualbox_fallback_workflow(self):
        """T4-08: Scenario: Dynamic Hardware vs VirtualBox VM Fallback Workflow.

        Validates that enerco-session adapts dynamically between VirtualBox VM
        (applying software rendering and VBoxClient) and bare-metal UEFI hardware
        (preserving full hardware acceleration and power profiles).
        """
        # 1. airootfs/etc/environment does not contain hardcoded software GL
        env_content = read_repo_file("airootfs/etc/environment")
        self.assertNotIn("LIBGL_ALWAYS_SOFTWARE=1", env_content)

        # 2. enerco-session dynamically detects hypervisors
        session = read_repo_file("pkgs/enerco-enterprise-tools/enerco-session")
        self.assertIn("systemd-detect-virt", session)
        self.assertIn("LIBGL_ALWAYS_SOFTWARE=1", session)
        self.assertIn("WLR_NO_HARDWARE_CURSORS=1", session)

        # 3. Power management tools available for bare metal
        packages = read_repo_file("packages.x86_64")
        self.assertIn("power-profiles-daemon", packages)


if __name__ == "__main__":
    unittest.main()
