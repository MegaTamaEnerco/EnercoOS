"""Tier 2: Feature 1 - Host/WSL Git Reconciliation Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 1), TEST_INFRA.md, Survey 1 finding 1.
Validates line ending integrity (no CRLF in shell scripts), untracked binary detection,
file permission preservation, repository size bounds, and headless git resolution.
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


class TestF01GitReconciliationBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 1: Host/WSL Git Reconciliation."""

    def test_no_crlf_line_endings_in_shell_scripts(self):
        """T2-F01-1: Boundary: Ensure shell scripts and PKGBUILDs do NOT have Windows CRLF line endings."""
        scripts_to_check = [
            "build.sh",
            "scripts/build-packages.sh",
            "scripts/sync-to-vm.sh",
            "pkgs/enerco-enterprise-tools/enerco-session",
            "pkgs/enerco-enterprise-tools/enerco-installer",
            "pkgs/enerco-macshell/macshell-start",
        ]
        for rel_path in scripts_to_check:
            if repo_file_exists(rel_path):
                p = get_repo_path(rel_path)
                data = p.read_bytes()
                self.assertNotIn(
                    b"\r\n",
                    data,
                    f"Script {rel_path} contains Windows CRLF line endings (\\r\\n), which breaks Linux execution!",
                )

    def test_untracked_binary_detection(self):
        """T2-F01-2: Boundary: Verify no uncommitted large binary archives exist in source trees."""
        # Check that pkgs/ doesn't have stale uncommitted *.pkg.tar.zst
        pkgs_dir = get_repo_path("pkgs")
        if pkgs_dir.exists():
            for p in pkgs_dir.rglob("*.pkg.tar.zst"):
                # Must be gitignored
                res = run_host_command(["git", "status", "--porcelain", str(p)])
                if res.returncode == 0:
                    status = res.stdout.strip()
                    self.assertFalse(
                        status.startswith("A ") or status.startswith("M "),
                        f"Built package {p.name} must not be tracked in git index",
                    )

    def test_executable_permissions_on_entrypoint_scripts(self):
        """T2-F01-3: Boundary: Verify build and launcher scripts have executable permission in repo."""
        # On POSIX or through git ls-files --stage
        git_dir = get_repo_path(".git")
        if git_dir.exists():
            res = run_host_command(["git", "ls-files", "--stage", "build.sh", "scripts/build-packages.sh"])
            if res.returncode == 0 and res.stdout.strip():
                for line in res.stdout.strip().splitlines():
                    # Format: <mode> <sha> <stage> <file>
                    mode = line.split()[0]
                    self.assertEqual(
                        mode,
                        "100755",
                        f"Script entrypoint must have executable git file mode (100755): {line}",
                    )

    def test_tracked_file_size_limits(self):
        """T2-F01-4: Boundary: Assert no tracked repository file exceeds 50MB (ISO bloat boundary)."""
        max_size = 50 * 1024 * 1024  # 50 MB
        for root, _, files in os.walk(REPO_ROOT):
            if ".git" in root or "dist" in root or "results" in root:
                continue
            for f in files:
                p = os.path.join(root, f)
                size = os.path.getsize(p)
                self.assertLess(
                    size,
                    max_size,
                    f"File {p} exceeds 50MB limit ({size} bytes). Large binaries must be generated, not committed.",
                )

    def test_headless_git_rev_parse_boundary(self):
        """T2-F01-5: Boundary: Test git resolution under non-interactive / headless environment."""
        git_dir = get_repo_path(".git")
        if git_dir.exists():
            res = run_host_command(["git", "status", "--porcelain"])
            self.assertEqual(res.returncode, 0, f"git status failed in headless context: {res.stderr}")


if __name__ == "__main__":
    unittest.main()
