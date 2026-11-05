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

# Define build order (Calamares dependencies and assets first)
PACKAGES=(
    "enerco-branding"
    "enerco-desktop-config"
    "enerco-enterprise-tools"
    "calamares"
    "enerco-calamares-config"
)

USE_CHROOT=false
if [[ "${1:-}" == "--chroot" ]]; then
    USE_CHROOT=true
    echo "[INFO] Clean chroot build requested (using devtools extra-x86_64-build)."
fi

for pkg in "${PACKAGES[@]}"; do
    pkg_path="${PKGS_DIR}/${pkg}"
    if [[ ! -d "${pkg_path}" || ! -f "${pkg_path}/PKGBUILD" ]]; then
        echo "[WARN] Skipping ${pkg}: No PKGBUILD found at ${pkg_path}"
        continue
    fi

    # Check if package was already built
    if compgen -G "${LOCALREPO_DIR}/${pkg}-*.pkg.tar.zst" >/dev/null; then
        echo "[INFO] ${pkg} already built in localrepo, skipping recompilation."
        continue
    fi

    echo ">>> Building package: ${pkg} ..."
    pushd "${pkg_path}" >/dev/null

    # Clean prior build remnants
    rm -rf src/ pkg/ *.pkg.tar.*

    if [[ "${USE_CHROOT}" == true ]]; then
        extra-x86_64-build
    else
        # Use -d to allow in-tree cross dependencies without host pre-installation
        makepkg -sfd --noconfirm --skippgpcheck
    fi

    # Move generated packages to localrepo
    find . -maxdepth 1 -name "*.pkg.tar.*" -exec mv -v {} "${LOCALREPO_DIR}/" \;

    popd >/dev/null
    echo ">>> Successfully built ${pkg}."
    echo ""
done

# Update pacman repo database
echo "=== Updating Repository Database (${DB_NAME}) ==="
pushd "${LOCALREPO_DIR}" >/dev/null

# Clean old symlinks if any
rm -f enerco-local.db enerco-local.files

# Exclude debug packages from main repository index
PKG_FILES=$(ls *.pkg.tar.zst 2>/dev/null | grep -v -- '-debug-' || true)

if [[ -n "${PKG_FILES}" ]]; then
    # shellcheck disable=SC2086
    repo-add -n -R "${DB_NAME}" ${PKG_FILES}
    echo "=== Local repository updated successfully! ==="
    ls -lh
else
    echo "[ERROR] No packages found in ${LOCALREPO_DIR} to add to repository."
    exit 1
fi

popd >/dev/null

