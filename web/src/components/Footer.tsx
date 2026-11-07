import Link from "next/link";
import { ExternalLink, ShieldCheck } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-white/10 bg-[#06070c]/90">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          <div className="md:col-span-2">
            <div className="flex items-center gap-3">
              <img
                src="/enerco-logo.svg"
                alt="PT Mega Tama Enerco"
                className="h-7 w-7 rounded-md"
              />
              <span className="text-base font-bold tracking-tight text-white">
                EnercoOS Enterprise Workstation
              </span>
            </div>
            <p className="mt-3 max-w-md text-sm leading-relaxed text-[#9aa5be]">
              Open-source Arch Linux enterprise workstation platform developed by{" "}
              <strong className="font-semibold text-white">PT Mega Tama Enerco</strong>.
              Powered by Hyprland, Quickshell (MacShell Liquid Glass), Calamares 3.3.11, and
              direct MTERP integration.
            </p>
            <div className="mt-4 inline-flex items-center gap-2 rounded-md border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs text-[#b4bcd0]">
              <ShieldCheck className="h-4 w-4 text-[#3898ff]" />
              <span>Licensed under GNU GPL v3.0 or later (GPL-3.0-or-later)</span>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-white">
              Documentation
            </h3>
            <ul className="mt-3 space-y-2 text-sm text-[#9aa5be]">
              <li>
                <Link href="/docs/getting-started" className="hover:text-white transition">
                  Overview & System Requirements
                </Link>
              </li>
              <li>
                <Link href="/docs/installation" className="hover:text-white transition">
                  Calamares Installation Guide
                </Link>
              </li>
              <li>
                <Link href="/docs/desktop-and-shortcuts" className="hover:text-white transition">
                  Liquid Glass & Keyboard Shortcuts
                </Link>
              </li>
              <li>
                <Link href="/docs/architecture-and-packaging" className="hover:text-white transition">
                  PKGBUILD & Archiso Architecture
                </Link>
              </li>
              <li>
                <Link href="/docs/updating-and-maintenance" className="hover:text-white transition">
                  System Updates & Maintenance
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-white">
              PT Mega Tama Enerco
            </h3>
            <ul className="mt-3 space-y-2 text-sm text-[#9aa5be]">
              <li>
                <Link href="/releases" className="hover:text-white transition">
                  Direct ISO Downloads & SHA-256
                </Link>
              </li>
              <li>
                <Link href="/docs/open-source-and-legal" className="hover:text-white transition">
                  Open Source Credits & Legal
                </Link>
              </li>
              <li>
                <a
                  href="https://mterp.megatama-enerco.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:text-white transition"
                >
                  MTERP Enterprise ERP
                  <ExternalLink className="h-3 w-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://org.megatama-enerco.com"
                  className="inline-flex items-center gap-1 hover:text-white transition"
                >
                  org.megatama-enerco.com
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-10 flex flex-col items-start justify-between gap-4 border-t border-white/10 pt-6 text-xs text-[#7f8aa3] sm:flex-row sm:items-center">
          <p>
            © {new Date().getFullYear()} PT Mega Tama Enerco (org.megatama-enerco.com). All rights reserved.
          </p>
          <p>
            Linux® is a registered trademark of Linus Torvalds. EnercoOS is not affiliated with Apple Inc. or Arch Linux.
          </p>
        </div>
      </div>
    </footer>
  );
}
