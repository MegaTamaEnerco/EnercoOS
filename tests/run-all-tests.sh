#!/usr/bin/env bash
# ==============================================================================
# EnercoOS E2E Test Suite Shell Runner
# Executes python tests/run_e2e_tests.py inside WSL / Linux environment
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

# Find Python 3
PYTHON_BIN="python3"
if ! command -v python3 &>/dev/null; then
    if command -v python &>/dev/null; then
        PYTHON_BIN="python"
    else
        echo "[ERROR] python3 or python not found in PATH" >&2
        exit 1
    fi
fi

echo "[INFO] Running EnercoOS E2E Test Suite using ${PYTHON_BIN}..."
"${PYTHON_BIN}" "${SCRIPT_DIR}/run_e2e_tests.py" "$@"
