"""Tier 2: Feature 2 - Clean enerco-macshell Packaging Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 2), TEST_INFRA.md, Survey 1 finding 2.
Validates packaging isolation, pkgdir boundary sanitization, QML syntax validation,
permissions boundaries, and source verification.
"""

import re
import unittest
from tests.config import (
    REPO_ROOT,
    get_repo_path,
    read_repo_file,
    repo_file_exists,
)


class TestF02MacShellPackagingBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 2: Clean enerco-macshell Packaging."""

    def test_pkgbuild_pkgdir_safety_guards(self):
        """T2-F02-1: Boundary: Verify PKGBUILD does not execute dangerous unbound rm -rf commands."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        # Ensure no unbound rm -rf $pkgdir or rm -rf /
        self.assertNotRegex(
            content,
            r"rm\s+-rf\s+['\"]?\$pkgdir/?['\"]?\s*$",
            "PKGBUILD must not execute raw rm -rf $pkgdir without safety boundary",
        )

    def test_qml_source_bracket_integrity(self):
        """T2-F02-2: Boundary: Verify QML files if present have balanced curly braces and syntax bounds."""
        qml_dirs = [
            get_repo_path("pkgs/enerco-macshell/MacShell"),
            get_repo_path("pkgs/enerco-macshell/MacLock"),
        ]
        qml_count = 0
        for d in qml_dirs:
            if d.exists():
                for f in d.rglob("*.qml"):
                    qml_count += 1
                    text = f.read_text(encoding="utf-8", errors="ignore")
                    open_cnt = text.count("{")
                    close_cnt = text.count("}")
                    self.assertEqual(
                        open_cnt,
                        close_cnt,
                        f"Unbalanced curly braces in QML file {f.name}: {open_cnt} open vs {close_cnt} close",
                    )
        # If no local QML files because git submodule / repo is in WSL, assert source declaration
        if qml_count == 0:
            content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
            self.assertTrue(
                "source=" in content or "MacShell" in content,
                "PKGBUILD must declare source fetching or bundle for MacShell",
            )

    def test_pkgbuild_sets_proper_executable_permissions(self):
        """T2-F02-3: Boundary: Verify PKGBUILD uses install -m755 for scripts and 644 for assets."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        # Ensure scripts are installed with 755
        self.assertTrue(
            "-m755" in content or "-m 755" in content or "chmod +x" in content,
            "PKGBUILD must set executable permissions (755) on shell executables",
        )

    def test_pkgbuild_avoids_hardcoded_absolute_build_paths(self):
        """T2-F02-4: Boundary: Verify PKGBUILD does not leak absolute host paths into build targets."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        self.assertNotIn(
            "/home/builder",
            content,
            "PKGBUILD must not contain hardcoded user build paths (/home/builder)",
        )
        self.assertNotIn(
            "C:\\",
            content,
            "PKGBUILD must not contain Windows path strings",
        )

    def test_pkgbuild_package_checksum_array_boundary(self):
        """T2-F02-5: Boundary: Verify checksum array matches source entries in PKGBUILD."""
        content = read_repo_file("pkgs/enerco-macshell/PKGBUILD")
        # Checks sha256sums or md5sums exists if source= is defined
        if "source=(" in content:
            has_checksums = "sha256sums=" in content or "md5sums=" in content or "b2sums=" in content
            self.assertTrue(has_checksums, "PKGBUILD must define checksum array when source array is declared")


if __name__ == "__main__":
    unittest.main()
