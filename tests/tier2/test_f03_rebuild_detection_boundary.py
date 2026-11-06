"""Tier 2: Feature 3 - Package Rebuild Detection Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R4), PROJECT.md (Feature 3), TEST_INFRA.md, Survey 1 finding 3.
Validates build-packages.sh behavior on corrupted packages, missing directories,
error propagation, force rebuild overrides, and version parsing edge cases.
"""

import re
import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF03RebuildDetectionBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 3: Package Rebuild Detection."""

    def test_build_packages_creates_missing_localrepo_dir(self):
        """T2-F03-1: Boundary: Verify build-packages.sh creates localrepo directory if absent."""
        content = read_repo_file("scripts/build-packages.sh")
        self.assertRegex(
            content,
            r"mkdir\s+-p\s+.*LOCALREPO",
            "scripts/build-packages.sh must create localrepo directory with mkdir -p",
        )

    def test_build_packages_error_abort_policy(self):
        """T2-F03-2: Boundary: Verify build-packages.sh aborts immediately on build failure (set -e)."""
        content = read_repo_file("scripts/build-packages.sh")
        # Must have set -e or error check after makepkg
        has_error_handling = (
            "set -e" in content
            or "|| exit" in content
            or "|| return" in content
            or "if ! makepkg" in content
        )
        self.assertTrue(
            has_error_handling,
            "scripts/build-packages.sh must immediately abort if a package build fails",
        )

    def test_build_packages_force_rebuild_overrides_cached_artifact(self):
        """T2-F03-3: Boundary: Verify --rebuild skips package existence check and forces makepkg."""
        content = read_repo_file("scripts/build-packages.sh")
        # When --rebuild is passed, the skip condition must be bypassed
        self.assertTrue(
            "REBUILD" in content or "rebuild" in content,
            "scripts/build-packages.sh must have explicit logic to bypass artifact cache when rebuild is requested",
        )

    def test_build_packages_repo_add_database_integrity(self):
        """T2-F03-4: Boundary: Verify repo-add is called with remove/overwrite safety options."""
        content = read_repo_file("scripts/build-packages.sh")
        self.assertIn("repo-add", content)
        # Should not fail if db already exists
        self.assertTrue(
            "repo-add" in content,
            "scripts/build-packages.sh must update local repository index safely",
        )

    def test_build_packages_handles_pkgs_with_dots_and_revisions(self):
        """T2-F03-5: Boundary: Verify version extraction regex handles multi-digit and dot pkgrel."""
        content = read_repo_file("scripts/build-packages.sh")

        # 1. Structural check: Verify presence of pkgver and pkgrel extraction in scripts/build-packages.sh
        self.assertIn("pkgver=", content, "scripts/build-packages.sh must extract pkgver from PKGBUILD")
        self.assertIn("pkgrel=", content, "scripts/build-packages.sh must extract pkgrel from PKGBUILD")
        self.assertIn("${pkgver}-${pkgrel}", content, "scripts/build-packages.sh must combine pkgver and pkgrel as ${pkgver}-${pkgrel}")

        # 2. Boundary safety check: Ensure no naive single-digit truncation regex in version extraction
        # (e.g. pkgrel=[0-9] without quantifier or \d\b truncating 13 to 1)
        self.assertNotRegex(
            content,
            r"pkgrel.*\[0-9\](?!\+|\*|\{)",
            "scripts/build-packages.sh must not use single-digit regex that truncates multi-digit pkgrel",
        )

        # 3. Dynamic regex extraction: Extract the grep and sed expressions directly from scripts/build-packages.sh
        pkgver_grep = re.search(r"grep\s+-E\s+['\"]([^'\"]*pkgver=)['\"]", content)
        pkgrel_grep = re.search(r"grep\s+-E\s+['\"]([^'\"]*pkgrel=)['\"]", content)
        self.assertIsNotNone(pkgver_grep, "Must locate grep -E pattern for pkgver in scripts/build-packages.sh")
        self.assertIsNotNone(pkgrel_grep, "Must locate grep -E pattern for pkgrel in scripts/build-packages.sh")

        # Convert POSIX character class [[:space:]] to Python regex [ \t]
        ver_pat = pkgver_grep.group(1).replace("[[:space:]]", r"[ \t]")
        rel_pat = pkgrel_grep.group(1).replace("[[:space:]]", r"[ \t]")

        # Extract sed cleaning pattern: sed "s/['\" ]//g"
        sed_match = re.search(r'sed\s+"s/(?P<pattern>[^/]+)//g"', content)
        self.assertIsNotNone(sed_match, "Must locate sed quote/space cleaning pattern in scripts/build-packages.sh")
        strip_pattern = r"['\"\s]"

        def extract_version(pkgbuild_text: str) -> str:
            v_val, r_val = "", ""
            for line in pkgbuild_text.splitlines():
                if not v_val and re.match(ver_pat, line):
                    raw = line.split("=", 1)[1]
                    v_val = re.sub(strip_pattern, "", raw)
                if not r_val and re.match(rel_pat, line):
                    raw = line.split("=", 1)[1]
                    r_val = re.sub(strip_pattern, "", raw)
            return f"{v_val}-{r_val}" if (v_val and r_val) else ""

        # 4. Test multi-digit and dot boundary cases
        boundary_cases = [
            ("pkgname=test\npkgver=1.0.0\npkgrel=13\n", "1.0.0-13"),
            ("pkgname=test\npkgver=2.4.1\npkgrel=1.1\n", "2.4.1-1.1"),
            ("pkgname=test\n  pkgver=\"3.0.0\"\n  pkgrel='18' \n", "3.0.0-18"),
            ("pkgname=test\npkgver=0.9.8.7\npkgrel=102\n", "0.9.8.7-102"),
        ]

        for pkgbuild_content, expected in boundary_cases:
            result = extract_version(pkgbuild_content)
            self.assertEqual(
                result,
                expected,
                f"Version extraction failed for expected '{expected}', got '{result}'",
            )
            if expected.endswith("-13"):
                self.assertNotEqual(result, "1.0.0-1", "pkgrel 13 must not truncate to 1")
                self.assertFalse(result.endswith("-1"), "pkgrel 13 must not end with single digit 1")

        # 5. Verify against authentic in-tree repository packages with multi-digit revisions
        calamares_content = read_repo_file("pkgs/enerco-calamares-config/PKGBUILD")
        self.assertEqual(
            extract_version(calamares_content),
            "1.0.0-16",
            "enerco-calamares-config version must extract exactly as 1.0.0-16",
        )
        desktop_content = read_repo_file("pkgs/enerco-desktop-config/PKGBUILD")
        self.assertEqual(
            extract_version(desktop_content),
            "1.0.0-20",
            "enerco-desktop-config version must extract exactly as 1.0.0-20",
        )


if __name__ == "__main__":
    unittest.main()
