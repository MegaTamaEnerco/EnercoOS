#!/usr/bin/env python3
"""Apply pure PT Mega Tama Enerco branding to MacShell QML and SVG assets."""

import os
import shutil
import subprocess
import sys

WHITE_EMBLEM_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 283.5 283.5" width="64" height="64">
  <title>PT Mega Tama Enerco Emblem</title>
  <path fill="#ffffff" d="M148.415 117.112 L186.186 170.731 C186.408 171.101 186.852 171.323 187.297 171.323 L230.992 171.323 C231.733 171.323 232.325 170.731 232.325 169.99 L232.399 61.048 C232.399 60.308 231.807 59.715 231.066 59.715 L190.629 59.715 C190.259 59.715 189.889 59.863 189.667 60.16 L147.304 106.521 C146.786 107.114 145.897 107.114 145.379 106.595 L99.462 60.16 C99.24 59.937 98.869 59.789 98.499 59.789 L52.434 59.789 C51.693 59.789 51.101 60.382 51.101 61.122 L51.101 178.137 C51.101 178.581 51.323 178.952 51.619 179.174 L99.758 214.796 C100.425 215.315 101.387 215.019 101.758 214.278 L146.194 117.334 C146.564 116.445 147.823 116.297 148.415 117.112 Z"/>
</svg>
"""

BLACK_EMBLEM_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 283.5 283.5" width="64" height="64">
  <title>PT Mega Tama Enerco Emblem</title>
  <path fill="#1d1b38" d="M148.415 117.112 L186.186 170.731 C186.408 171.101 186.852 171.323 187.297 171.323 L230.992 171.323 C231.733 171.323 232.325 170.731 232.325 169.99 L232.399 61.048 C232.399 60.308 231.807 59.715 231.066 59.715 L190.629 59.715 C190.259 59.715 189.889 59.863 189.667 60.16 L147.304 106.521 C146.786 107.114 145.897 107.114 145.379 106.595 L99.462 60.16 C99.24 59.937 98.869 59.789 98.499 59.789 L52.434 59.789 C51.693 59.789 51.101 60.382 51.101 61.122 L51.101 178.137 C51.101 178.581 51.323 178.952 51.619 179.174 L99.758 214.796 C100.425 215.315 101.387 215.019 101.758 214.278 L146.194 117.334 C146.564 116.445 147.823 116.297 148.415 117.112 Z"/>
</svg>
"""


