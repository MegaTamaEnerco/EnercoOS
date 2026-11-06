"""EnercoOS E2E Test Suite Harness and Runner.

Executes Tier 1 (Feature Coverage), Tier 2 (Boundary & Corner Cases),
Tier 3 (Cross-Feature Interactions), and Tier 4 (Real-World Application Scenarios).
Generates TAP v13, JUnit XML, and structured JSON test reports.
"""

import argparse
import json
import os
import re
import sys
import time
import unittest
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# Ensure tests package is importable
TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Milestone mappings for progressive testability
FEATURE_MILESTONES = {
    "F01": "M1",
    "F02": "M1",
    "F03": "M1",
    "F04": "M1",
    "F05": "M2",
    "F06": "M2",
    "F07": "M2",
    "F08": "M2",
    "F09": "M2",
    "F10": "M2",
    "F11": "M3",
    "F12": "M3",
    "F13": "M3",
    "F14": "M3",
    "F15": "M4",
    "F16": "M3",
}


@dataclass
class TestResultItem:
    """Individual test execution result record."""
    id: str
    name: str
    tier: str
    feature: Optional[str]
    milestone: Optional[str]
    status: str  # PASS, FAIL, ERROR, SKIP
    duration_ms: float
    message: str = ""
    traceback: str = ""


@dataclass
class SuiteSummary:
    """Aggregated test suite results summary."""
    total: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    duration_sec: float = 0.0
    items: List[TestResultItem] = field(default_factory=list)


class CustomTestResult(unittest.TestResult):
    """Custom TestResult collector capturing timings and details."""

    def __init__(self):
        super().__init__()
        self.results: List[TestResultItem] = []
        self._test_start_time = 0.0

    def startTest(self, test: unittest.TestCase):
        super().startTest(test)
        self._test_start_time = time.perf_counter()

    def _extract_metadata(self, test: unittest.TestCase):
        test_id = test.id()
        # Extract Tier
        tier = "unknown"
        if "tier1" in test_id:
            tier = "Tier 1"
        elif "tier2" in test_id:
            tier = "Tier 2"
        elif "tier3" in test_id:
            tier = "Tier 3"
        elif "tier4" in test_id:
            tier = "Tier 4"

        # Extract Feature & Milestone
        feature = None
        milestone = None
        m = re.search(r"f(\d{2})", test_id, re.IGNORECASE)
        if m:
            feature = f"F{int(m.group(1)):02d}"
            milestone = FEATURE_MILESTONES.get(feature)

        duration = (time.perf_counter() - self._test_start_time) * 1000.0
        return test_id, test._testMethodName, tier, feature, milestone, duration

    def addSuccess(self, test: unittest.TestCase):
        super().addSuccess(test)
        test_id, name, tier, feat, ms, dur = self._extract_metadata(test)
        self.results.append(TestResultItem(
            id=test_id,
            name=name,
            tier=tier,
            feature=feat,
            milestone=ms,
            status="PASS",
            duration_ms=dur,
        ))

    def addFailure(self, test: unittest.TestCase, err):
        super().addFailure(test, err)
        test_id, name, tier, feat, ms, dur = self._extract_metadata(test)
        msg = str(err[1])
        tb = self._exc_info_to_string(err, test)
        self.results.append(TestResultItem(
            id=test_id,
            name=name,
            tier=tier,
            feature=feat,
            milestone=ms,
            status="FAIL",
            duration_ms=dur,
            message=msg,
            traceback=tb,
        ))

    def addError(self, test: unittest.TestCase, err):
        super().addError(test, err)
        test_id, name, tier, feat, ms, dur = self._extract_metadata(test)
        msg = str(err[1])
        tb = self._exc_info_to_string(err, test)
        self.results.append(TestResultItem(
            id=test_id,
            name=name,
            tier=tier,
            feature=feat,
            milestone=ms,
            status="ERROR",
            duration_ms=dur,
            message=msg,
            traceback=tb,
        ))

    def addSkip(self, test: unittest.TestCase, reason: str):
        super().addSkip(test, reason)
        test_id, name, tier, feat, ms, dur = self._extract_metadata(test)
        self.results.append(TestResultItem(
            id=test_id,
            name=name,
            tier=tier,
            feature=feat,
            milestone=ms,
            status="SKIP",
            duration_ms=dur,
            message=reason,
        ))


