---
title: "Updating EnercoOS & Adding Docs"
description: "Workflow for building updated EnercoOS ISOs, adding new Markdown documentation pages, and publishing new ISO releases on org.megatama-enerco.com."
category: "Operations & Deployment"
order: 5
updatedAt: "2026-11-07"
---

## 1. How to Add or Update Documentation

All documentation on `org.megatama-enerco.com/docs` is driven directly by Markdown files inside `web/content/docs/`. No database or React code changes are required.

### Creating a New Documentation Page

Create a new `.md` file in `web/content/docs/<your-slug>.md` with YAML frontmatter at the top:

```markdown
---
title: "VPN & Corporate Network Setup"
description: "Configuring OpenVPN and WireGuard profiles on EnercoOS workstations."
category: "Operations & Deployment"
order: 8
updatedAt: "2026-11-07"
---

## Connecting to PT Mega Tama Enerco VPN

Run the following command or import your `.ovpn` profile in NetworkManager...
```

- **`category`:** Groups the document in the left sidebar (`Fundamentals`, `User Guide`, `Engineering`, `Operations & Deployment`, or any custom category name).
- **`order`:** Controls the sort order in the sidebar (lowest number first).
- **Table of Contents:** Any `##` (`h2`) and `###` (`h3`) headings in your Markdown are automatically extracted into the right-hand **On This Page** navigation rail.

---

## 2. How to Publish a New EnercoOS ISO Release

When you modify an EnercoOS package in `pkgs/`:

### Step 1: Bump `pkgrel` and Build the ISO

1. Increment `pkgrel` in the modified package's `pkgs/<package>/PKGBUILD`.
2. Run the automated test suite and build the ISO:
   ```bash
   python tests/runner.py
   sudo ./build.sh
   ```
3. The built ISO is written to `dist/enercoos-YYYY.MM.DD-x86_64.iso`.

### Step 2: Link the ISO into `web/public/downloads/`

From the `web/` directory, run:

```bash
cd web
npm run sync:iso
```

This script hardlinks (or symlinks) every `.iso` file from `../dist/` into `web/public/downloads/` so Next.js can serve `/downloads/enercoos-YYYY.MM.DD-x86_64.iso` directly without duplicating 2.8 GB on disk.

### Step 3: Add a Release Note File in `web/content/releases/`

Create `web/content/releases/YYYY.MM.DD.md` (for example `web/content/releases/2026.12.01.md`):

```markdown
---
version: "2026.12.01"
codename: "Liquid Glass Enterprise"
date: "2026-12-01"
channel: "Stable"
isoFilename: "enercoos-2026.12.01-x86_64.iso"
isoUrl: "/downloads/enercoos-2026.12.01-x86_64.iso"
isoSize: "2.8 GB"
sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
kernel: "Linux 7.2.14-zen1 + Linux 7.2.14"
installer: "Calamares 3.3.11 (Qt6)"
shell: "MacShell 1.0.0-5 (Quickshell 0.3.2 + Hyprland 0.57.1)"
---

## Highlights in 2026.12.01

- Updated kernel and security packages
- Improved MTERP session launch speed
```

### Step 4: Rebuild & Reload PM2

```bash
cd web
npm run pm2:reload
```

The landing page hero badge, `/releases` download button, SHA-256 verifier, and release history timeline will immediately update to your newest version.
