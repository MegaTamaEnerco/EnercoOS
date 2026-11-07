import Link from "next/link";
import {
  Download,
  BookOpen,
  ExternalLink,
  Terminal,
  ShieldCheck,
  Cpu,
  HardDrive,
  Layers,
  ArrowRight,
  Server,
} from "lucide-react";
import { DesktopPreview } from "@/components/DesktopPreview";
import { CopyButton } from "@/components/CopyButton";
import { getAllDocsMeta, getAllReleases } from "@/lib/content";

const PACKAGES = [
  {
    name: "enerco-branding",
    version: "1.0.0-8",
    license: "GPL-3.0-or-later",
    summary: "Corporate PT Mega Tama Enerco emblems, enerco-mac.png wallpaper, /etc/os-release",
  },
  {
    name: "enerco-macshell",
    version: "1.0.0-5",
    license: "GPL-3.0-or-later",
    summary: "Unified Quickshell Liquid Glass desktop (MacBar, MacDock, MacSpot, MacLock) + supervisor",
  },
  {
    name: "enerco-desktop-config",
    version: "1.0.0-23",
    license: "GPL-3.0-or-later",
    summary: "Hyprland 0.57 Lua config (hyprland.lua), SDDM Wayland kiosk greeter, Kitty, Rofi, Zsh",
  },
  {
    name: "enerco-enterprise-tools",
    version: "1.0.0-17",
    license: "GPL-3.0-or-later",
    summary: "Smart GPU/VM wrapper (enerco-session), enerco-mterp, ZRAM, udev I/O & sysctl tuning",
  },
  {
    name: "calamares",
    version: "3.3.11-2",
    license: "GPL-3.0-or-later",
    summary: "Native Qt6 / KDE Frameworks 6 graphical disk installer",
  },
  {
    name: "enerco-calamares-config",
    version: "1.0.0-19",
    license: "GPL-3.0-or-later",
    summary: "Partitioning, dual-kernel initramfs, POSIX systemd symlink provisioning, live cleanup",
  },
  {
    name: "macos-like-icon-theme",
    version: "1.0.0-1",
    license: "GPL-3.0-or-later",
    summary: "High-DPI vector application and system icon theme for GTK, Qt, and Quickshell",
  },
];

const SHORTCUTS = [
  { keys: "Super + Space", action: "Open Enerco Search (MacSpot Apps, Clipboard & Emoji)" },
  { keys: "Super + Return", action: "Launch Kitty Terminal" },
  { keys: "Super + B", action: "Launch MTERP Enterprise Web App (mterp.megatama-enerco.com)" },
  { keys: "Super + E", action: "Open Thunar File Manager" },
  { keys: "Super + I", action: "Launch Install EnercoOS (Calamares)" },
  { keys: "Super + L", action: "Lock Workstation Screen (MacLock)" },
  { keys: "Super + W / Q", action: "Close Active Window" },
  { keys: "Super + F11..F8", action: "Switch Display Resolution (1080p / 768p / 800p / Auto)" },
];

