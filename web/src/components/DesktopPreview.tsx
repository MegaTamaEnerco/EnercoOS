"use client";

import { useState } from "react";
import {
  Terminal,
  HardDrive,
  Globe,
  Search,
  Wifi,
  Volume2,
  BatteryCharging,
  FolderClosed,
  CheckCircle2,
  Cpu,
  Shield,
} from "lucide-react";

type ActiveApp = "installer" | "terminal" | "mterp" | "search";

export function DesktopPreview() {
  const [activeApp, setActiveApp] = useState<ActiveApp>("installer");

  const appTitleMap: Record<ActiveApp, string> = {
    installer: "Install EnercoOS",
    terminal: "Kitty — zsh",
    mterp: "MTERP Enterprise Portal",
    search: "Enerco Search",
  };

  return (
    <div className="relative mx-auto w-full max-w-5xl">
      {/* Interactive Mode Switcher Bar above the screen */}
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2 px-1">
        <div className="flex items-center gap-2 text-xs text-[#9aa5be]">
          <span className="inline-block h-2 w-2 rounded-full bg-emerald-400" />
          <span>Interactive EnercoOS Liquid Glass Preview (`qs -c MacShell` on `Hyprland 0.57.1`)</span>
        </div>
        <div className="flex flex-wrap items-center gap-1.5">
          {(
            [
              { id: "installer", label: "Calamares 3.3.11", icon: HardDrive },
              { id: "terminal", label: "Kitty Terminal", icon: Terminal },
              { id: "mterp", label: "MTERP Web App", icon: Globe },
              { id: "search", label: "MacSpot (Super+Space)", icon: Search },
            ] as const
          ).map((item) => {
            const Icon = item.icon;
            const isSelected = activeApp === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setActiveApp(item.id)}
                className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition cursor-pointer ${
                  isSelected
                    ? "bg-[#0071e3] text-white shadow-sm"
                    : "border border-white/10 bg-white/[0.04] text-[#b4bcd0] hover:bg-white/[0.08] hover:text-white"
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                {item.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Simulated Monitor Frame */}
      <div className="relative overflow-hidden rounded-2xl border border-white/15 bg-[#07080d] shadow-2xl">
        {/* Wallpaper Background (real enerco-mac.png) */}
        <div
          className="relative min-h-[460px] w-full bg-cover bg-center sm:min-h-[510px]"
          style={{ backgroundImage: "url('/enerco-mac.png')" }}
        >
          {/* Top MacBar (Liquid Glass Menu Bar) */}
          <div className="flex h-8 w-full items-center justify-between border-b border-white/10 bg-[#0b0d17]/75 px-3.5 text-xs text-white backdrop-blur-xl">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 font-semibold">
                <img src="/enerco-logo.svg" alt="MTE" className="h-4 w-4 rounded-sm" />
                <span>{appTitleMap[activeApp]}</span>
              </div>
              <div className="hidden sm:flex items-center gap-3.5 text-[11px] text-white/75">
                <span>File</span>
                <span>Edit</span>
                <span>View</span>
                <span>Window</span>
                <span>Help</span>
              </div>
            </div>

            <div className="flex items-center gap-1.5 rounded-full bg-white/10 px-2.5 py-0.5 text-[11px] font-medium">
              <span>Workspace 1</span>
            </div>

            <div className="flex items-center gap-3 text-[11px] text-white/85">
              <Wifi className="h-3.5 w-3.5" />
              <Volume2 className="h-3.5 w-3.5" />
              <div className="hidden sm:flex items-center gap-1">
                <span>100%</span>
                <BatteryCharging className="h-3.5 w-3.5 text-emerald-400" />
              </div>
              <button
                type="button"
                onClick={() => setActiveApp("search")}
                className="hover:text-[#58a6ff] transition cursor-pointer"
                title="Open Enerco Search"
              >
                <Search className="h-3.5 w-3.5" />
              </button>
              <span className="font-medium tabular-nums">Sat 7 Nov 12:30</span>
            </div>
          </div>

          {/* Desktop Shortcuts on Right */}
          <div className="hidden lg:flex flex-col gap-4 position absolute right-5 top-12 z-10 items-center text-center">
            <button
              type="button"
              onClick={() => setActiveApp("installer")}
              className="group flex flex-col items-center gap-1 rounded-xl p-2 hover:bg-white/10 transition cursor-pointer"
            >
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#0071e3]/90 text-white shadow-lg">
                <HardDrive className="h-6 w-6" />
              </div>
              <span className="text-[11px] font-medium text-white drop-shadow">
                Install EnercoOS
              </span>
            </button>

            <button
              type="button"
              onClick={() => setActiveApp("mterp")}
              className="group flex flex-col items-center gap-1 rounded-xl p-2 hover:bg-white/10 transition cursor-pointer"
            >
              <img
                src="/enerco-logo.svg"
                alt="MTERP"
                className="h-11 w-11 rounded-xl shadow-lg"
              />
              <span className="text-[11px] font-medium text-white drop-shadow">
                MTERP ERP
              </span>
            </button>
          </div>

          {/* Active Window Surface */}
          <div className="flex items-center justify-center px-4 pt-6 pb-20 sm:px-8">
            {activeApp === "installer" && (
              <div className="w-full max-w-2xl overflow-hidden rounded-xl border border-white/15 bg-[#101320]/90 text-white shadow-2xl backdrop-blur-2xl">
                <div className="flex items-center justify-between border-b border-white/10 bg-white/[0.03] px-4 py-2.5">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-rose-500/80" />
                    <span className="h-3 w-3 rounded-full bg-amber-400/80" />
                    <span className="h-3 w-3 rounded-full bg-emerald-500/80" />
                  </div>
                  <span className="text-xs font-medium text-[#b4bcd0]">
                    EnercoOS 2026 Enterprise Workstation Installer (Calamares 3.3.11)
                  </span>
                  <span className="text-[11px] font-mono text-[#7f8aa3]">Qt6 · Wayland</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-12">
                  {/* Left Sidebar Steps */}
                  <div className="border-b border-white/10 bg-[#0b0d17]/60 p-4 sm:col-span-4 sm:border-b-0 sm:border-r">
                    <div className="flex items-center gap-2.5 pb-4 border-b border-white/10">
                      <img src="/enerco-logo.svg" alt="Enerco" className="h-8 w-8 rounded-lg" />
                      <div>
                        <div className="text-xs font-bold text-white">PT Mega Tama Enerco</div>
                        <div className="text-[10px] text-[#9aa5be]">Enterprise Edition</div>
                      </div>
                    </div>
                    <ul className="mt-4 space-y-1.5 text-xs">
                      <li className="rounded-md px-2.5 py-1.5 text-emerald-400 flex items-center justify-between">
                        <span>1. Welcome</span>
                        <CheckCircle2 className="h-3.5 w-3.5" />
                      </li>
                      <li className="rounded-md px-2.5 py-1.5 text-emerald-400 flex items-center justify-between">
                        <span>2. Location & Timezone</span>
                        <CheckCircle2 className="h-3.5 w-3.5" />
                      </li>
                      <li className="rounded-md px-2.5 py-1.5 text-emerald-400 flex items-center justify-between">
                        <span>3. Partitions (EFI + ext4)</span>
                        <CheckCircle2 className="h-3.5 w-3.5" />
                      </li>
                      <li className="rounded-md px-2.5 py-1.5 text-emerald-400 flex items-center justify-between">
                        <span>4. Enterprise User</span>
                        <CheckCircle2 className="h-3.5 w-3.5" />
                      </li>
                      <li className="rounded-md bg-[#0071e3] px-2.5 py-1.5 font-semibold text-white">
                        5. Ready to Install
                      </li>
                    </ul>
                  </div>

                  {/* Right Installer Body */}
                  <div className="p-5 sm:col-span-8 flex flex-col justify-between">
                    <div>
                      <h3 className="text-base font-bold text-white">
                        Turnkey Enterprise Workstation Deployment
                      </h3>
                      <p className="mt-1.5 text-xs leading-relaxed text-[#b4bcd0]">
                        Calamares provisions dual kernels (`vmlinuz-linux-zen` & `vmlinuz-linux`),
                        enables `NetworkManager`, `systemd-zram-setup@zram0`, and `vboxservice`,
                        and configures the `SDDM` Wayland login session automatically.
                      </p>

                      <div className="mt-4 space-y-2 rounded-lg border border-white/10 bg-black/35 p-3 text-xs font-mono">
                        <div className="flex justify-between">
                          <span className="text-[#8ea0c0]">Bootloader:</span>
                          <span className="text-emerald-300">UEFI GRUB + EFI Fallback</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-[#8ea0c0]">Display Greeter:</span>
                          <span className="text-[#58a6ff]">SDDM Wayland (weston kiosk)</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-[#8ea0c0]">Target Session:</span>
                          <span className="text-white">/usr/local/bin/enerco-session</span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-5 flex items-center justify-between border-t border-white/10 pt-3">
                      <span className="text-[11px] text-[#9aa5be]">
                        185/185 E2E Verification Tests Passed
                      </span>
                      <button
                        type="button"
                        onClick={() => setActiveApp("terminal")}
                        className="rounded-lg bg-[#0071e3] px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-[#1482f5] transition cursor-pointer"
                      >
                        Inspect Terminal →
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeApp === "terminal" && (
              <div className="w-full max-w-2xl overflow-hidden rounded-xl border border-white/15 bg-[#080a12]/95 text-white shadow-2xl backdrop-blur-2xl font-mono">
                <div className="flex items-center justify-between border-b border-white/10 bg-white/[0.03] px-4 py-2.5 font-sans">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-rose-500/80" />
                    <span className="h-3 w-3 rounded-full bg-amber-400/80" />
                    <span className="h-3 w-3 rounded-full bg-emerald-500/80" />
                  </div>
                  <span className="text-xs font-medium text-[#b4bcd0]">
                    kitty — admin@mte-workstation:~
                  </span>
                  <span className="text-[11px] text-[#7f8aa3]">zsh 5.9</span>
                </div>

                <div className="p-5 text-xs leading-relaxed">
                  <div className="text-emerald-400">
                    admin@mte-workstation <span className="text-[#58a6ff]">~</span> $ cat /etc/os-release
                  </div>
                  <pre className="mt-1.5 text-[#d5ddf0] overflow-x-auto">
{`NAME="EnercoOS"
PRETTY_NAME="EnercoOS Enterprise Workstation 2026"
ID=enercoos
VERSION="2026 Enterprise"
BUILD_ID=2026.11
HOME_URL="https://org.megatama-enerco.com"`}
                  </pre>

                  <div className="mt-4 text-emerald-400">
                    admin@mte-workstation <span className="text-[#58a6ff]">~</span> $ uname -r && qs --version
                  </div>
                  <div className="mt-1 text-[#b4bcd0]">
                    7.2.14-zen1-1-zen — Quickshell 0.3.2 (MacShell Liquid Glass Active)
                  </div>

                  <div className="mt-4 text-emerald-400">
                    admin@mte-workstation <span className="text-[#58a6ff]">~/EnercoOS</span> $ python tests/runner.py
                  </div>
                  <div className="mt-1 text-emerald-300">
                    [PASS] 185 / 185 E2E Tests Passed (0 failures, 0 errors in 0.28s)
                  </div>
                </div>
              </div>
            )}

            {activeApp === "mterp" && (
              <div className="w-full max-w-2xl overflow-hidden rounded-xl border border-white/15 bg-[#101320]/95 text-white shadow-2xl backdrop-blur-2xl">
                <div className="flex items-center justify-between border-b border-white/10 bg-[#312e59]/50 px-4 py-2.5">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-rose-500/80" />
                    <span className="h-3 w-3 rounded-full bg-amber-400/80" />
                    <span className="h-3 w-3 rounded-full bg-emerald-500/80" />
                  </div>
                  <span className="text-xs font-medium text-white">
                    MTERP — https://mterp.megatama-enerco.com (Ozone Wayland Native)
                  </span>
                  <span className="text-[11px] font-mono text-emerald-300">TLS 1.3</span>
                </div>

                <div className="p-6">
                  <div className="flex items-center gap-3">
                    <img src="/enerco-logo.svg" alt="MTE" className="h-10 w-10 rounded-xl" />
                    <div>
                      <h3 className="text-base font-bold text-white">
                        PT Mega Tama Enerco — MTERP Suite
                      </h3>
                      <p className="text-xs text-[#b4bcd0]">
                        Dedicated Wayland Web App (`enerco-mterp` · `Super + B`)
                      </p>
                    </div>
                  </div>

                  <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-3">
                    <div className="rounded-lg border border-white/10 bg-white/[0.04] p-3">
                      <div className="flex items-center gap-2 text-xs font-semibold text-white">
                        <Cpu className="h-4 w-4 text-[#58a6ff]" />
                        Zero-Copy GPU
                      </div>
                      <p className="mt-1 text-[11px] text-[#9aa5be]">
                        Launches with `--ozone-platform=wayland` and VA-API hardware acceleration.
                      </p>
                    </div>
                    <div className="rounded-lg border border-white/10 bg-white/[0.04] p-3">
                      <div className="flex items-center gap-2 text-xs font-semibold text-white">
                        <Shield className="h-4 w-4 text-emerald-400" />
                        Isolated Profile
                      </div>
                      <p className="mt-1 text-[11px] text-[#9aa5be]">
                        Dedicated Dock icon, desktop launcher, and corporate security policy.
                      </p>
                    </div>
                    <div className="rounded-lg border border-white/10 bg-white/[0.04] p-3">
                      <div className="flex items-center gap-2 text-xs font-semibold text-white">
                        <Globe className="h-4 w-4 text-amber-300" />
                        Instant Hotkey
                      </div>
                      <p className="mt-1 text-[11px] text-[#9aa5be]">
                        Press `Super + B` from any workspace to open MTERP immediately.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeApp === "search" && (
              <div className="w-full max-w-lg overflow-hidden rounded-2xl border border-white/20 bg-[#121626]/90 text-white shadow-2xl backdrop-blur-2xl">
                <div className="flex items-center gap-3 border-b border-white/10 px-4 py-3.5">
                  <Search className="h-5 w-5 text-[#58a6ff]" />
                  <span className="text-sm font-medium text-white">
                    mterp — Enerco Search (MacSpot)
                  </span>
                  <span className="ml-auto rounded border border-white/15 bg-white/5 px-1.5 py-0.5 text-[10px] font-mono text-[#9aa5be]">
                    Super + Space
                  </span>
                </div>
                <div className="divide-y divide-white/5 p-2 text-xs">
                  <div className="flex items-center justify-between rounded-lg bg-[#0071e3] px-3 py-2.5 text-white">
                    <div className="flex items-center gap-2.5">
                      <img src="/enerco-logo.svg" alt="MTERP" className="h-5 w-5 rounded" />
                      <span className="font-semibold">MTERP Enterprise ERP</span>
                    </div>
                    <span className="text-[11px] text-white/80">mterp.megatama-enerco.com</span>
                  </div>
                  <div className="flex items-center justify-between px-3 py-2.5 text-[#c5cde0]">
                    <div className="flex items-center gap-2.5">
                      <HardDrive className="h-4 w-4 text-[#58a6ff]" />
                      <span>Install EnercoOS (Calamares)</span>
                    </div>
                    <span className="font-mono text-[11px] text-[#7f8aa3]">Super + I</span>
                  </div>
                  <div className="flex items-center justify-between px-3 py-2.5 text-[#c5cde0]">
                    <div className="flex items-center gap-2.5">
                      <Terminal className="h-4 w-4 text-emerald-400" />
                      <span>Kitty Terminal</span>
                    </div>
                    <span className="font-mono text-[11px] text-[#7f8aa3]">Super + Return</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Bottom Floating MacDock */}
          <div className="absolute bottom-3 left-1/2 -translate-x-1/2">
            <div className="flex items-center gap-2.5 rounded-2xl border border-white/20 bg-[#101424]/80 px-3.5 py-2 shadow-2xl backdrop-blur-2xl">
              <button
                type="button"
                onClick={() => setActiveApp("installer")}
                title="Thunar File Manager"
                className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-500/20 text-sky-300 border border-sky-400/30 transition hover:-translate-y-1 cursor-pointer"
              >
                <FolderClosed className="h-5 w-5" />
              </button>
              <button
                type="button"
                onClick={() => setActiveApp("mterp")}
                title="MTERP Enterprise ERP"
                className={`flex h-10 w-10 items-center justify-center rounded-xl border transition hover:-translate-y-1 cursor-pointer ${
                  activeApp === "mterp"
                    ? "border-[#58a6ff] bg-[#312e59]"
                    : "border-white/15 bg-[#312e59]/70"
                }`}
              >
                <img src="/enerco-logo.svg" alt="MTERP" className="h-7 w-7 rounded-md" />
              </button>
              <button
                type="button"
                onClick={() => setActiveApp("terminal")}
                title="Kitty Terminal"
                className={`flex h-10 w-10 items-center justify-center rounded-xl border transition hover:-translate-y-1 cursor-pointer ${
                  activeApp === "terminal"
                    ? "border-emerald-400 bg-emerald-500/25 text-emerald-300"
                    : "border-white/15 bg-black/50 text-emerald-400"
                }`}
              >
                <Terminal className="h-5 w-5" />
              </button>
              <button
                type="button"
                onClick={() => setActiveApp("installer")}
                title="Install EnercoOS (Calamares)"
                className={`flex h-10 w-10 items-center justify-center rounded-xl border transition hover:-translate-y-1 cursor-pointer ${
                  activeApp === "installer"
                    ? "border-white/50 bg-[#0071e3] text-white"
                    : "border-white/15 bg-[#0071e3]/70 text-white"
                }`}
              >
                <HardDrive className="h-5 w-5" />
              </button>
              <button
                type="button"
                onClick={() => setActiveApp("search")}
                title="Enerco Search (MacSpot)"
                className={`flex h-10 w-10 items-center justify-center rounded-xl border transition hover:-translate-y-1 cursor-pointer ${
                  activeApp === "search"
                    ? "border-[#58a6ff] bg-[#0071e3]/40 text-white"
                    : "border-white/15 bg-white/10 text-white"
                }`}
              >
                <Search className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
