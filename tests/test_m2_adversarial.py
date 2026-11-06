"""Adversarial stress-test suite for Milestone 2 implementations.

Tests dynamic GPU acceleration environments, installer privilege escalation,
polkit authentication rules, welcome assistant live detection, and target chroot cleanup.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
SESSION_SCRIPT = REPO_ROOT / "pkgs" / "enerco-enterprise-tools" / "enerco-session"
INSTALLER_SCRIPT = REPO_ROOT / "pkgs" / "enerco-enterprise-tools" / "enerco-installer"
WELCOME_SCRIPT = REPO_ROOT / "pkgs" / "enerco-enterprise-tools" / "enerco-welcome"
POLKIT_RULE = REPO_ROOT / "airootfs" / "etc" / "polkit-1" / "rules.d" / "49-calamares.rules"
SHELLPROCESS_CONF = REPO_ROOT / "pkgs" / "enerco-calamares-config" / "shellprocess.conf"
GRUBCFG_CONF = REPO_ROOT / "pkgs" / "enerco-calamares-config" / "grubcfg.conf"
BOOTLOADER_CONF = REPO_ROOT / "pkgs" / "enerco-calamares-config" / "bootloader.conf"
SERVICES_CONF = REPO_ROOT / "pkgs" / "enerco-calamares-config" / "services-systemd.conf"
USERS_CONF = REPO_ROOT / "pkgs" / "enerco-calamares-config" / "users.conf"
MIRRORLIST = REPO_ROOT / "airootfs" / "etc" / "pacman.d" / "mirrorlist"
PACKAGES_LIST = REPO_ROOT / "packages.x86_64"


def to_linux_path(p: Path) -> str:
    """Translates a Path object into a POSIX path suitable for WSL or native Linux."""
    if sys.platform == "win32":
        # Convert C:\... to /mnt/c/...
        drive = p.drive[0].lower()
        rest = p.as_posix()[2:]  # strip 'C:'
        return f"/mnt/{drive}{rest}"
    return p.as_posix()


def run_bash_cmd(cmd_or_script: str, cwd: Path = None) -> subprocess.CompletedProcess:
    """Executes a bash command either directly or through WSL on Windows."""
    if sys.platform == "win32":
        wsl_cmd = ["wsl", "-d", "archlinux", "bash", "-c", cmd_or_script]
        return subprocess.run(wsl_cmd, capture_output=True, text=True, timeout=20)
    else:
        return subprocess.run(["bash", "-c", cmd_or_script], capture_output=True, text=True, cwd=cwd, timeout=20)


def run_session_in_mock_env(virt_type="none", gpu_info="", dmi_product="", dmi_vendor=""):
    """Executes enerco-session inside a mocked hardware/virtualization environment.
    
    Returns a dictionary of all exported environment variables captured at Hyprland launch.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        env_dump_file = tmp_path / "env_dump.json"

        # Mock systemd-detect-virt
        virt_bin = bin_dir / "systemd-detect-virt"
        virt_exit = 0 if virt_type != "none" else 1
        virt_bin.write_text(f"#!/usr/bin/env bash\necho '{virt_type}'\nexit {virt_exit}\n", encoding="utf-8")
        virt_bin.chmod(0o755)

        # Mock lspci
        lspci_bin = bin_dir / "lspci"
        lspci_bin.write_text(f"#!/usr/bin/env bash\necho '{gpu_info}'\nexit 0\n", encoding="utf-8")
        lspci_bin.chmod(0o755)

        # Mock cat for /sys/class/dmi/id/
        cat_bin = bin_dir / "cat"
        cat_script = f"""#!/usr/bin/env bash
for arg in "$@"; do
    if [[ "$arg" == *"/product_name"* ]]; then
        echo '{dmi_product}'
        exit 0
    elif [[ "$arg" == *"/sys_vendor"* ]]; then
        echo '{dmi_vendor}'
        exit 0
    fi
done
exec /usr/bin/cat "$@"
"""
        cat_bin.write_text(cat_script, encoding="utf-8")
        cat_bin.chmod(0o755)

        # Mock start-hyprland and Hyprland
        hypr_bin = bin_dir / "start-hyprland"
        hypr_script = f"""#!/usr/bin/env bash
python3 -c "import os, json; json.dump(dict(os.environ), open('{to_linux_path(env_dump_file)}', 'w'))"
exit 0
"""
        hypr_bin.write_text(hypr_script, encoding="utf-8")
        hypr_bin.chmod(0o755)

        hypr_direct = bin_dir / "Hyprland"
        hypr_direct.write_text(hypr_script, encoding="utf-8")
        hypr_direct.chmod(0o755)

        # Runner bash script
        runner_bin = tmp_path / "run.sh"
        session_linux_path = to_linux_path(SESSION_SCRIPT)
        bin_linux_path = to_linux_path(bin_dir)
        tmp_linux_path = to_linux_path(tmp_path)
        runner_script = f"""#!/usr/bin/env bash
export PATH="{bin_linux_path}:$PATH"
export HOME="{tmp_linux_path}"
export XDG_RUNTIME_DIR="{tmp_linux_path}"
bash "{session_linux_path}"
"""
        runner_bin.write_text(runner_script, encoding="utf-8")
        runner_bin.chmod(0o755)

        # Execute
        res = run_bash_cmd(f'bash "{to_linux_path(runner_bin)}"')

        if not env_dump_file.exists():
            raise RuntimeError(
                f"Failed to capture environment from enerco-session.\n"
                f"stdout: {res.stdout}\nstderr: {res.stderr}"
            )

        with open(env_dump_file, "r", encoding="utf-8") as f:
            return json.load(f)


