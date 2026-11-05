#!/usr/bin/env bash
# ==============================================================================
# EnercoOS Build VM Synchronizer
# Syncs code changes from Windows/WSL2 host to the dedicated Arch Build VM
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

VM_HOST="${1:-archvm.local}"
VM_USER="${2:-arch}"
VM_DEST="${3:-~/enercoos}"

echo "=== Syncing EnercoOS to Arch Build VM ==="
echo "Target: ${VM_USER}@${VM_HOST}:${VM_DEST}"

rsync -avz --delete \
    --exclude='.git' \
    --exclude='dist/' \
    --exclude='work/' \
    --exclude='localrepo/*.pkg.tar.*' \
    --exclude='pkgs/*/src/' \
    --exclude='pkgs/*/pkg/' \
    "${PROJECT_ROOT}/" "${VM_USER}@${VM_HOST}:${VM_DEST}/"

echo "=== Sync Complete! ==="
echo "To trigger the build on the VM, run:"
echo "  ssh ${VM_USER}@${VM_HOST} 'cd ${VM_DEST} && sudo ./build.sh'"

