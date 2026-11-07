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
PKGS_DIR="${SCRIPT_DIR}/pkgs"
PACMAN_CONF_TEMPLATE="${SCRIPT_DIR}/pacman.conf"
BUILD_PACMAN_CONF="${WORK_DIR}/pacman-build.conf"

# Trap handler for signal cleanup
cleanup_work_dir() {
    local exit_code=$?
    if [[ -d "${WORK_DIR:-}" ]]; then
        mount | grep "${WORK_DIR}" | awk '{print $3}' | sort -r | xargs -r umount -l 2>/dev/null || true
    fi
    exit ${exit_code}
}
trap cleanup_work_dir INT TERM EXIT

# Parse CLI options (support -h/--help without requiring root privileges)
REBUILD_PKGS=false
for arg in "$@"; do
    case "${arg}" in
        --rebuild-pkgs)
            REBUILD_PKGS=true
            ;;
        -h|--help)
            echo "Usage: sudo $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --rebuild-pkgs    Force recompilation of all in-tree packages before ISO build"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
    esac
done

echo "=========================================================="
echo "          PT MEGA TAMA ENERCO - ENERCOOS BUILDER          "
echo "=========================================================="

if [[ $EUID -ne 0 ]]; then
   echo "[ERROR] build.sh must be executed with root privileges."
   echo "Run: sudo ./build.sh"
   exit 1
fi

# Step 1: Verify and build local packages as non-root user
BUILDER_USER="${SUDO_USER:-builder}"
if [[ -z "${SUDO_USER:-}" ]] || [[ "${BUILDER_USER}" == "root" ]]; then
    DIR_OWNER="$(stat -c '%U' "${SCRIPT_DIR}")"
    if [[ "${DIR_OWNER}" != "root" ]] && id "${DIR_OWNER}" &>/dev/null; then
        BUILDER_USER="${DIR_OWNER}"
    elif id "builder" &>/dev/null; then
        BUILDER_USER="builder"
    else
        FIRST_USER="$(awk -F: '$3 >= 1000 && $3 < 60000 {print $1; exit}' /etc/passwd)"
        if [[ -n "${FIRST_USER}" ]]; then
            BUILDER_USER="${FIRST_USER}"
        else
            echo "[ERROR] Cannot find a non-root user to build packages (makepkg cannot run as root)."
            exit 1
        fi
    fi
fi

echo "[STEP 1/4] Checking and building in-tree standard Arch packages (user: ${BUILDER_USER})..."
mkdir -p "${LOCALREPO_DIR}"
chown -R "${BUILDER_USER}:${BUILDER_USER}" "${LOCALREPO_DIR}" "${PKGS_DIR}"

BUILD_PKG_ARGS=()
if [[ "${REBUILD_PKGS}" == true ]]; then
    BUILD_PKG_ARGS+=("--rebuild")
fi

if command -v sudo &>/dev/null; then
    sudo -u "${BUILDER_USER}" -H bash "${SCRIPT_DIR}/scripts/build-packages.sh" "${BUILD_PKG_ARGS[@]}"
elif command -v runuser &>/dev/null; then
    runuser -u "${BUILDER_USER}" -- bash "${SCRIPT_DIR}/scripts/build-packages.sh" "${BUILD_PKG_ARGS[@]}"
else
    su -s /bin/bash "${BUILDER_USER}" -c "$(printf '%q ' bash "${SCRIPT_DIR}/scripts/build-packages.sh" "${BUILD_PKG_ARGS[@]}")"
fi

# Step 2: Clean previous build workspace
echo "[STEP 2/4] Initializing clean workspace at ${WORK_DIR}..."
rm -rf "${WORK_DIR}"
mkdir -p "${WORK_DIR}"
mkdir -p "${OUT_DIR}"

# Step 3: Configure pacman.conf with absolute local repository path
echo "[STEP 3/4] Preparing pacman build configuration..."
sed "s|@ENERCO_LOCAL_REPO_PATH@|${LOCALREPO_DIR}|g" "${PACMAN_CONF_TEMPLATE}" > "${BUILD_PACMAN_CONF}"

# Ensure airootfs systemd unit links are genuine POSIX symlinks (guards against Windows core.symlinks=false rsync)
mkdir -p "${SCRIPT_DIR}/airootfs/etc/systemd/system/multi-user.target.wants" \
         "${SCRIPT_DIR}/airootfs/etc/systemd/system-generators"
ln -sf /dev/null "${SCRIPT_DIR}/airootfs/etc/systemd/system/NetworkManager-wait-online.service"
ln -sf /dev/null "${SCRIPT_DIR}/airootfs/etc/systemd/system/systemd-loop.service"
ln -sf /dev/null "${SCRIPT_DIR}/airootfs/etc/systemd/system/systemd-loop@.service"
ln -sf /dev/null "${SCRIPT_DIR}/airootfs/etc/systemd/system/systemd-networkd-wait-online.service"
ln -sf /dev/null "${SCRIPT_DIR}/airootfs/etc/systemd/system-generators/systemd-gpt-auto-generator"
ln -sf /usr/lib/systemd/system/NetworkManager.service "${SCRIPT_DIR}/airootfs/etc/systemd/system/multi-user.target.wants/NetworkManager.service"
ln -sf /usr/lib/systemd/system/irqbalance.service "${SCRIPT_DIR}/airootfs/etc/systemd/system/multi-user.target.wants/irqbalance.service"
ln -sf /usr/lib/systemd/system/systemd-zram-setup@.service "${SCRIPT_DIR}/airootfs/etc/systemd/system/multi-user.target.wants/systemd-zram-setup@zram0.service"
ln -sf /usr/lib/systemd/system/vboxservice.service "${SCRIPT_DIR}/airootfs/etc/systemd/system/multi-user.target.wants/vboxservice.service"

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
    # Drop caches to reclaim RAM from mksquashfs before drvfs transfer
    sync
    echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
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
