"""EnercoOS E2E Test Suite Configuration and Environment Detection.

Provides cross-platform paths, environment discovery (Windows host, WSL 2 Arch Linux,
VirtualBox CLI), and helper utilities for reading repository artifacts and running commands.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Base repository root
TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent

# OS and Platform detection
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")
IS_WSL = False
if IS_LINUX:
    try:
        with open("/proc/version", "r", encoding="utf-8") as f:
            proc_ver = f.read().lower()
            IS_WSL = "microsoft" in proc_ver or "wsl" in proc_ver
    except Exception:
        IS_WSL = False

# VirtualBox VBoxManage path resolution
def get_vboxmanage_path() -> Optional[str]:
    """Find the VBoxManage executable on Windows host or Linux."""
    if IS_WINDOWS:
        common_paths = [
            r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe",
            r"C:\Program Files (x86)\Oracle\VirtualBox\VBoxManage.exe",
        ]
        for p in common_paths:
            if os.path.exists(p):
                return p
        # Check PATH
        try:
            res = subprocess.run(["where", "VBoxManage"], capture_output=True, text=True, check=False)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip().splitlines()[0]
        except Exception:
            pass
    else:
        try:
            res = subprocess.run(["which", "VBoxManage"], capture_output=True, text=True, check=False)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
    return None

VBOXMANAGE_PATH = get_vboxmanage_path()

# WSL distribution detection
def is_wsl_available() -> bool:
    """Check if WSL with archlinux distribution is available on Windows."""
    if not IS_WINDOWS:
        return False
    try:
        res = subprocess.run(["wsl", "-l", "-q"], capture_output=True, text=True, check=False)
        if res.returncode == 0:
            # Output might be UTF-16 on Windows
            stdout = res.stdout.replace("\x00", "")
            return "archlinux" in stdout.lower()
    except Exception:
        pass
    return False

HAS_WSL_ARCHLINUX = is_wsl_available()

def get_repo_path(relative_path: str) -> Path:
    """Get absolute path to a file relative to repository root."""
    return REPO_ROOT / relative_path

def read_repo_file(relative_path: str) -> str:
    """Read a repository file as text (UTF-8, fallback Latin-1)."""
    p = get_repo_path(relative_path)
    if not p.exists():
        raise FileNotFoundError(f"Repository file not found: {relative_path} (resolved {p})")
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="latin-1")

def repo_file_exists(relative_path: str) -> bool:
    """Check if a file exists relative to repository root."""
    return get_repo_path(relative_path).exists()

def run_in_wsl(command: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Execute a bash command inside the WSL archlinux environment."""
    if not IS_WINDOWS:
        return subprocess.run(["bash", "-c", command], capture_output=True, text=True, timeout=timeout)
    full_cmd = ["wsl", "-d", "archlinux", "bash", "-c", command]
    return subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)

def run_host_command(cmd_list: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Execute a command directly on the host."""
    return subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
