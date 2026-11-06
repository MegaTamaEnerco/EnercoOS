#!/usr/bin/env bash
# ==============================================================================
# EnercoOS Package Repository Builder
# Builds all standard PKGBUILDs in pkgs/ and populates localrepo/
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PKGS_DIR="${PROJECT_ROOT}/pkgs"
LOCALREPO_DIR="${PROJECT_ROOT}/localrepo"
DB_NAME="enerco-local.db.tar.gz"

# ------------------------------------------------------------------------------
# Privilege Guard: Drop root privileges to builder user if run as root
# ------------------------------------------------------------------------------
if [[ $EUID -eq 0 ]]; then
    BUILDER_USER="${SUDO_USER:-builder}"
    if ! id "${BUILDER_USER}" &>/dev/null; then
        DIR_OWNER="$(stat -c '%U' "${PROJECT_ROOT}")"
        if [[ "${DIR_OWNER}" != "root" ]] && id "${DIR_OWNER}" &>/dev/null; then
            BUILDER_USER="${DIR_OWNER}"
        else
            echo "[ERROR] Running makepkg as root is not allowed and non-root builder user not found."
            exit 1
        fi
    fi
    echo "[INFO] Running as root; delegating execution to non-root user '${BUILDER_USER}'..."
    mkdir -p "${LOCALREPO_DIR}"
    chown -R "${BUILDER_USER}:${BUILDER_USER}" "${PKGS_DIR}" "${LOCALREPO_DIR}"
    if command -v sudo &>/dev/null; then
        exec sudo -u "${BUILDER_USER}" -H bash "$0" "$@"
    elif command -v runuser &>/dev/null; then
        exec runuser -u "${BUILDER_USER}" -- bash "$0" "$@"
    else
        exec su -s /bin/bash "${BUILDER_USER}" -c "$(printf '%q ' bash "$0" "$@")"
    fi
fi

echo "=== EnercoOS Standard Package Builder ==="
echo "Project Root: ${PROJECT_ROOT}"
echo "Local Repo:   ${LOCALREPO_DIR}"
echo ""

mkdir -p "${LOCALREPO_DIR}"

# Check for makepkg and repo-add
for tool in makepkg repo-add; do
    if ! command -v "${tool}" &>/dev/null; then
        echo "[ERROR] Required tool '${tool}' is not installed in this environment."
        echo "Please run inside an Arch Linux environment with 'base-devel' installed."
        exit 1
    fi
done

# Define canonical build order (Calamares dependencies and assets first)
DEFAULT_PACKAGES=(
    "enerco-branding"
    "macos-like-icon-theme"
    "enerco-macshell"
    "enerco-desktop-config"
    "enerco-enterprise-tools"
    "calamares"
    "enerco-calamares-config"
)

# Parse CLI options
FORCE_REBUILD=false
USE_CHROOT=false
TARGET_PACKAGES=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--force|--rebuild)
            FORCE_REBUILD=true
            shift
            ;;
        --chroot)
            USE_CHROOT=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS] [PACKAGE_NAME...]"
            echo ""
            echo "Options:"
            echo "  -f, --force, --rebuild  Force rebuild packages even if matching version exists in localrepo"
            echo "  --chroot                Use clean chroot build (devtools extra-x86_64-build)"
            echo "  -h, --help              Show this help message"
            echo ""
            echo "Available in-tree packages:"
            for p in "${DEFAULT_PACKAGES[@]}"; do
                echo "  - ${p}"
            done
            exit 0
            ;;
        -*)
            echo "[ERROR] Unknown option: $1"
            echo "Run '$0 --help' for usage."
            exit 1
            ;;
        *)
            TARGET_PACKAGES+=("$1")
            shift
            ;;
    esac
done

