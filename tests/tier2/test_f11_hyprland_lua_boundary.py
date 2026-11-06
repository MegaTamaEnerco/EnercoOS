"""Tier 2: Feature 11 - Hyprland 0.57 Lua Configuration Unification Boundary Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 11), TEST_INFRA.md, Survey 3 finding 2.
Validates Lua syntax boundaries, absence of incompatible comment styles, multi-monitor fallbacks,
touchpad gesture ergonomics, and macOS styling aesthetics.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF11HyprlandLuaBoundary(unittest.TestCase):
    """Tier 2 boundary test suite for Feature 11: Hyprland 0.57 Lua Configuration Unification."""

    def test_hyprland_lua_no_bash_hash_comments(self):
        """T2-F11-1: Boundary: Verify hyprland.lua does not contain invalid '#' comments outside strings."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        # In Lua, comments start with '--'. Lines beginning with '#' trigger parse error
        for i, line in enumerate(content.splitlines()):
            stripped = line.strip()
            self.assertFalse(
                stripped.startswith("#"),
                f"Line {i+1} starts with invalid Lua comment '#': {stripped}",
            )

    def test_monitor_default_auto_fallback(self):
        """T2-F11-2: Boundary: Verify monitor rules define preferred auto fallback for arbitrary screens."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        self.assertIn("preferred", content, "hyprland.lua must define 'preferred' fallback monitor mode")
        self.assertIn("auto", content, "hyprland.lua must specify auto positioning for multi-monitor")

    def test_touchpad_macos_ergonomics_boundary(self):
        """T2-F11-3: Boundary: Verify touchpad settings enable natural scroll and tap to click."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        self.assertIn("natural_scroll = true", content, "Natural scrolling must be enabled for macOS feel")
        self.assertIn("tap_to_click = true", content, "Tap to click must be enabled")

    def test_window_rule_dialog_floating(self):
        """T2-F11-4: Boundary: Verify window rules float standard dialogs (calamares, pavucontrol, zenity)."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        self.assertIn("calamares", content)
        self.assertIn("pavucontrol", content)
        self.assertIn("zenity", content)

    def test_dark_glass_rounding_and_blur_boundaries(self):
        """T2-F11-5: Boundary: Verify decoration rounding and blur parameters meet macOS Tahoe styling."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        self.assertIn("rounding = 14", content, "Window corner rounding must be 14px")
        self.assertIn("blur = {", content, "Blur must be configured for frosted glass aesthetics")


if __name__ == "__main__":
    unittest.main()
