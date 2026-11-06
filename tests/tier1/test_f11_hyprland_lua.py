"""Tier 1: Feature 11 - Hyprland 0.57 Lua Configuration Unification Tests (Min 5 tests).

Derivation source: ORIGINAL_REQUEST.md (R2), PROJECT.md (Feature 11), TEST_INFRA.md, Survey 3 finding 2.
Validates Hyprland Lua syntax, presence of hardware media/audio keys, brightness controls,
MacShell layer rules, and spotlight search launcher bindings.
"""

import unittest
from tests.config import (
    read_repo_file,
    repo_file_exists,
)


class TestF11HyprlandLua(unittest.TestCase):
    """Tier 1 test suite for Feature 11: Hyprland 0.57 Lua Configuration Unification."""

    def test_hyprland_lua_exists(self):
        """T1-F11-1: Verify pkgs/enerco-desktop-config/hyprland.lua exists."""
        self.assertTrue(
            repo_file_exists("pkgs/enerco-desktop-config/hyprland.lua"),
            "pkgs/enerco-desktop-config/hyprland.lua must exist",
        )

    def test_hyprland_lua_hardware_audio_keys(self):
        """T1-F11-2: Verify hyprland.lua defines audio volume and mute hotkeys (wpctl/pipewire)."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        self.assertTrue(
            "XF86AudioRaiseVolume" in content or "wpctl" in content,
            "hyprland.lua must define hardware audio raise volume keybinding",
        )
        self.assertTrue(
            "XF86AudioLowerVolume" in content or "wpctl" in content,
            "hyprland.lua must define hardware audio lower volume keybinding",
        )
        self.assertTrue(
            "XF86AudioMute" in content or "wpctl" in content,
            "hyprland.lua must define hardware audio mute keybinding",
        )

    def test_hyprland_lua_hardware_brightness_keys(self):
        """T1-F11-3: Verify hyprland.lua defines monitor brightness keys (brightnessctl)."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        self.assertTrue(
            "XF86MonBrightness" in content or "brightnessctl" in content,
            "hyprland.lua must define hardware monitor brightness keybindings",
        )

    def test_hyprland_lua_macshell_layer_rules(self):
        """T1-F11-4: Verify hyprland.lua configures MacShell layer rules (macbarbg/macdock/macspot)."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        has_macshell_layers = (
            "macbarbg" in content
            or "macdock" in content
            or "macspot" in content
            or "MacShell" in content
        )
        self.assertTrue(
            has_macshell_layers,
            "hyprland.lua must configure layer rules for MacShell dark glass blur components",
        )

    def test_hyprland_lua_spotlight_launcher_binding(self):
        """T1-F11-5: Verify Super+Space triggers spotlight search or application launcher."""
        content = read_repo_file("pkgs/enerco-desktop-config/hyprland.lua")
        self.assertIn("space", content.lower(), "hyprland.lua must bind Super+Space for application search")
        self.assertTrue(
            "spotlight" in content or "rofi" in content or "menu" in content,
            "hyprland.lua must configure spotlight or rofi menu for application launching",
        )


if __name__ == "__main__":
    unittest.main()
