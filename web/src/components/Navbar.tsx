import Link from "next/link";
import { Download, ExternalLink, BookOpen, Disc, Layers } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 liquid-glass-bar">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <Link
            href="/"
            className="flex items-center gap-3 text-base font-semibold tracking-tight text-white transition hover:opacity-90"
          >
            <img
              src="/enerco-logo.svg"
              alt="PT Mega Tama Enerco Emblem"
              className="h-8 w-8 rounded-lg shadow-md"
            />
            <div className="flex flex-col">
              <span className="leading-none font-bold tracking-tight text-white">
                EnercoOS
              </span>
              <span className="mt-0.5 text-[11px] font-medium text-[#9aa5be]">
                PT Mega Tama Enerco
              </span>
            </div>
          </Link>

          <nav aria-label="Main Navigation" className="hidden md:flex items-center gap-1">
            <Link
              href="/"
              className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium text-[#c5cde0] transition hover:bg-white/[0.06] hover:text-white"
            >
              <Layers className="h-4 w-4 text-[#58a6ff]" />
              Overview
            </Link>
            <Link
              href="/docs/getting-started"
              className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium text-[#c5cde0] transition hover:bg-white/[0.06] hover:text-white"
            >
              <BookOpen className="h-4 w-4 text-[#58a6ff]" />
              Documentation
            </Link>
            <Link
              href="/releases"
              className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium text-[#c5cde0] transition hover:bg-white/[0.06] hover:text-white"
            >
              <Disc className="h-4 w-4 text-[#58a6ff]" />
              Releases & ISO
            </Link>
            <Link
              href="/docs/deployment-pm2-cloudflared"
              className="rounded-lg px-3 py-1.5 text-sm font-medium text-[#c5cde0] transition hover:bg-white/[0.06] hover:text-white"
            >
              PM2 + Cloudflared
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <a
            href="https://mterp.megatama-enerco.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:inline-flex items-center gap-1.5 rounded-lg border border-white/12 bg-white/[0.04] px-3.5 py-1.5 text-xs font-medium text-[#d5ddf0] transition hover:border-white/25 hover:bg-white/[0.08] hover:text-white"
          >
            MTERP Portal
            <ExternalLink className="h-3.5 w-3.5 text-[#8ea0c0]" />
          </a>

          <Link
            href="/releases"
            className="inline-flex items-center gap-2 rounded-lg bg-[#0071e3] px-3.5 py-1.5 text-xs font-semibold text-white shadow-sm transition hover:bg-[#1482f5]"
          >
            <Download className="h-3.5 w-3.5" />
            <span>Download 2026.11 ISO</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
