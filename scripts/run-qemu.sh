#!/usr/bin/env bash
# ==============================================================================
# EnercoOS Rapid QEMU Verification Runner
# Boots the latest generated ISO inside QEMU with UEFI (OVMF)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DIST_DIR="${PROJECT_ROOT}/dist"

# Find latest ISO
ISO_PATH=$(ls -t "${DIST_DIR}"/enercoos-*.iso 2>/dev/null | head -n 1 || true)
if [[ -n "${1:-}" ]]; then
    ISO_PATH="$1"
fi

if [[ -z "${ISO_PATH}" || ! -f "${ISO_PATH}" ]]; then
    echo "[ERROR] No ISO found in ${DIST_DIR}."
    echo "Usage: $0 [path/to/enercoos-x86_64.iso]"
    exit 1
fi

echo "=== Booting EnercoOS in QEMU ==="
echo "Target ISO: ${ISO_PATH}"

# Detect OVMF firmware path on Arch Linux
OVMF_CODE=""
for path in \
    "/usr/share/edk2/x64/OVMF_CODE.4m.fd" \
    "/usr/share/edk2/x64/OVMF_CODE.secboot.4m.fd" \
    "/usr/share/edk2-ovmf/x64/OVMF_CODE.fd" \
    "/usr/share/OVMF/OVMF_CODE.fd" \
    "/usr/share/ovmf/x64/OVMF_CODE.fd"; do
    if [[ -f "${path}" ]]; then
        OVMF_CODE="${path}"
        break
    fi
done

KVM_FLAG=""
if [[ -e /dev/kvm ]] && [[ -r /dev/kvm ]] && [[ -w /dev/kvm ]]; then
    KVM_FLAG="-enable-kvm"
    echo "[INFO] Hardware acceleration (/dev/kvm) enabled."
else
    echo "[WARN] /dev/kvm not accessible; running in emulation mode."
fi

QEMU_ARGS=(
    -m 4096
    -smp 4
    -cdrom "${ISO_PATH}"
    -boot d
    -vga std
    -display gtk
    -net nic,model=virtio
    -net user
)

if [[ -n "${OVMF_CODE}" ]]; then
    QEMU_ARGS+=(-drive "if=pflash,format=raw,readonly=on,file=${OVMF_CODE}")
    echo "[INFO] Using UEFI firmware: ${OVMF_CODE}"
fi

if [[ -n "${KVM_FLAG}" ]]; then
    QEMU_ARGS+=("${KVM_FLAG}")
fi

qemu-system-x86_64 "${QEMU_ARGS[@]}"