def brand_macshell_dir(ms_dir: str, logo_svg: str) -> None:
    # 1. Replace third-party SVG/PNG logo assets with PT Mega Tama Enerco emblem
    with open(os.path.join(ms_dir, "apple-logo-white.svg"), "w", encoding="utf-8") as f:
        f.write(WHITE_EMBLEM_SVG)
    with open(os.path.join(ms_dir, "apple-logo-black.svg"), "w", encoding="utf-8") as f:
        f.write(BLACK_EMBLEM_SVG)

    assets_dir = os.path.join(ms_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    shutil.copy2(logo_svg, os.path.join(assets_dir, "linux-logo.svg"))
    try:
        subprocess.run(
            ["rsvg-convert", "-w", "256", "-h", "256", logo_svg, "-o", os.path.join(assets_dir, "macshell-logo.png")],
            check=True,
        )
    except Exception:
        pass

    # 2. Brand AboutApp.qml
    about_path = os.path.join(ms_dir, "AboutApp.qml")
    if os.path.isfile(about_path):
        txt = open(about_path, "r", encoding="utf-8").read()
        txt = txt.replace('title: "About This Linux"', 'title: "About EnercoOS"')
        txt = txt.replace('text: "MacShell"', 'text: "EnercoOS"')
        txt = txt.replace(
            'text: "Linux® is a registered trademark of Linus Torvalds.\\nMacShell 0.5.1"',
            'text: "PT Mega Tama Enerco · Enterprise Workstation\\norg.megatama-enerco.com"',
        )
        old_more_block = """                Item {
                    width: parent.width; height: 24
                    Rectangle {
                        anchors.centerIn: parent
                        width: moreTxt.implicitWidth + 30; height: 24; radius: 7
                        color: moreMa.pressed ? pal.btnDown : pal.btn
                        border.width: 1; border.color: pal.border
                        Text { id: moreTxt; anchors.centerIn: parent; text: I18n.tr("More Info\\u2026"); color: pal.text; font.family: root.fontForWeight(Font.Normal, root.fam); font.pixelSize: 12 }
                        MouseArea {
                            id: moreMa; anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                var cmd = (root.bar ? root.bar.terminal : "kitty") + " -e sh -c 'fastfetch || neofetch; echo; read -p \\\"Press Enter\\\" _'";
                                Quickshell.execDetached(["sh", "-c", cmd]);
                            }
                        }
                    }
                }"""
        new_more_block = """                Item {
                    width: parent.width; height: 24
                    Row {
                        anchors.horizontalCenter: parent.horizontalCenter
                        spacing: 8
                        Rectangle {
                            width: updateTxt.implicitWidth + 20; height: 24; radius: 7
                            color: updateMa.pressed ? pal.btnDown : pal.btn
                            border.width: 1; border.color: pal.border
                            Text { id: updateTxt; anchors.centerIn: parent; text: I18n.tr("Software Update\\u2026"); color: pal.text; font.family: root.fontForWeight(Font.Normal, root.fam); font.pixelSize: 12 }
                            MouseArea {
                                id: updateMa; anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                onClicked: Quickshell.execDetached(["/usr/local/bin/enerco-update"])
                            }
                        }
                        Rectangle {
                            width: moreTxt.implicitWidth + 20; height: 24; radius: 7
                            color: moreMa.pressed ? pal.btnDown : pal.btn
                            border.width: 1; border.color: pal.border
                            Text { id: moreTxt; anchors.centerIn: parent; text: I18n.tr("More Info\\u2026"); color: pal.text; font.family: root.fontForWeight(Font.Normal, root.fam); font.pixelSize: 12 }
                            MouseArea {
                                id: moreMa; anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    var cmd = (root.bar ? root.bar.terminal : "kitty") + " -e sh -c 'fastfetch || neofetch; echo; read -p \\\"Press Enter\\\" _'";
                                    Quickshell.execDetached(["sh", "-c", cmd]);
                                }
                            }
                        }
                    }
                }"""
        txt = txt.replace(old_more_block, new_more_block)
        open(about_path, "w", encoding="utf-8").write(txt)

    # 3. Brand MacBar.qml
    bar_path = os.path.join(ms_dir, "MacBar.qml")
    if os.path.isfile(bar_path):
        txt = open(bar_path, "r", encoding="utf-8").read()
        txt = txt.replace('property string barLogoMode: "arch"', 'property string barLogoMode: "custom"')
        txt = txt.replace(
            'property string barCustomLogoPath: ""',
            'property string barCustomLogoPath: "/usr/share/pixmaps/enerco-logo.svg"',
        )
        txt = txt.replace(
            'barLogoMode = "arch"; barCustomLogoPath = "";',
            'barLogoMode = "custom"; barCustomLogoPath = "/usr/share/pixmaps/enerco-logo.svg";',
        )
        txt = txt.replace(
            'property string updateUrl: "https://github.com/0-ss/MacShell/releases/latest"',
            'property string updateUrl: "https://org.megatama-enerco.com"',
        )
        txt = txt.replace(
            'function openUpdateLink() { Quickshell.execDetached(["xdg-open", updateUrl]); }',
            'function openUpdateLink() { Quickshell.execDetached(["/usr/local/bin/enerco-update"]); }',
        )
        old_apple_about = """            m.push(ico(mi("About This Linux", "", function () {
                if (hub && hub.about) hub.about.open();
                else sh(terminal + " -e sh -c 'fastfetch || neofetch; echo; read -p \\\"Press Enter\\\" _'");
            }), "m_about"));"""
        new_apple_about = """            m.push(ico(mi("About EnercoOS", "", function () {
                if (hub && hub.about) hub.about.open();
                else sh(terminal + " -e sh -c 'fastfetch || neofetch; echo; read -p \\\"Press Enter\\\" _'");
            }), "m_about"));
            m.push(ico(mi("Software Update\\u2026", "", function () {
                Quickshell.execDetached(["/usr/local/bin/enerco-update"]);
            }), "system-software-update"));"""
        txt = txt.replace(old_apple_about, new_apple_about)
        txt = txt.replace('mi("About This Linux"', 'mi("About EnercoOS"')
        txt = txt.replace(
            'm.push(mi("Hyprland Keybinds", "", function () { Quickshell.execDetached(["xdg-open", "https://github.com/0-ss/MacShell#hyprland-configuration-lua"]); }));',
            'm.push(mi("EnercoOS Shortcuts", "", function () { Quickshell.execDetached(["/usr/local/bin/enerco-welcome", "--force"]); }));',
        )
        txt = txt.replace(
            'function lookup(appId) {\n        if (!appId) return null;',
            'function lookup(appId) {\n        if (!appId) return null;\n        if (appId === "io.calamares.calamares") appId = "calamares";',
        )
        txt = txt.replace(
            ': (activeTl.title === "macshell Settings" ? I18n.tr("System Settings") : "MacShell");',
            ': (activeTl.title === "macshell Settings" ? I18n.tr("System Settings") : "EnercoOS");',
        )
        txt = txt.replace(
            'id === "org.quickshell" ? "MacShell"',
            'id === "org.quickshell" ? "EnercoOS"',
        )
        # Replace Arch Glyph in top-left bar item with PT Mega Tama Enerco emblem Image
        old_logo_block = """                                Glyph {
                                    visible: mt.modelData.id === "apple" && root.barLogoMode === "arch"
                                    anchors.centerIn: parent
                                    width: 15; height: 15
                                    kind: "arch"
                                    color: bpal.fg
                                }"""
        new_logo_block = """                                Image {
                                    visible: mt.modelData.id === "apple" && root.barLogoMode === "arch"
                                    anchors.centerIn: parent
                                    width: 16; height: 16
                                    source: !root.barTextDark ? Qt.resolvedUrl("apple-logo-white.svg") : Qt.resolvedUrl("apple-logo-black.svg")
                                    sourceSize: Qt.size(64, 64)
                                    fillMode: Image.PreserveAspectFit
                                    smooth: true
                                    mipmap: true
                                }"""
        txt = txt.replace(old_logo_block, new_logo_block)

        old_fallback_block = """                                Glyph {
                                    visible: mt.modelData.id === "apple" && root.barLogoMode === "custom"
                                             && (root.barCustomLogoUrl === "" || customBarLogo.status === Image.Error)
                                    anchors.centerIn: parent
                                    width: 15; height: 15
                                    kind: "arch"
                                    color: bpal.fg
                                }"""
        new_fallback_block = """                                Image {
                                    visible: mt.modelData.id === "apple" && root.barLogoMode === "custom"
                                             && (root.barCustomLogoUrl === "" || customBarLogo.status === Image.Error)
                                    anchors.centerIn: parent
                                    width: 16; height: 16
                                    source: !root.barTextDark ? Qt.resolvedUrl("apple-logo-white.svg") : Qt.resolvedUrl("apple-logo-black.svg")
                                    sourceSize: Qt.size(64, 64)
                                    fillMode: Image.PreserveAspectFit
                                    smooth: true
                                    mipmap: true
                                }"""
        txt = txt.replace(old_fallback_block, new_fallback_block)
        txt = txt.replace('I18n.tr("Spotlight Search")', 'I18n.tr("Enerco Search")')
        open(bar_path, "w", encoding="utf-8").write(txt)

    # 4. Brand MacDock.qml
    dock_path = os.path.join(ms_dir, "MacDock.qml")
    if os.path.isfile(dock_path):
        txt = open(dock_path, "r", encoding="utf-8").read()
        txt = txt.replace(
            'function lookup(appId) {\n        if (!appId) return null;',
            'function lookup(appId) {\n        if (!appId) return null;\n        if (appId === "io.calamares.calamares") appId = "calamares";',
        )
        txt = txt.replace('"Apple Liquid Glass"', '"Enerco Liquid Glass"')
        txt = txt.replace('needs Apple Liquid Glass style', 'needs Enerco Liquid Glass style')
        txt = txt.replace(
            'subtitle: I18n.tr("Choose the Arch mark, Apple logo, or a custom image")',
            'subtitle: I18n.tr("Choose the PT Mega Tama Enerco emblem, badge, or a custom image")',
        )
        txt = txt.replace('model: ["Arch", "Apple", "Custom"]', 'model: ["Enerco Mono", "Enerco Emblem", "Custom"]')
        txt = txt.replace('title: I18n.tr("Apple menu")', 'title: I18n.tr("System menu")')
        txt = txt.replace('title: I18n.tr("Reset MacShell")', 'title: I18n.tr("Reset EnercoOS Shell")')
        txt = txt.replace(
            'text: I18n.tr("Designed by Rick.\\nRebuilt on Linux by two people who could not afford the Mac.")',
            'text: I18n.tr("PT Mega Tama Enerco · Enterprise Workstation\\norg.megatama-enerco.com")',
        )
        txt = txt.replace(
            'text: I18n.tr("Protect your MacShell with AppleCare+")',
            'text: I18n.tr("PT Mega Tama Enerco Enterprise Support")',
        )
        txt = txt.replace(
            'text: I18n.tr("Unlimited repairs for accidental damage, 24/7 priority access to Apple experts, and battery service coverage. Same price as for a MacBook Pro.")',
            'text: I18n.tr("Official enterprise workstation platform for PT Mega Tama Enerco. Integrated with MTERP and corporate security policies.")',
        )
        txt = txt.replace(
            'text: I18n.tr("$279.00 for 3 years or $99.99/yr.")',
            'text: I18n.tr("org.megatama-enerco.com · mterp.megatama-enerco.com")',
        )
        txt = txt.replace('text: I18n.tr("Add AppleCare+")', 'text: I18n.tr("Enterprise Portal")')
        txt = txt.replace('name: own ? "MacShell"', 'name: own ? "EnercoOS"')
        txt = txt.replace('name: own3 ? (tl.title || "MacShell")', 'name: own3 ? (tl.title || "EnercoOS")')
        open(dock_path, "w", encoding="utf-8").write(txt)

    # 5. Enable WindowDecor in shell.qml for macOS traffic lights & window frames on every window
    shell_path = os.path.join(ms_dir, "shell.qml")
    if os.path.isfile(shell_path):
        txt = open(shell_path, "r", encoding="utf-8").read()
        if "WindowDecor {" not in txt:
            # 1. Add decor and decorWantsGeo properties to sharedHub
            txt = txt.replace(
                "property var about: aboutApp\n",
                "property var about: aboutApp\n        property var decor: windowDecor\n",
            )
            txt = txt.replace(
                "property bool dockWantsGeo: false\n",
                "property bool dockWantsGeo: false\n        property bool decorWantsGeo: false\n",
            )
            # 2. Add decorWantsGeo to geo query timers
            txt = txt.replace(
                "(sharedHub.barWantsGeo || sharedHub.dockWantsGeo)",
                "(sharedHub.barWantsGeo || sharedHub.dockWantsGeo || sharedHub.decorWantsGeo)",
            )
            # 3. Instantiate WindowDecor
            txt = txt.replace(
                "AboutApp { id: aboutApp; hub: sharedHub }\n",
                "AboutApp { id: aboutApp; hub: sharedHub }\n    WindowDecor { id: windowDecor; hub: sharedHub }\n",
            )
            # 4. Attach decor to sharedHub in Component.onCompleted
            txt = txt.replace(
                "sharedHub.desktop = desktopIcons;\n",
                "sharedHub.desktop = desktopIcons;\n        sharedHub.decor = windowDecor;\n",
            )
            # 5. Add windecor IPC handler
            windecor_ipc = """    // qs -c MacShell ipc call windecor toggle | on | off
    IpcHandler {
        target: "windecor"
        function toggle(): void { windowDecor.enabled = !windowDecor.enabled; }
        function on(): void { windowDecor.enabled = true; }
        function off(): void { windowDecor.enabled = false; }
    }
"""
            txt = txt.replace(
                "    IpcHandler {\n        target: \"settings\"\n",
                windecor_ipc + "    IpcHandler {\n        target: \"settings\"\n",
            )
            open(shell_path, "w", encoding="utf-8").write(txt)


if __name__ == "__main__":
    logo_svg = sys.argv[1]
    for target_dir in sys.argv[2:]:
        brand_macshell_dir(target_dir, logo_svg)