if [[ ${#TARGET_PACKAGES[@]} -eq 0 ]]; then
    BUILD_LIST=("${DEFAULT_PACKAGES[@]}")
else
    BUILD_LIST=("${TARGET_PACKAGES[@]}")
fi

# Function: Extract pkgver and pkgrel from PKGBUILD
get_pkg_version_info() {
    local dir="$1"
    local pkgver="" pkgrel=""
    
    # 1. Authoritative extraction via makepkg --printsrcinfo
    if command -v makepkg &>/dev/null && [[ $EUID -ne 0 ]]; then
        local srcinfo
        if srcinfo="$(cd "${dir}" && makepkg --printsrcinfo 2>/dev/null)"; then
            pkgver="$(echo "${srcinfo}" | sed -n 's/^[[:space:]]*pkgver = //p' | head -n 1)"
            pkgrel="$(echo "${srcinfo}" | sed -n 's/^[[:space:]]*pkgrel = //p' | head -n 1)"
        fi
    fi
    
    # 2. Fallback direct extraction from PKGBUILD
    if [[ -z "${pkgver}" || -z "${pkgrel}" ]]; then
        pkgver="$(grep -E '^[[:space:]]*pkgver=' "${dir}/PKGBUILD" | head -n 1 | cut -d= -f2- | sed "s/['\" ]//g")"
        pkgrel="$(grep -E '^[[:space:]]*pkgrel=' "${dir}/PKGBUILD" | head -n 1 | cut -d= -f2- | sed "s/['\" ]//g")"
    fi
    
    if [[ -z "${pkgver}" || -z "${pkgrel}" ]]; then
        echo ""
    else
        echo "${pkgver}-${pkgrel}"
    fi
}

PACKAGES_BUILT=0

# Clean build source destination directory
export SRCDEST="/tmp/enerco-makepkg-sources"
export PKGDEST="${LOCALREPO_DIR}"
mkdir -p "${SRCDEST}"

for pkg in "${BUILD_LIST[@]}"; do
    pkg_path="${PKGS_DIR}/${pkg}"
    if [[ ! -d "${pkg_path}" || ! -f "${pkg_path}/PKGBUILD" ]]; then
        echo "[WARN] Skipping ${pkg}: No PKGBUILD found at ${pkg_path}"
        continue
    fi

    ver_rel="$(get_pkg_version_info "${pkg_path}")"

    # Version comparison check: skip rebuild only if matching version archive exists in localrepo
    if [[ "${FORCE_REBUILD}" != true ]] && [[ -n "${ver_rel}" ]]; then
        if compgen -G "${LOCALREPO_DIR}/${pkg}-${ver_rel}-*.pkg.tar.zst" >/dev/null; then
            echo "[INFO] ${pkg} (${ver_rel}) already built in localrepo, skipping recompilation."
            continue
        else
            echo "[INFO] ${pkg} needs build: target version ${ver_rel} not found in localrepo."
        fi
    elif [[ "${FORCE_REBUILD}" == true ]]; then
        echo "[INFO] Force rebuild requested for ${pkg}."
    fi

    echo ">>> Building package: ${pkg} (${ver_rel:-unknown version}) ..."
    pushd "${pkg_path}" >/dev/null

    # Clean prior in-tree build remnants
    rm -rf src/ pkg/ *.pkg.tar.*

    # Clean prior versions of this package from localrepo to avoid stale duplicates
    rm -f "${LOCALREPO_DIR}/${pkg}-"[0-9]*.pkg.tar.* "${LOCALREPO_DIR}/${pkg}-debug-"[0-9]*.pkg.tar.*

    if [[ "${USE_CHROOT}" == true ]]; then
        extra-x86_64-build
    else
        # Use -C -c to clean src and work files; -sfd for deps & non-confirm
        makepkg -C -c -sfd --noconfirm --skippgpcheck
    fi

    # Remove any debug package from localrepo to conserve disk and stay under size limits
    rm -f "${LOCALREPO_DIR}/${pkg}-debug-"*.pkg.tar.*
    rm -f ./*-debug-*.pkg.tar.* 2>/dev/null || true

    # Move any packages left in directory to localrepo if PKGDEST was ignored
    find . -maxdepth 1 -name "*.pkg.tar.*" ! -name "*-debug-*" -exec mv -v {} "${LOCALREPO_DIR}/" \; 2>/dev/null || true

    # Ensure no lingering src/pkg directories in pkgs/
    rm -rf src/ pkg/

    popd >/dev/null
    PACKAGES_BUILT=$((PACKAGES_BUILT + 1))
    echo ">>> Successfully built ${pkg}."
    echo ""
done

# Update pacman repo database
if [[ ${PACKAGES_BUILT} -gt 0 ]] || [[ ! -f "${LOCALREPO_DIR}/${DB_NAME}" ]]; then
    echo "=== Updating Repository Database (${DB_NAME}) ==="
    pushd "${LOCALREPO_DIR}" >/dev/null

    # Exclude debug packages from main repository index
    PKG_FILES=$(ls *.pkg.tar.zst 2>/dev/null | grep -v -- '-debug-' || true)

    if [[ -n "${PKG_FILES}" ]]; then
        # shellcheck disable=SC2086
        repo-add -R "${DB_NAME}" ${PKG_FILES}

        # Ensure required symlinks exist for pacman sync
        ln -sf "${DB_NAME}" enerco-local.db
        ln -sf "enerco-local.files.tar.gz" enerco-local.files

        echo "=== Local repository updated successfully! ==="
        ls -lh
    else
        echo "[ERROR] No packages found in ${LOCALREPO_DIR} to add to repository."
        exit 1
    fi

    popd >/dev/null
else
    # Ensure symlinks exist even when no packages were recompiled
    pushd "${LOCALREPO_DIR}" >/dev/null
    if [[ -f "${DB_NAME}" ]]; then
        ln -sf "${DB_NAME}" enerco-local.db
        ln -sf "enerco-local.files.tar.gz" enerco-local.files
    fi
    popd >/dev/null
    echo "=== All packages up to date (${PACKAGES_BUILT} built). Database (${DB_NAME}) unchanged. ==="
fi