class TestM2DynamicGpuAccelerationAdversarial(unittest.TestCase):
    """Stress-test enerco-session under bare metal and simulated hypervisors."""

    def test_bare_metal_intel_uhd_graphics(self):
        """Simulate bare-metal Intel system: NO software rendering flags, native iHD VA-API."""
        env = run_session_in_mock_env(
            virt_type="none",
            gpu_info="00:02.0 VGA compatible controller: Intel Corporation CometLake-U GT2 [UHD Graphics] (rev 02)",
            dmi_product="XPS 13 9300",
            dmi_vendor="Dell Inc.",
        )
        self.assertNotIn("LIBGL_ALWAYS_SOFTWARE", env, "Bare metal Intel must not set LIBGL_ALWAYS_SOFTWARE")
        self.assertNotIn("WLR_NO_HARDWARE_CURSORS", env, "Bare metal Intel must not disable hardware cursors")
        self.assertNotIn("WLR_RENDERER_ALLOW_SOFTWARE", env, "Bare metal Intel must not allow software renderer")
        self.assertNotIn("AQ_NO_MODIFIERS", env, "Bare metal Intel must not disable Aquamarine modifiers")
        self.assertEqual(env.get("LIBVA_DRIVER_NAME"), "iHD", "Intel GPU must set LIBVA_DRIVER_NAME=iHD")

    def test_bare_metal_amd_radeon_rx6800(self):
        """Simulate bare-metal AMD system: NO software rendering flags, native mesa radeonsi."""
        env = run_session_in_mock_env(
            virt_type="none",
            gpu_info="03:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 21 [Radeon RX 6800/6800 XT / 6900 XT] (rev c1)",
            dmi_product="MS-7C37",
            dmi_vendor="Micro-Star International Co., Ltd.",
        )
        self.assertNotIn("LIBGL_ALWAYS_SOFTWARE", env, "Bare metal AMD must not set LIBGL_ALWAYS_SOFTWARE")
        self.assertNotIn("WLR_NO_HARDWARE_CURSORS", env, "Bare metal AMD must not disable hardware cursors")
        self.assertNotIn("WLR_RENDERER_ALLOW_SOFTWARE", env, "Bare metal AMD must not allow software renderer")
        self.assertNotIn("AQ_NO_MODIFIERS", env, "Bare metal AMD must not disable modifiers")
        self.assertNotIn("LIBVA_DRIVER_NAME", env, "AMD GPU must leave LIBVA_DRIVER_NAME to mesa default")

    def test_bare_metal_nvidia_rtx4090(self):
        """Simulate bare-metal NVIDIA system: native GPU acceleration with proprietary Wayland flags."""
        env = run_session_in_mock_env(
            virt_type="none",
            gpu_info="01:00.0 VGA compatible controller: NVIDIA Corporation AD102 [GeForce RTX 4090] (rev a1)",
            dmi_product="ROG CROSSHAIR X670E HERO",
            dmi_vendor="ASUSTeK COMPUTER INC.",
        )
        self.assertNotIn("LIBGL_ALWAYS_SOFTWARE", env, "Bare metal NVIDIA must NEVER set LIBGL_ALWAYS_SOFTWARE")
        self.assertNotIn("WLR_RENDERER_ALLOW_SOFTWARE", env, "Bare metal NVIDIA must not allow software rendering")
        self.assertEqual(env.get("LIBVA_DRIVER_NAME"), "nvidia")
        self.assertEqual(env.get("GBM_BACKEND"), "nvidia-drm")
        self.assertEqual(env.get("__GLX_VENDOR_LIBRARY_NAME"), "nvidia")
        self.assertEqual(env.get("WLR_NO_HARDWARE_CURSORS"), "1")
        self.assertEqual(env.get("AQ_NO_MODIFIERS"), "1")

    def test_virtualbox_detected_via_systemd_virt(self):
        """Simulate VirtualBox VM detected via systemd-detect-virt='oracle'."""
        env = run_session_in_mock_env(
            virt_type="oracle",
            gpu_info="00:02.0 VGA compatible controller: InnoTek Systemberatung GmbH VirtualBox Graphics Adapter",
            dmi_product="VirtualBox",
            dmi_vendor="innotek GmbH",
        )
        self.assertEqual(env.get("LIBGL_ALWAYS_SOFTWARE"), "1")
        self.assertEqual(env.get("WLR_NO_HARDWARE_CURSORS"), "1")
        self.assertEqual(env.get("WLR_RENDERER_ALLOW_SOFTWARE"), "1")
        self.assertEqual(env.get("AQ_NO_MODIFIERS"), "1")

    def test_virtualbox_detected_via_dmi_product_fallback(self):
        """Adversarial: systemd-detect-virt fails (returns 'none'), but DMI reveals VirtualBox."""
        env = run_session_in_mock_env(
            virt_type="none",
            gpu_info="00:02.0 Display controller: Unknown Vendor",
            dmi_product="VirtualBox",
            dmi_vendor="innotek GmbH",
        )
        self.assertEqual(env.get("LIBGL_ALWAYS_SOFTWARE"), "1", "DMI product 'VirtualBox' must trigger VM flags")
        self.assertEqual(env.get("WLR_RENDERER_ALLOW_SOFTWARE"), "1")

    def test_virtualbox_detected_via_lspci_gpu_fallback(self):
        """Adversarial: systemd-detect-virt fails and DMI is empty, but lspci shows VirtualBox Adapter."""
        env = run_session_in_mock_env(
            virt_type="none",
            gpu_info="00:02.0 VGA compatible controller: InnoTek Systemberatung GmbH VirtualBox Graphics Adapter",
            dmi_product="",
            dmi_vendor="",
        )
        self.assertEqual(env.get("LIBGL_ALWAYS_SOFTWARE"), "1", "lspci VirtualBox GPU must trigger VM flags")
        self.assertEqual(env.get("AQ_NO_MODIFIERS"), "1")

    def test_vmware_workstation_vm(self):
        """Simulate VMware VM detected via VIRT_TYPE=vmware."""
        env = run_session_in_mock_env(
            virt_type="vmware",
            gpu_info="00:0f.0 VGA compatible controller: VMware SVGA II Adapter",
            dmi_product="VMware Virtual Platform",
            dmi_vendor="VMware, Inc.",
        )
        self.assertEqual(env.get("LIBGL_ALWAYS_SOFTWARE"), "1")
        self.assertEqual(env.get("WLR_NO_HARDWARE_CURSORS"), "1")
        self.assertEqual(env.get("WLR_RENDERER_ALLOW_SOFTWARE"), "1")
        self.assertEqual(env.get("AQ_NO_MODIFIERS"), "1")

    def test_qemu_kvm_virtio_gpu(self):
        """Simulate QEMU/KVM with VirtIO-GPU."""
        env = run_session_in_mock_env(
            virt_type="kvm",
            gpu_info="00:01.0 VGA compatible controller: Red Hat, Inc. Virtio GPU",
            dmi_product="Standard PC (Q35 + ICH9, 2009)",
            dmi_vendor="QEMU",
        )
        self.assertEqual(env.get("LIBGL_ALWAYS_SOFTWARE"), "1")
        self.assertEqual(env.get("WLR_RENDERER_ALLOW_SOFTWARE"), "1")


