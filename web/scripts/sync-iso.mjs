#!/usr/bin/env node
/**
 * Syncs or links built EnercoOS ISOs from ../dist/ into ./public/downloads/
 * for direct static serving on org.megatama-enerco.com/downloads/*.iso
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoDist = path.resolve(__dirname, "../../dist");
const publicDownloads = path.resolve(__dirname, "../public/downloads");

fs.mkdirSync(publicDownloads, { recursive: true });

// Check if ../dist exists and has ISOs
const distExists = fs.existsSync(repoDist);
const distIsos = distExists ? fs.readdirSync(repoDist).filter((f) => f.endsWith(".iso")) : [];

if (distIsos.length > 0) {
  for (const iso of distIsos) {
    const src = path.join(repoDist, iso);
    const dest = path.join(publicDownloads, iso);

    try {
      if (fs.existsSync(dest)) {
        fs.unlinkSync(dest);
      }
      // Prefer hardlink or symlink to avoid duplicating 2.8+ GB on disk
      try {
        fs.linkSync(src, dest);
        console.log(`[sync:iso] Hardlinked ${iso} -> public/downloads/${iso}`);
      } catch {
        fs.symlinkSync(src, dest);
        console.log(`[sync:iso] Symlinked ${iso} -> public/downloads/${iso}`);
      }
    } catch (err) {
      console.warn(`[sync:iso] Could not link ${iso}: ${err.message}`);
    }
  }
} else {
  // Check if ISOs already exist directly in public/downloads/
  const existingDownloads = fs.readdirSync(publicDownloads).filter((f) => f.endsWith(".iso"));
  if (existingDownloads.length > 0) {
    console.log(`[sync:iso] Serving ${existingDownloads.length} existing ISO(s) directly from public/downloads/:`);
    for (const iso of existingDownloads) {
      const stat = fs.statSync(path.join(publicDownloads, iso));
      console.log(`  - ${iso} (${(stat.size / (1024 * 1024 * 1024)).toFixed(2)} GB)`);
    }
  } else {
    console.log("[sync:iso] Note: No .iso files found in ../dist/ or public/downloads/ yet.");
    console.log("[sync:iso] The web portal is fully ready to build and run!");
    console.log("[sync:iso] To enable download links, simply upload your .iso file to:");
    console.log(`          ${publicDownloads}`);
  }
}

process.exit(0);
