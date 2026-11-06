"""Tier 1: Feature 3 - Package Rebuild Detection Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 3), TEST_INFRA.md, Survey 1 finding 3.
Validates scripts/build-packages.sh version comparison, --rebuild argument handling,
database generation, and package build sequencing.
"""

import re
import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF03RebuildDetection(unittest.TestCase):
    """Tier 1 test suite for Feature 3: Package Rebuild Detection."""

    def test_build_packages_script_exists_and_syntax(self):
        """T1-F03-1: Verify scripts/build-packages.sh exists and has valid bash shebang."""
        self.assertTrue(repo_file_exists("scripts/build-packages.sh"), "scripts/build-packages.sh must exist")
        content = read_repo_file("scripts/build-packages.sh")
        self.assertTrue(
            content.startswith("#!/bin/bash") or content.startswith("#!/usr/bin/env bash"),
            "scripts/build-packages.sh must start with a valid bash shebang",
        )

    def test_build_packages_supports_rebuild_flag(self):
        """T1-F03-2: Verify build-packages.sh accepts --rebuild command-line option."""
        content = read_repo_file("scripts/build-packages.sh")
        # Must parse --rebuild flag
        self.assertTrue(
            "--rebuild" in content or "REBUILD" in content,
            "scripts/build-packages.sh must support --rebuild flag to force package rebuilds",
        )

    def test_build_packages_exact_version_detection(self):
        """T1-F03-3: Verify build-packages.sh checks exact pkgver/pkgrel rather than naive prefix wildcard."""
        content = read_repo_file("scripts/build-packages.sh")
        # The buggy pattern: compgen -G "${LOCALREPO_DIR}/${pkg}-*.pkg.tar.zst"
        # skips new versions because of the wildcard suffix.
        # It must check exact version or inspect PKGBUILD version variables.
        has_exact_check = (
            "pkgver" in content
            and "pkgrel" in content
            and not ('compgen -G "${LOCALREPO_DIR}/${pkg}-*.pkg.tar.zst"' in content)
        )
        self.assertTrue(
            has_exact_check,
            "scripts/build-packages.sh must use exact version matching (${pkg}-${pkgver}-${pkgrel}) or respect REBUILD flag",
        )

    def test_build_packages_updates_localrepo_database(self):
        """T1-F03-4: Verify build-packages.sh invokes repo-add on enerco-local database."""
        content = read_repo_file("scripts/build-packages.sh")
        self.assertIn("repo-add", content, "scripts/build-packages.sh must execute repo-add")
        self.assertIn(
            "enerco-local.db.tar.gz",
            content,
            "scripts/build-packages.sh must register packages to enerco-local.db.tar.gz",
        )

    def test_package_build_ordering(self):
        """T1-F03-5: Verify packages array builds dependencies before dependents."""
        content = read_repo_file("scripts/build-packages.sh")
        # Find packages array or list
        branding_idx = content.find("enerco-branding")
        desktop_idx = content.find("enerco-desktop-config")
        calamares_idx = content.find("calamares")
        calamares_cfg_idx = content.find("enerco-calamares-config")

        self.assertTrue(branding_idx != -1, "enerco-branding must be in package list")
        self.assertTrue(desktop_idx != -1, "enerco-desktop-config must be in package list")
        self.assertTrue(calamares_idx != -1, "calamares must be in package list")
        self.assertTrue(calamares_cfg_idx != -1, "enerco-calamares-config must be in package list")

        self.assertLess(
            branding_idx,
            desktop_idx,
            "enerco-branding must be built before enerco-desktop-config",
        )
        self.assertLess(
            calamares_idx,
            calamares_cfg_idx,
            "calamares binary must be built before enerco-calamares-config",
        )


if __name__ == "__main__":
    unittest.main()