class TestM2CalamaresLauncherElevationAdversarial(unittest.TestCase):
    """Stress-test enerco-installer display forwarding and polkit authentication."""

    def test_installer_wayland_socket_resolution_order(self):
        """Test enerco-installer selects wayland-0 if wayland-1 does not exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            runtime_dir = tmp_path / "runtime"
            runtime_dir.mkdir()
            (runtime_dir / "wayland-0").touch()

            # Mock sudo to capture the passed environment variables
            bin_dir = tmp_path / "bin"
            bin_dir.mkdir()
            sudo_capture = tmp_path / "sudo_env.json"
            sudo_mock = bin_dir / "sudo"
            sudo_mock.write_text(
                f"""#!/usr/bin/env bash
python3 -c "import os, json; json.dump(dict(os.environ), open('{to_linux_path(sudo_capture)}', 'w'))"
exit 0
""",
                encoding="utf-8",
            )
            sudo_mock.chmod(0o755)

            runner = tmp_path / "run_installer.sh"
            installer_path = to_linux_path(INSTALLER_SCRIPT)
            bin_linux = to_linux_path(bin_dir)
            runtime_linux = to_linux_path(runtime_dir)
            runner.write_text(
                f"""#!/usr/bin/env bash
export PATH="{bin_linux}:$PATH"
export XDG_RUNTIME_DIR="{runtime_linux}"
unset WAYLAND_DISPLAY
bash "{installer_path}"
""",
                encoding="utf-8",
            )
            runner.chmod(0o755)

            res = run_bash_cmd(f'bash "{to_linux_path(runner)}"')
            self.assertTrue(sudo_capture.exists(), f"Mock sudo was not executed: {res.stderr}")
            with open(sudo_capture, "r", encoding="utf-8") as f:
                captured = json.load(f)

            self.assertEqual(captured.get("WAYLAND_DISPLAY"), "wayland-0", "Must resolve to existing wayland-0 socket")
            self.assertEqual(captured.get("QT_QPA_PLATFORM"), "wayland;xcb", "Must pass wayland;xcb Qt platform")

    def test_installer_forwards_cli_arguments_to_calamares(self):
        """Test that command line arguments given to enerco-installer reach calamares."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            bin_dir = tmp_path / "bin"
            bin_dir.mkdir()
            args_capture = tmp_path / "args.json"

            sudo_mock = bin_dir / "sudo"
            sudo_mock.write_text(
                f"""#!/usr/bin/env bash
python3 -c "import sys, json; json.dump(sys.argv[1:], open('{to_linux_path(args_capture)}', 'w'))"
exit 0
""",
                encoding="utf-8",
            )
            sudo_mock.chmod(0o755)

            runner = tmp_path / "run_args.sh"
            installer_path = to_linux_path(INSTALLER_SCRIPT)
            bin_linux = to_linux_path(bin_dir)
            runner.write_text(
                f"""#!/usr/bin/env bash
export PATH="{bin_linux}:$PATH"
bash "{installer_path}" -d --config /tmp/custom.conf
""",
                encoding="utf-8",
            )
            runner.chmod(0o755)

            res = run_bash_cmd(f'bash "{to_linux_path(runner)}"')
            self.assertTrue(args_capture.exists(), f"Mock sudo args not captured: {res.stderr}")
            with open(args_capture, "r", encoding="utf-8") as f:
                passed_args = json.load(f)

            self.assertIn("-d", passed_args, "Must forward -d debug flag to calamares")
            self.assertIn("--config", passed_args, "Must forward --config flag to calamares")
            self.assertIn("/tmp/custom.conf", passed_args, "Must forward config argument")

    def test_polkit_rule_logic_matrix(self):
        """Adversarial evaluation of polkit rule matrix: action IDs vs subject identities."""
        rule_content = POLKIT_RULE.read_text(encoding="utf-8")

        # Simulate the polkit addRule JS logic in Python
        def evaluate_polkit_rule(action_id, user, groups):
            action = {"id": action_id}
            subject = {
                "user": user,
                "groups": groups,
                "isInGroup": lambda g: g in groups,
            }
            # Exact logic from 49-calamares.rules
            if (
                action["id"] in [
                    "com.github.calamares.calamares.pkexec.run",
                    "org.archlinux.pkexec.calamares",
                    "com.github.calamares.calamares",
                ]
            ) and (subject["isInGroup"]("wheel") or subject["user"] == "enerco"):
                return "YES"
            return None

        # Positive cases
        self.assertEqual(evaluate_polkit_rule("com.github.calamares.calamares.pkexec.run", "enerco", []), "YES")
        self.assertEqual(evaluate_polkit_rule("org.archlinux.pkexec.calamares", "enerco", []), "YES")
        self.assertEqual(evaluate_polkit_rule("com.github.calamares.calamares", "enerco", []), "YES")
        self.assertEqual(evaluate_polkit_rule("com.github.calamares.calamares.pkexec.run", "admin_user", ["wheel"]), "YES")

        # Adversarial / Negative cases
        self.assertIsNone(
            evaluate_polkit_rule("com.github.calamares.calamares.pkexec.run", "unprivileged_user", ["users"]),
            "Unprivileged non-wheel user must NOT get passwordless polkit YES",
        )
        self.assertIsNone(
            evaluate_polkit_rule("org.freedesktop.policykit.exec", "enerco", []),
            "General pkexec must NOT be granted by 49-calamares.rules",
        )
        self.assertIsNone(
            evaluate_polkit_rule("org.freedesktop.udisks2.filesystem-mount", "enerco", []),
            "UDisks2 must NOT be authorized by 49-calamares.rules",
        )
        self.assertIsNone(
            evaluate_polkit_rule("com.github.calamares.calamares.pkexec.run.evil", "enerco", []),
            "Action sub-id prefix injection must NOT match",
        )

        # Verify exact AST syntax in the actual rule file
        self.assertIn("action.id == \"com.github.calamares.calamares.pkexec.run\"", rule_content)
        self.assertIn("action.id == \"org.archlinux.pkexec.calamares\"", rule_content)
        self.assertIn("action.id == \"com.github.calamares.calamares\"", rule_content)
        self.assertIn("subject.isInGroup(\"wheel\")", rule_content)
        self.assertIn("subject.user == \"enerco\"", rule_content)
        self.assertIn("polkit.Result.YES", rule_content)


