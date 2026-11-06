#!/usr/bin/env python3
"""EnercoOS E2E Test Suite CLI Entrypoint.

Usage:
    python tests/run_e2e_tests.py
    python tests/run_e2e_tests.py --tier 1
    python tests/run_e2e_tests.py --milestone M1
    python tests/run_e2e_tests.py --feature F01
    python tests/run_e2e_tests.py --allow-defects
"""

import sys
from pathlib import Path

# Add REPO_ROOT to path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.runner import main

if __name__ == "__main__":
    main()