export default async function HomePage() {
  const releases = await getAllReleases();
  const latestRelease = releases[0];
  const docs = getAllDocsMeta();

  return (
    <div className="pb-20">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-16 sm:pt-16 sm:pb-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/[0.04] px-3.5 py-1 text-xs font-medium text-[#d5ddf0]">
              <span className="h-2 w-2 rounded-full bg-[#3898ff]" />
              <span>
                EnercoOS {latestRelease?.version ?? "2026.11.07"} · Official PT Mega Tama Enerco Workstation
              </span>
            </div>

            <h1 className="mt-6 text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl">
              The Liquid Glass Enterprise Linux Workstation
            </h1>

            <p className="mt-5 text-base leading-relaxed text-[#b4bcd0] sm:text-lg">
              Built on Arch Linux by{" "}
              <strong className="font-semibold text-white">PT Mega Tama Enerco</strong>. Combines a
              unified Qt6/QML Liquid Glass desktop (`MacShell` + `Hyprland`) with native{" "}
              <strong className="font-semibold text-white">MTERP</strong> integration, smart
              GPU/VM hardware detection, and turnkey Calamares disk installation.
            </p>

            <div className="mt-8 flex flex-wrap items-center justify-center gap-3.5">
              <a
                href={latestRelease?.isoUrl ?? "/downloads/enercoos-2026.11.07-x86_64.iso"}
                className="inline-flex items-center gap-2.5 rounded-xl bg-[#0071e3] px-6 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-[#1482f5]"
              >
                <Download className="h-4 w-4" />
                <span>Download ISO ({latestRelease?.version ?? "2026.11.07"})</span>
              </a>

              <Link
                href="/docs/getting-started"
                className="inline-flex items-center gap-2 rounded-xl border border-white/15 bg-white/[0.05] px-5 py-3 text-sm font-semibold text-white transition hover:border-white/25 hover:bg-white/[0.1]"
              >
                <BookOpen className="h-4 w-4 text-[#58a6ff]" />
                <span>Read Documentation</span>
              </Link>

              <Link
                href="/releases"
                className="inline-flex items-center gap-1.5 rounded-xl px-4 py-3 text-sm font-medium text-[#b4bcd0] transition hover:text-white"
              >
                <span>SHA-256 & Release Notes</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>

          {/* Interactive Desktop Showcase */}
          <div className="mt-12">
            <DesktopPreview />
          </div>
        </div>
      </section>

      {/* Architectural Pillars */}
      <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <h2 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
            Engineered for Enterprise Reliability & Speed
          </h2>
          <p className="mt-2 text-sm leading-relaxed text-[#b4bcd0]">
            Every layer of EnercoOS is packaged as reproducible Arch `PKGBUILD` recipes and verified
            against 185 automated end-to-end tests.
          </p>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
          <div className="liquid-glass rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#0071e3]/20 text-[#58a6ff] border border-[#0071e3]/30">
                <Layers className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-semibold text-white">
                Unified Liquid Glass Shell (`MacShell` + `Hyprland`)
              </h3>
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[#b4bcd0]">
              Runs `MacBar`, `MacDock`, `MacSpot`, `MacNotif`, and `MacLock` inside a single
              Quickshell 0.3.2 process on Hyprland 0.57.1. Delivers real-time frosted glass shaders,
              global application menus, and pure PT Mega Tama Enerco corporate identity with zero
              third-party trademark symbols.
            </p>
          </div>

          <div className="liquid-glass rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                <Cpu className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-semibold text-white">
                Smart Hardware & Hypervisor Session (`enerco-session`)
              </h3>
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[#b4bcd0]">
              Inspects `systemd-detect-virt`, `lspci`, and DMI signatures at login. Automatically
              enables hardware VA-API/DRM acceleration on Intel, AMD, and NVIDIA bare metal while
              activating `pixman` / `llvmpipe` software rendering fallbacks on VirtualBox, QEMU, and
              VMware guests.
            </p>
          </div>

          <div className="liquid-glass rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/15 text-amber-300 border border-amber-500/30">
                <HardDrive className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-semibold text-white">
                Turnkey Calamares 3.3.11 Disk Installer
              </h3>
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[#b4bcd0]">
              Provisions UEFI (`GRUB` with EFI fallback) and BIOS disks, installs dual kernels
              (`vmlinuz-linux-zen` & `vmlinuz-linux`), configures `SDDM` Wayland kiosk login, and
              purges all live-only installation artifacts before first boot.
            </p>
          </div>

          <div className="liquid-glass rounded-2xl p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-semibold text-white">
                MTERP Integration & Endpoint Hardening
              </h3>
            </div>
            <p className="mt-3 text-sm leading-relaxed text-[#b4bcd0]">
              Ships with a dedicated Chromium Ozone Wayland launcher (`enerco-mterp`) for{" "}
              <a
                href="https://mterp.megatama-enerco.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#58a6ff] underline underline-offset-2"
              >
                mterp.megatama-enerco.com
              </a>
              , LibreOffice Fresh, ZRAM zstd swap, CachyOS-tuned sysctl/udev I/O rules, and UFW
              firewall policies.
            </p>
          </div>
        </div>
      </section>

      {/* Two-Column Technical Reference: Packages + Shortcuts */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12">
          {/* In-Tree PKGBUILD Table */}
          <div className="lg:col-span-7 liquid-glass rounded-2xl p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-white">
                  Modular Arch `PKGBUILD` Repository (`pkgs/`)
                </h2>
                <p className="mt-1 text-xs text-[#9aa5be]">
                  Compiled via `scripts/build-packages.sh` into `localrepo/enerco-local.db.tar.gz`
                </p>
              </div>
              <Link
                href="/docs/architecture-and-packaging"
                className="text-xs font-semibold text-[#58a6ff] hover:text-white transition"
              >
                Architecture Docs →
              </Link>
            </div>

            <div className="mt-5 overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-white/10 text-[#9aa5be]">
                    <th className="pb-2.5 pr-4 font-semibold">Package</th>
                    <th className="pb-2.5 pr-4 font-semibold">Version</th>
                    <th className="pb-2.5 font-semibold">Role</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {PACKAGES.map((pkg) => (
                    <tr key={pkg.name}>
                      <td className="py-2.5 pr-4 font-mono font-medium text-[#58a6ff] whitespace-nowrap">
                        {pkg.name}
                      </td>
                      <td className="py-2.5 pr-4 font-mono text-white tabular-nums whitespace-nowrap">
                        {pkg.version}
                      </td>
                      <td className="py-2.5 text-[#b4bcd0]">{pkg.summary}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Default Shortcuts & Quick Build Commands */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            <div className="liquid-glass rounded-2xl p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white">Default Workstation Shortcuts</h2>
                <Link
                  href="/docs/desktop-and-shortcuts"
                  className="text-xs font-semibold text-[#58a6ff] hover:text-white transition"
                >
                  Full Table →
                </Link>
              </div>

              <div className="mt-4 divide-y divide-white/5 text-xs">
                {SHORTCUTS.map((sc) => (
                  <div key={sc.keys} className="flex items-center justify-between py-2 gap-3">
                    <kbd className="rounded border border-white/15 bg-black/40 px-2 py-0.5 font-mono text-[11px] font-medium text-white whitespace-nowrap">
                      {sc.keys}
                    </kbd>
                    <span className="text-right text-[#b4bcd0]">{sc.action}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="liquid-glass rounded-2xl p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Terminal className="h-4 w-4 text-emerald-400" />
                  <h3 className="text-sm font-bold text-white">Build & Verify from Source</h3>
                </div>
                <CopyButton text="python tests/runner.py && sudo ./build.sh" label="Copy Cmd" />
              </div>
              <pre className="mt-3 overflow-x-auto rounded-lg border border-white/10 bg-black/50 p-3 font-mono text-xs text-[#d5ddf0]">
{`# Run 185 E2E tests & build bootable ISO
python tests/runner.py
sudo ./build.sh`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Documentation Hub Directory */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-white">
              Documentation & Operations Guides
            </h2>
            <p className="mt-1 text-sm text-[#b4bcd0]">
              Managed directly via Markdown files in `web/content/docs/` — ready for instant updates.
            </p>
          </div>
          <Link
            href="/docs/deployment-pm2-cloudflared"
            className="inline-flex items-center gap-2 rounded-lg border border-white/15 bg-white/[0.04] px-3.5 py-2 text-xs font-semibold text-white transition hover:bg-white/[0.08]"
          >
            <Server className="h-3.5 w-3.5 text-[#58a6ff]" />
            <span>PM2 + Cloudflared Deployment Guide</span>
          </Link>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {docs.map((doc) => (
            <Link
              key={doc.slug}
              href={`/docs/${doc.slug}`}
              className="group liquid-glass flex flex-col justify-between rounded-xl p-5 transition hover:border-[#58a6ff]/50"
            >
              <div>
                <div className="flex items-center justify-between text-[11px] font-medium text-[#8ea0c0]">
                  <span>{doc.category}</span>
                  <span className="font-mono tabular-nums">{doc.updatedAt}</span>
                </div>
                <h3 className="mt-2 text-base font-semibold text-white group-hover:text-[#58a6ff] transition">
                  {doc.title}
                </h3>
                <p className="mt-1.5 text-xs leading-relaxed text-[#b4bcd0]">
                  {doc.description}
                </p>
              </div>
              <div className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-[#58a6ff]">
                <span>Read guide</span>
                <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