class TestM2WelcomeAndCleanupAdversarial(unittest.TestCase):
    """Stress-test enerco-welcome live environment detection and target desktop cleanup."""

    def test_welcome_assistant_live_vs_target_detection(self):
        """Verify enerco-welcome code gates the installer button strictly on /run/archiso."""
        welcome_code = WELCOME_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('os.path.exists("/run/archiso")', welcome_code)
        self.assertIn('os.path.exists("/usr/local/bin/enerco-installer")', welcome_code)
        self.assertIn('Install EnercoOS (Calamares)', welcome_code)

        # Ensure no unconditional installer button creation exists
        lines_with_install = [l for l in welcome_code.splitlines() if "Install EnercoOS" in l]
        self.assertEqual(len(lines_with_install), 1, "Install button must be created in exactly one conditional block")

    def test_shellprocess_target_chroot_cleanup_simulation(self):
        """Simulate shellprocess cleanup script on a target chroot directory hierarchy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            chroot = Path(tmpdir)
            chroot_linux = to_linux_path(chroot)

            # Create mock target files that should be cleaned
            (chroot / "etc" / "mkinitcpio.conf.d").mkdir(parents=True)
            (chroot / "etc" / "mkinitcpio.conf.d" / "archiso.conf").write_text("# archiso", encoding="utf-8")

            (chroot / "etc" / "systemd" / "system" / "multi-user.target.wants").mkdir(parents=True)
            (chroot / "etc" / "systemd" / "system" / "enerco-live-setup.service").write_text("# live", encoding="utf-8")
            (chroot / "etc" / "systemd" / "system" / "multi-user.target.wants" / "enerco-live-setup.service").write_text("# live", encoding="utf-8")

            (chroot / "etc" / "systemd" / "system" / "getty@tty1.service.d").mkdir(parents=True)
            (chroot / "etc" / "systemd" / "system" / "getty@tty1.service.d" / "autologin.conf").write_text("# auto", encoding="utf-8")

            (chroot / "etc" / "profile.d").mkdir(parents=True)
            (chroot / "etc" / "profile.d" / "enerco-autostart.sh").write_text("# auto", encoding="utf-8")

            (chroot / "etc" / "skel" / "Desktop").mkdir(parents=True)
            (chroot / "etc" / "skel" / "Desktop" / "calamares.desktop").write_text("# calamares", encoding="utf-8")

            (chroot / "home" / "targetuser" / "Desktop").mkdir(parents=True)
            (chroot / "home" / "targetuser" / "Desktop" / "calamares.desktop").write_text("# calamares", encoding="utf-8")

            (chroot / "usr" / "share" / "applications").mkdir(parents=True)
            (chroot / "usr" / "share" / "applications" / "calamares.desktop").write_text("# calamares", encoding="utf-8")

            (chroot / "etc" / "polkit-1" / "rules.d").mkdir(parents=True)
            (chroot / "etc" / "polkit-1" / "rules.d" / "49-calamares.rules").write_text("# polkit", encoding="utf-8")

            dock_dir = chroot / "etc" / "skel" / ".config" / "macdock"
            dock_dir.mkdir(parents=True)
            dock_file = dock_dir / "pinned.json"
            dock_file.write_text(json.dumps(["kitty", "calamares", "org.kde.dolphin"]), encoding="utf-8")

            # Extract cleanup commands from shellprocess.conf via PyYAML in WSL/Python
            extract_script = f"""python3 -c "import yaml, json; conf=yaml.safe_load(open('{to_linux_path(SHELLPROCESS_CONF)}')); json.dump(conf['script'], open('{to_linux_path(chroot / 'commands.json')}', 'w'))" """
            run_bash_cmd(extract_script)

            with open(chroot / "commands.json", "r", encoding="utf-8") as f:
                script_cmds = json.load(f)

            # Filter for cleanup commands
            cleanup_cmds = [
                c for c in script_cmds
                if any(k in c for k in ["calamares", "archiso", "enerco-live", "autologin", "pinned.json"])
            ]

            # Execute commands inside mock chroot directory
            for cmd in cleanup_cmds:
                clean_cmd = cmd.lstrip("-")
                # Replace absolute root paths with chroot paths
                adapted_cmd = clean_cmd.replace("/etc/", f"{chroot_linux}/etc/")
                adapted_cmd = adapted_cmd.replace("/home/", f"{chroot_linux}/home/")
                adapted_cmd = adapted_cmd.replace("/usr/", f"{chroot_linux}/usr/")

                res = run_bash_cmd(adapted_cmd)
                self.assertEqual(res.returncode, 0, f"Cleanup command failed: {adapted_cmd}\nstderr: {res.stderr}")

            # Assert all artifacts removed
            self.assertFalse((chroot / "etc" / "mkinitcpio.conf.d" / "archiso.conf").exists())
            self.assertFalse((chroot / "etc" / "systemd" / "system" / "enerco-live-setup.service").exists())
            self.assertFalse((chroot / "etc" / "systemd" / "system" / "multi-user.target.wants" / "enerco-live-setup.service").exists())
            self.assertFalse((chroot / "etc" / "systemd" / "system" / "getty@tty1.service.d" / "autologin.conf").exists())
            self.assertFalse((chroot / "etc" / "profile.d" / "enerco-autostart.sh").exists())
            self.assertFalse((chroot / "etc" / "skel" / "Desktop" / "calamares.desktop").exists())
            self.assertFalse((chroot / "home" / "targetuser" / "Desktop" / "calamares.desktop").exists())
            self.assertFalse((chroot / "usr" / "share" / "applications" / "calamares.desktop").exists())
            self.assertFalse((chroot / "etc" / "polkit-1" / "rules.d" / "49-calamares.rules").exists())

            # Verify pinned.json had calamares removed and preserved other pins
            with open(dock_file, "r", encoding="utf-8") as f:
                remaining_pins = json.load(f)
            self.assertNotIn("calamares", remaining_pins, "Calamares pin must be stripped from macdock")
            self.assertEqual(remaining_pins, ["kitty", "org.kde.dolphin"], "Other dock pins must remain intact")


class TestM2SystemConfigurationAdversarial(unittest.TestCase):
    """Stress-test bootloader, mirrorlist, and VirtualBox guest service configs."""

    def test_grubcfg_and_bootloader_kernel_parameters(self):
        """Verify grubcfg.conf has top-level kernel_params and bootloader.conf has kernelParams."""
        grub_content = GRUBCFG_CONF.read_text(encoding="utf-8")
        boot_content = BOOTLOADER_CONF.read_text(encoding="utf-8")

        # Must have top-level kernel_params in grubcfg.conf
        self.assertRegex(grub_content, r"(?m)^kernel_params:\s*$")
        self.assertIn('"quiet"', grub_content)
        self.assertIn('"splash"', grub_content)
        self.assertIn('"nowatchdog"', grub_content)
        self.assertIn('"zswap.enabled=0"', grub_content)
        self.assertIn('"mitigations=auto"', grub_content)

        # Must have top-level kernelParams in bootloader.conf
        self.assertRegex(boot_content, r"(?m)^kernelParams:\s*$")
        self.assertIn('"quiet"', boot_content)
        self.assertIn('"splash"', boot_content)

    def test_vboxservice_mandatory_false_boundary(self):
        """Verify vboxservice is configured with mandatory: false so bare metal does not fail."""
        content = SERVICES_CONF.read_text(encoding="utf-8")
        vbox_block = re.search(r"-\s*name:\s*[\"']?vboxservice[\"']?[\s\S]*?(?=-\s*name|\Z)", content)
        self.assertIsNotNone(vbox_block, "vboxservice must be listed in services-systemd.conf")
        self.assertIn('action: "enable"', vbox_block.group(0))
        self.assertIn("mandatory: false", vbox_block.group(0), "vboxservice must have mandatory: false")

    def test_pacman_target_mirrors_structure(self):
        """Verify airootfs pacman mirrorlist contains valid geo and CDN Server lines."""
        content = MIRRORLIST.read_text(encoding="utf-8")
        servers = [l.strip() for l in content.splitlines() if l.strip().startswith("Server = ")]
        self.assertGreaterEqual(len(servers), 2, "Must configure at least 2 active mirrors")
        for s in servers:
            self.assertTrue(s.startswith("Server = https://"), f"Mirror must use HTTPS: {s}")
            self.assertIn("$repo/os/$arch", s, f"Mirror must contain standard repo/arch path: {s}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