class EnercoOSTestRunner:
    """E2E Test Runner orchestrating test loading, filtering, reporting, and execution."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (TESTS_DIR / "results")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_suite(
        self,
        tier: Optional[str] = None,
        milestone: Optional[str] = None,
        feature: Optional[str] = None,
        pattern_filter: Optional[str] = None,
    ) -> unittest.TestSuite:
        """Discover and filter test cases based on parameters."""
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()

        # Determine directories to scan
        tier_dirs = []
        if tier in [None, "all"]:
            tier_dirs = ["tier1", "tier2", "tier3", "tier4"]
        elif tier in ["1", "tier1"]:
            tier_dirs = ["tier1"]
        elif tier in ["2", "tier2"]:
            tier_dirs = ["tier2"]
        elif tier in ["3", "tier3"]:
            tier_dirs = ["tier3"]
        elif tier in ["4", "tier4"]:
            tier_dirs = ["tier4"]

        for td in tier_dirs:
            p = TESTS_DIR / td
            if p.exists():
                discovered = loader.discover(start_dir=str(p), pattern="test_*.py", top_level_dir=str(REPO_ROOT))
                suite.addTest(discovered)

        # Filter tests by feature, milestone, or pattern if requested
        if milestone or feature or pattern_filter:
            filtered_suite = unittest.TestSuite()
            for test in self._flatten_suite(suite):
                test_id = test.id()
                # Milestone filter
                if milestone:
                    feat_match = re.search(r"f(\d{2})", test_id, re.IGNORECASE)
                    if feat_match:
                        f_id = f"F{int(feat_match.group(1)):02d}"
                        if FEATURE_MILESTONES.get(f_id) != milestone.upper():
                            continue
                    else:
                        continue
                # Feature filter
                if feature:
                    f_upper = feature.upper()
                    if f_upper.startswith("F"):
                        f_num = f_upper[1:]
                    else:
                        f_num = f_upper
                    f_pattern = f"f{int(f_num):02d}"
                    if f_pattern not in test_id.lower():
                        continue
                # Substring pattern filter
                if pattern_filter:
                    if pattern_filter.lower() not in test_id.lower():
                        continue
                filtered_suite.addTest(test)
            return filtered_suite

        return suite

    def _flatten_suite(self, suite: unittest.TestSuite) -> List[unittest.TestCase]:
        """Flatten a nested TestSuite into a list of TestCase instances."""
        tests = []
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                tests.extend(self._flatten_suite(item))
            elif isinstance(item, unittest.TestCase):
                tests.append(item)
        return tests

    def run(
        self,
        tier: Optional[str] = None,
        milestone: Optional[str] = None,
        feature: Optional[str] = None,
        pattern_filter: Optional[str] = None,
        verbose: bool = True,
    ) -> SuiteSummary:
        """Run the test suite and return structured summary."""
        suite = self.load_suite(tier=tier, milestone=milestone, feature=feature, pattern_filter=pattern_filter)
        flat_tests = self._flatten_suite(suite)
        total_tests = len(flat_tests)

        print(f"\n=======================================================")
        print(f" EnercoOS E2E Test Suite Runner")
        print(f" Loaded {total_tests} test cases (Filter: tier={tier}, milestone={milestone}, feature={feature})")
        print(f"=======================================================\n")

        result_collector = CustomTestResult()
        start_time = time.perf_counter()

        # Run tests
        for i, test in enumerate(flat_tests, 1):
            test_id = test.id()
            short_name = test_id.split(".")[-1]
            if verbose:
                sys.stdout.write(f"[{i:03d}/{total_tests:03d}] {short_name:<48} ... ")
                sys.stdout.flush()

            test.run(result_collector)

            latest = result_collector.results[-1]
            if verbose:
                status_color = latest.status
                if latest.status == "PASS":
                    print(f"\033[32mPASS\033[0m ({latest.duration_ms:.1f}ms)")
                elif latest.status == "FAIL":
                    print(f"\033[31mFAIL\033[0m ({latest.duration_ms:.1f}ms)")
                elif latest.status == "ERROR":
                    print(f"\033[35mERROR\033[0m ({latest.duration_ms:.1f}ms)")
                elif latest.status == "SKIP":
                    print(f"\033[33mSKIP\033[0m ({latest.duration_ms:.1f}ms)")

        total_duration = time.perf_counter() - start_time

        summary = SuiteSummary(
            total=total_tests,
            passed=len(result_collector.results) - len(result_collector.failures) - len(result_collector.errors) - len(result_collector.skipped),
            failed=len(result_collector.failures),
            errors=len(result_collector.errors),
            skipped=len(result_collector.skipped),
            duration_sec=total_duration,
            items=result_collector.results,
        )

        self._print_summary(summary)
        self._write_tap_report(summary)
        self._write_junit_xml(summary)
        self._write_json_report(summary)

        return summary

    def _print_summary(self, summary: SuiteSummary):
        """Print formatted execution summary."""
        print("\n" + "=" * 55)
        print(" TEST EXECUTION SUMMARY")
        print("=" * 55)
        print(f" Total Tests : {summary.total}")
        print(f" Passed      : \033[32m{summary.passed}\033[0m")
        print(f" Failed      : \033[31m{summary.failed}\033[0m")
        print(f" Errors      : \033[35m{summary.errors}\033[0m")
        print(f" Skipped     : \033[33m{summary.skipped}\033[0m")
        print(f" Elapsed Time: {summary.duration_sec:.2f}s")
        print("=" * 55)

        if summary.failed > 0 or summary.errors > 0:
            print("\n--- DEFECTS / FAILURES DETECTED ---")
            for item in summary.items:
                if item.status in ["FAIL", "ERROR"]:
                    print(f"\n[!] {item.id} ({item.status})")
                    first_line = item.message.strip().splitlines()[0] if item.message else "Assertion failed"
                    print(f"    Message: {first_line}")

    def _write_tap_report(self, summary: SuiteSummary):
        """Generate standard TAP (Test Anything Protocol) version 13 report."""
        tap_path = self.output_dir / "report.tap"
        lines = [
            "TAP version 13",
            f"1..{summary.total}",
        ]
        for i, item in enumerate(summary.items, 1):
            if item.status == "PASS":
                lines.append(f"ok {i} - {item.id} # time={item.duration_ms:.1f}ms")
            elif item.status == "SKIP":
                lines.append(f"ok {i} - {item.id} # SKIP {item.message}")
            else:
                lines.append(f"not ok {i} - {item.id} # time={item.duration_ms:.1f}ms")
                if item.message:
                    lines.append(f"  ---")
                    lines.append(f"  message: {item.message.splitlines()[0]}")
                    lines.append(f"  severity: fail")
                    lines.append(f"  ...")
        tap_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f" TAP report generated:   {tap_path}")

    def _write_junit_xml(self, summary: SuiteSummary):
        """Generate standard JUnit XML report for CI integration."""
        xml_path = self.output_dir / "junit.xml"
        testsuite = ET.Element(
            "testsuite",
            name="EnercoOS-E2E-Tests",
            tests=str(summary.total),
            failures=str(summary.failed),
            errors=str(summary.errors),
            skipped=str(summary.skipped),
            time=f"{summary.duration_sec:.3f}",
        )
        for item in summary.items:
            testcase = ET.SubElement(
                testsuite,
                "testcase",
                classname=item.id.rsplit(".", 1)[0],
                name=item.name,
                time=f"{item.duration_ms / 1000.0:.3f}",
            )
            if item.status == "FAIL":
                failure = ET.SubElement(testcase, "failure", message=item.message.splitlines()[0] if item.message else "Failed")
                failure.text = item.traceback
            elif item.status == "ERROR":
                err = ET.SubElement(testcase, "error", message=item.message.splitlines()[0] if item.message else "Error")
                err.text = item.traceback
            elif item.status == "SKIP":
                ET.SubElement(testcase, "skipped", message=item.message)

        tree = ET.ElementTree(testsuite)
        tree.write(str(xml_path), encoding="utf-8", xml_declaration=True)
        print(f" JUnit XML generated:    {xml_path}")

    def _write_json_report(self, summary: SuiteSummary):
        """Generate structured JSON report with test records and execution metadata."""
        json_path = self.output_dir / "report.json"
        data = {
            "summary": {
                "total": summary.total,
                "passed": summary.passed,
                "failed": summary.failed,
                "errors": summary.errors,
                "skipped": summary.skipped,
                "duration_sec": summary.duration_sec,
            },
            "environment": {
                "python": sys.version,
                "platform": sys.platform,
                "os": os.name,
            },
            "results": [asdict(item) for item in summary.items],
        }
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f" JSON report generated:  {json_path}")


def main():
    parser = argparse.ArgumentParser(description="EnercoOS E2E Test Suite Runner")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all", help="Test tier to execute")
    parser.add_argument("--milestone", choices=["M1", "M2", "M3", "M4", "all"], default=None, help="Filter by milestone")
    parser.add_argument("--feature", default=None, help="Filter by feature (e.g. F01, F02, F16)")
    parser.add_argument("--filter", default=None, help="Filter test names by substring")
    parser.add_argument("--output-dir", default=None, help="Directory to store reports")
    parser.add_argument("--allow-defects", action="store_true", help="Always exit 0 even if implementation bugs are found")
    args = parser.parse_args()

    milestone = None if args.milestone == "all" else args.milestone
    output_dir = Path(args.output_dir) if args.output_dir else None

    runner = EnercoOSTestRunner(output_dir=output_dir)
    summary = runner.run(
        tier=args.tier,
        milestone=milestone,
        feature=args.feature,
        pattern_filter=args.filter,
    )

    if not args.allow_defects and (summary.failed > 0 or summary.errors > 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
