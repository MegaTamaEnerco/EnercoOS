"""Tier 1: Feature 2 - Clean enerco-macshell Packaging Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 2), TEST_INFRA.md, Survey 1 finding 2.
Validates .gitignore patterns, PKGBUILD syntax, dependency declarations, reproducible
source handling, and target directory mappings.
"""

import re
import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF02MacShellPackaging(unittest.TestCase):
    """Tier 1 test suite for Feature 2: Clean enerco-macshell Packaging."""

    def test_gitignore_does_not_blanket_ignore_macshell_sources(self):
        """T1-F02-1: Verify .gitignore does not contain overly broad 'pkgs/*/*/' pattern."""
        self.assertTrue(repo_file_exists(".gitignore"), ".gitignore must exist")
        content = read_repo_file(".gitignore")
        lines = [line.strip() for line in content.splitlines()]
        # Finding: 'pkgs/*/*/' ignores MacShell and MacLock subdirectories in repo
        self.assertNotIn(
            "pkgs/*/*/",
            lines,
            "Overly broad .gitignore rule 'pkgs/*/*/' must be removed or scoped so source files are tracked",
        )

    def test_macshell_pkgbuild_exists_and_has_valid_metadata(self):
        """T1-F02-2: Verify pkgs/enerco-macshell/PKGBUILD has standard packaging variables."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-macshell/PKGBUILD"),
            "pkgs/enerco-macshell/PKGBUILD must exist",
        )
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        self.assertRegex(content, r"pkgname\s*=\s*['\"]?enerco-macshell['\"]?", "pkgname must be enerco-macshell")
        self.assertRegex(content, r"pkgver\s*=\s*[0-9.]+", "pkgver must be defined")
        self.assertRegex(content, r"pkgrel\s*=\s*[0-9]+", "pkgrel must be defined")
        self.assertIn("package()", content, "PKGBUILD must contain package() function")

    def test_macshell_pkgbuild_declares_core_dependencies(self):
        """T1-F02-3: Verify PKGBUILD declares quickshell or qt6 runtime dependencies."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        self.assertIn("depends=", content, "PKGBUILD must define depends array")
        # Must require quickshell or qt6-declarative
        has_qs = "quickshell" in content
        has_qt6 = "qt6" in content
        self.assertTrue(
            has_qs or has_qt6,
            "enerco-macshell dependencies must include quickshell or qt6 components",
        )

    def test_macshell_pkgbuild_installs_supervisor_and_configs(self):
        """T1-F02-4: Verify PKGBUILD packages macshell-start script and Quickshell components."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        # Must install macshell-start wrapper
        self.assertTrue(
            "macshell-start" in content or "bin" in content,
            "PKGBUILD must install shell supervisor executable",
        )
        # Must stage MacShell QML configurations
        self.assertTrue(
            "MacShell" in content or "quickshell" in content,
            "PKGBUILD must stage MacShell configuration files",
        )

    def test_macshell_pkgbuild_reproducible_source_handling(self):
        """T1-F02-5: Verify PKGBUILD does not use broken anti-pattern referencing parent dir outside srcdir."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        # Anti-pattern: cp -dr ${srcdir}/../MacShell ... which fails in clean chroots
        self.assertNotRegex(
            content,
            r"\$\{srcdir\}/\.\./MacShell",
            "PKGBUILD must not use broken relative parent reference '${srcdir}/../MacShell'",
        )


if __name__ == "__main__":
    unittest.main()
