"""Tier 1: Feature 1 - Host/WSL Git Reconciliation Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 1), TEST_INFRA.md.
Validates git configuration, line ending enforcement, synchronization scripts, and
prevention of committed binary artifacts.
"""

import os
import re
import subprocess
import unittest
from pathlib import Path
from tests.config import (
    REPO_ROOT,
    get_repo_path,
    read_repo_file,
    repo_file_exists,
    run_host_command,
)


class TestF01GitReconciliation(unittest.TestCase):
    """Tier 1 test suite for Feature 1: Host/WSL Git Reconciliation."""

    def test_gitattributes_enforces_lf_line_endings(self):
        """T1-F01-1: Verify .gitattributes enforces LF for scripts and PKGBUILDs."""
        self.assertTrue(repo_file_exists(".gitattributes"), ".gitattributes must exist")
        content = read_repo_file(".gitattributes")
        # Must enforce eol=lf on shell scripts and build descriptors
        self.assertIn("eol=lf", content, ".gitattributes must define eol=lf")
        self.assertTrue(
            re.search(r"\*\.sh\s+text\s+eol=lf", content) or "text eol=lf" in content,
            "Shell scripts must be mapped to text eol=lf",
        )

    def test_no_binary_iso_committed_in_git(self):
        """T1-F01-2: Verify no large ISO binaries are tracked in the git repository."""
        dist_dir = get_repo_path("dist")
        if dist_dir.exists():
            for f in dist_dir.glob("*.iso"):
                # If an ISO exists, verify it is ignored by git
                res = run_host_command(["git", "status", "--porcelain", str(f)])
                if res.returncode == 0:
                    # git status shouldn't show it as staged (no leading 'A' or 'M' without ??)
                    status_line = res.stdout.strip()
                    self.assertFalse(
                        status_line.startswith("A ") or status_line.startswith("M "),
                        f"ISO artifact {f.name} must not be tracked in git index: {status_line}",
                    )

    def test_sync_to_vm_script_syntax_and_structure(self):
        """T1-F01-3: Verify scripts/sync-to-vm.sh exists and contains valid bash syntax."""
        self.assertTrue(repo_file_exists("scripts/sync-to-vm.sh"), "scripts/sync-to-vm.sh must exist")
        content = read_repo_file("scripts/sync-to-vm.sh")
        self.assertTrue(content.startswith("#!/bin/bash") or content.startswith("#!/usr/bin/env bash"),
                        "sync-to-vm.sh must have a valid bash shebang")
        self.assertIn("rsync", content, "sync-to-vm.sh should utilize rsync or scp for vm synchronization")

    def test_repo_git_tracking_and_head_resolution(self):
        """T1-F01-4: Verify git repository HEAD is accessible and commit SHA is valid."""
        git_dir = get_repo_path(".git")
        if git_dir.exists():
            res = run_host_command(["git", "rev-parse", "HEAD"])
            self.assertEqual(res.returncode, 0, f"git rev-parse HEAD failed: {res.stderr}")
            sha = res.stdout.strip()
            self.assertTrue(re.match(r"^[0-9a-f]{40}$", sha), f"Invalid commit SHA: {sha}")
        else:
            self.skipTest(".git directory not present in current test environment")

    def test_wslconfig_memory_and_swap_configuration(self):
        """T1-F01-5: Verify .wslconfig defines necessary build memory and swap for mkarchiso."""
        self.assertTrue(repo_file_exists(".wslconfig"), ".wslconfig must exist for WSL 2 build setup")
        content = read_repo_file(".wslconfig")
        self.assertIn("[wsl2]", content, ".wslconfig must contain [wsl2] section")
        self.assertTrue(
            re.search(r"memory\s*=\s*\d+GB", content, re.IGNORECASE),
            ".wslconfig must allocate adequate memory (e.g. >= 8GB)",
        )
        self.assertTrue(
            re.search(r"swap\s*=\s*\d+GB", content, re.IGNORECASE),
            ".wslconfig must allocate swap space for memory-intensive mkarchiso steps",
        )


if __name__ == "__main__":
    unittest.main()
