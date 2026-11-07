import type { Metadata } from "next";
import Link from "next/link";
import {
  Download,
  ShieldCheck,
  Terminal,
  HardDrive,
  Calendar,
  Cpu,
  Layers,
  BookOpen,
} from "lucide-react";
import { getAllReleases } from "@/lib/content";
import { CopyButton } from "@/components/CopyButton";

export const metadata: Metadata = {
  title: "Releases & Direct ISO Downloads",
  description:
    "Download official EnercoOS 2026 Enterprise Workstation bootable ISO images, verify SHA-256 checksums, and review release notes.",
};

export default async function ReleasesPage() {
  const releases = await getAllReleases();
  const latest = releases[0];

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="max-w-3xl">
        <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
          EnercoOS Releases & Direct ISO Downloads
        </h1>
        <p className="mt-3 text-base leading-relaxed text-[#b4bcd0]">
          Official 64-bit (`x86_64`) UEFI and BIOS bootable installation images built and verified by{" "}
          <strong className="font-semibold text-white">PT Mega Tama Enerco</strong>. Always verify
          the SHA-256 digest before flashing to installation media.
        </p>
      </div>

      {/* Latest Stable Release Card */}
      {latest && (
        <section className="mt-10 liquid-glass rounded-2xl p-6 sm:p-8">
          <div className="flex flex-col justify-between gap-6 border-b border-white/10 pb-6 lg:flex-row lg:items-center">
            <div>
              <div className="flex flex-wrap items-center gap-2.5">
                <span className="rounded-full bg-[#0071e3] px-3 py-0.5 text-xs font-semibold text-white">
                  Latest {latest.channel}
                </span>
                <span className="inline-flex items-center gap-1 text-xs text-[#9aa5be] tabular-nums">
                  <Calendar className="h-3.5 w-3.5" />
                  Released {latest.date}
                </span>
                <span className="text-xs font-mono text-[#58a6ff]">{latest.codename}</span>
              </div>

              <h2 className="mt-3 text-2xl font-bold text-white sm:text-3xl tabular-nums">
                EnercoOS {latest.version} Enterprise Workstation
              </h2>
              <p className="mt-1 font-mono text-xs text-[#9aa5be]">{latest.isoFilename}</p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <a
                href={latest.isoUrl}
                download={latest.isoFilename}
                className="inline-flex items-center gap-2.5 rounded-xl bg-[#0071e3] px-6 py-3.5 text-sm font-semibold text-white shadow-lg transition hover:bg-[#1482f5]"
              >
                <Download className="h-4 w-4" />
                <span>Download ISO ({latest.isoSize.split(" ")[0]})</span>
              </a>

              <Link
                href="/docs/installation"
                className="inline-flex items-center gap-2 rounded-xl border border-white/15 bg-white/[0.05] px-4 py-3.5 text-xs font-semibold text-white transition hover:bg-white/[0.1]"
              >
                <BookOpen className="h-4 w-4 text-[#58a6ff]" />
                <span>Installation Guide</span>
              </Link>
            </div>
          </div>

          {/* Technical Metadata Grid */}
          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-xl border border-white/10 bg-black/30 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold text-[#9aa5be]">
                <Cpu className="h-4 w-4 text-[#58a6ff]" />
                Kernels Included
              </div>
              <div className="mt-1.5 font-mono text-xs text-white">{latest.kernel}</div>
            </div>

            <div className="rounded-xl border border-white/10 bg-black/30 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold text-[#9aa5be]">
                <Layers className="h-4 w-4 text-emerald-400" />
                Desktop Shell
              </div>
              <div className="mt-1.5 font-mono text-xs text-white">{latest.shell}</div>
            </div>

            <div className="rounded-xl border border-white/10 bg-black/30 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold text-[#9aa5be]">
                <HardDrive className="h-4 w-4 text-amber-300" />
                System Installer & Size
              </div>
              <div className="mt-1.5 font-mono text-xs text-white tabular-nums">
                {latest.installer} · {latest.isoSize}
              </div>
            </div>
          </div>

          {/* SHA-256 Checksum Box */}
          <div className="mt-6 rounded-xl border border-white/12 bg-[#06070c] p-4">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2 text-xs font-semibold text-white">
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
                <span>SHA-256 Checksum ({latest.isoFilename})</span>
              </div>
              <CopyButton text={latest.sha256} label="Copy SHA-256" />
            </div>
            <div className="mt-2 overflow-x-auto font-mono text-xs text-emerald-300 tabular-nums select-all">
              {latest.sha256}
            </div>
          </div>

          {/* Verification & Flashing Commands */}
          <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-black/30 p-4">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-xs font-semibold text-white">
                  <Terminal className="h-3.5 w-3.5 text-[#58a6ff]" />
                  Verify & Flash on Linux
                </span>
                <CopyButton
                  text={`sha256sum ${latest.isoFilename}\nsudo dd bs=4M if=${latest.isoFilename} of=/dev/sdX status=progress oflag=sync`}
                  label="Copy"
                />
              </div>
              <pre className="mt-2.5 overflow-x-auto font-mono text-[11px] leading-relaxed text-[#d5ddf0]">
{`sha256sum ${latest.isoFilename}
sudo dd bs=4M if=${latest.isoFilename} of=/dev/sdX status=progress oflag=sync`}
              </pre>
            </div>

            <div className="rounded-xl border border-white/10 bg-black/30 p-4">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-xs font-semibold text-white">
                  <Terminal className="h-3.5 w-3.5 text-[#58a6ff]" />
                  Verify on Windows PowerShell
                </span>
                <CopyButton
                  text={`Get-FileHash .\\${latest.isoFilename} -Algorithm SHA256`}
                  label="Copy"
                />
              </div>
              <pre className="mt-2.5 overflow-x-auto font-mono text-[11px] leading-relaxed text-[#d5ddf0]">
{`Get-FileHash .\\${latest.isoFilename} -Algorithm SHA256
# Expected: ${latest.sha256.toUpperCase()}`}
              </pre>
            </div>
          </div>

          {/* Latest Release Changelog */}
          <div
            className="enerco-prose mt-6"
            dangerouslySetInnerHTML={{ __html: latest.html }}
          />
        </section>
      )}

      {/* Release History Timeline */}
      {releases.length > 1 && (
        <section className="mt-14">
          <h2 className="text-2xl font-bold tracking-tight text-white">
            Previous Releases & Changelog History
          </h2>
          <div className="mt-6 space-y-6">
            {releases.slice(1).map((rel) => (
              <div key={rel.slug} className="liquid-glass rounded-2xl p-6">
                <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-4">
                  <div>
                    <div className="flex items-center gap-2.5">
                      <span className="rounded-md border border-white/15 bg-white/5 px-2.5 py-0.5 text-xs font-medium text-[#b4bcd0]">
                        {rel.channel}
                      </span>
                      <span className="text-xs text-[#8ea0c0] tabular-nums">{rel.date}</span>
                    </div>
                    <h3 className="mt-2 text-xl font-bold text-white tabular-nums">
                      EnercoOS {rel.version} — {rel.codename}
                    </h3>
                  </div>

                  <a
                    href={rel.isoUrl}
                    download={rel.isoFilename}
                    className="inline-flex items-center gap-2 rounded-lg border border-white/15 bg-white/[0.05] px-4 py-2 text-xs font-semibold text-white transition hover:bg-white/[0.1]"
                  >
                    <Download className="h-3.5 w-3.5 text-[#58a6ff]" />
                    <span>{rel.isoFilename} ({rel.isoSize.split(" ")[0]})</span>
                  </a>
                </div>

                <div
                  className="enerco-prose mt-4"
                  dangerouslySetInnerHTML={{ __html: rel.html }}
                />
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
