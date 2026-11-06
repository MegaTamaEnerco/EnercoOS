"""Tier 1: Feature 15 - Enterprise ERP Integration & Productivity Stack Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R3), PROJECT.md (Feature 15), TEST_INFRA.md, Survey 3 finding 5.
Validates mterp.desktop freedesktop specification compliance, corporate URLs, shell aliases,
and office/document productivity package inclusion.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF15EnterpriseERP(unittest.TestCase):
    """Tier 1 test suite for Feature 15: Enterprise ERP Integration & Productivity Stack."""

    def test_mterp_desktop_no_invalid_h_token(self):
        """T1-F15-1: Verify mterp.desktop does NOT contain invalid Freedesktop token %h."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-enterprise-tools/mterp.desktop"),
            "pkgs/enerco-enterprise-tools/mterp.desktop must exist",
        )
        content = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        # %h creates a literal directory named '%h' in current working directory
        self.assertNotIn(
            "%h",
            content,
            "mterp.desktop must not use invalid field code '%h'; use wrapper script or standard Freedesktop expansion",
        )

    def test_mterp_desktop_corporate_url(self):
        """T1-F15-2: Verify mterp.desktop points to https://mterp.megatama-enerco.com."""
        content = read_repo_file("pkgs/enerco-enterprise-tools/mterp.desktop")
        self.assertIn(
            "https://mterp.megatama-enerco.com",
            content,
            "mterp.desktop must target corporate ERP endpoint https://mterp.megatama-enerco.com",
        )

    def test_zshrc_mterp_alias_points_to_correct_url(self):
        """T1-F15-3: Verify shell alias in .zshrc targets https://mterp.megatama-enerco.com, not .internal."""
        self.assertTrue(repo_file_exists("airootfs/home/enerco/.zshrc"), "airootfs/home/enerco/.zshrc must exist")
        content = read_repo_file("airootfs/home/enerco/.zshrc")
        self.assertNotIn(
            "mterp.internal",
            content,
            ".zshrc alias must not point to fictitious mterp.internal domain",
        )
        self.assertIn(
            "mterp.megatama-enerco.com",
            content,
            ".zshrc alias must point to https://mterp.megatama-enerco.com",
        )

    def test_packages_includes_office_productivity(self):
        """T1-F15-4: Verify packages.x86_64 includes LibreOffice for enterprise document authoring."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        has_office = any(p in packages for p in ["libreoffice-fresh", "libreoffice-still", "libreoffice"])
        self.assertTrue(
            has_office,
            "packages.x86_64 must include LibreOffice (fresh or still) for office productivity",
        )

    def test_packages_includes_pdf_and_document_viewer(self):
        """T1-F15-5: Verify packages.x86_64 includes Evince PDF viewer."""
        content = read_repo_file("packages.x86_64")
        packages = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        self.assertIn(
            "evince",
            packages,
            "packages.x86_64 must include evince for corporate PDF and document inspection",
        )


if __name__ == "__main__":
    unittest.main()
