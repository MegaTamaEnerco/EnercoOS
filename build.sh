#!/usr/bin/env bash
# ==============================================================================
# EnercoOS ISO Build Entrypoint
# Automates package building, local repository indexing, and mkarchiso execution
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/enerco-build-work"
OUT_DIR="${SCRIPT_DIR}/dist"
LOCALREPO_DIR="${SCRIPT_DIR}/localrepo"
PACMAN_CONF_TEMPLATE="${SCRIPT_DIR}/pacman.conf"
BUILD_PACMAN_CONF="${WORK_DIR}/pacman-build.conf"

echo "=========================================================="
echo "          PT MEGA TAMA ENERCO - ENERCOOS BUILDER          "
echo "=========================================================="

if [[ $EUID -ne 0 ]]; then
   echo "[ERROR] build.sh must be executed with root privileges."
   echo "Run: sudo ./build.sh"
   exit 1
fi

# Step 1: Verify and build local packages if needed
if [[ ! -f "${LOCALREPO_DIR}/enerco-local.db.tar.gz" ]] || [[ "${1:-}" == "--rebuild-pkgs" ]]; then
    echo "[STEP 1/4] Building in-tree standard Arch packages..."
    # Drop sudo privilege temporarily if needed or run directly
    if [[ -n "${SUDO_USER:-}" ]]; then
        sudo -u "${SUDO_USER}" bash "${SCRIPT_DIR}/scripts/build-packages.sh"
    else
        bash "${SCRIPT_DIR}/scripts/build-packages.sh"
    fi
else
    echo "[STEP 1/4] In-tree package repository found at ${LOCALREPO_DIR}."
fi

# Step 2: Clean previous build workspace
echo "[STEP 2/4] Initializing clean workspace at ${WORK_DIR}..."
rm -rf "${WORK_DIR}"
mkdir -p "${WORK_DIR}" "${OUT_DIR}"

# Step 3: Configure pacman.conf with absolute local repository path
echo "[STEP 3/4] Preparing pacman build configuration..."
sed "s|@ENERCO_LOCAL_REPO_PATH@|${LOCALREPO_DIR}|g" "${PACMAN_CONF_TEMPLATE}" > "${BUILD_PACMAN_CONF}"

# Step 4: Run mkarchiso
echo "[STEP 4/4] Executing mkarchiso..."
mkarchiso -v \
    -C "${BUILD_PACMAN_CONF}" \
    -w "${WORK_DIR}" \
    -o "${OUT_DIR}" \
    "${SCRIPT_DIR}"

# If running inside WSL, mirror output ISO to Windows dist directory safely
if [[ -d "/mnt/c/Users/CorSec/Documents/personal/EnercoOS" ]] && [[ "${SCRIPT_DIR}" != "/mnt/c/"* ]]; then
    echo "[STEP 5/5] Mirroring output ISO to Windows host workspace..."
    mkdir -p "/mnt/c/Users/CorSec/Documents/personal/EnercoOS/dist"
    for iso_file in "${OUT_DIR}"/*.iso; do
        if [[ -f "${iso_file}" ]]; then
            iso_name="$(basename "${iso_file}")"
            dest_file="/mnt/c/Users/CorSec/Documents/personal/EnercoOS/dist/${iso_name}"
            echo "Copying ${iso_name} via atomic staging..."
            cp -f "${iso_file}" "${dest_file}.tmp"
            mv -f "${dest_file}.tmp" "${dest_file}"
            echo "Mirrored: ${dest_file} ($(stat -c%s "${dest_file}") bytes)"
        fi
    done
fi

echo "=========================================================="
echo " [SUCCESS] EnercoOS ISO build completed successfully!"
echo " Generated images:"
ls -lh "${OUT_DIR}"/*.iso
echo "=========================================================="

