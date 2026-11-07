#!/usr/bin/env node
/**
 * Syncs or links built EnercoOS ISOs from ../dist/ into ./public/downloads/
 * for direct static serving on org.megatama-enerco.com/downloads/*.iso
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoDist = path.resolve(__dirname, "../../dist");
const publicDownloads = path.resolve(__dirname, "../public/downloads");

fs.mkdirSync(publicDownloads, { recursive: true });

if (!fs.existsSync(repoDist)) {
  console.log("[sync:iso] No ../dist directory found yet. Skipping ISO link.");
  process.exit(0);
}

const isoFiles = fs.readdirSync(repoDist).filter((f) => f.endsWith(".iso"));

for (const iso of isoFiles) {
  const src = path.join(repoDist, iso);
  const dest = path.join(publicDownloads, iso);

  try {
    if (fs.existsSync(dest)) {
      fs.unlinkSync(dest);
    }
    // Prefer hardlink or symlink to avoid duplicating 2.8 GB on disk
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
