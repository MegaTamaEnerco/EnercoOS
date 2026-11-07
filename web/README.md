# EnercoOS Web Portal (`org.megatama-enerco.com`)

Official Next.js App Router portal, documentation hub (`/docs`), and direct ISO release center (`/releases`) for **EnercoOS 2026 Enterprise Workstation** by **PT Mega Tama Enerco**.

---

## Development & Production Build

```bash
cd web

# Install dependencies
npm install

# Run local development server (http://localhost:3000)
npm run dev

# Build production bundle
npm run build

# Start production server
npm run start
```

---

## Content Structure

- **Documentation Guides (`/docs`):** Markdown files in `web/content/docs/*.md`
- **Release Notes & SHA-256 Manifests (`/releases`):** Markdown files in `web/content/releases/*.md`
- **Static ISO Downloads (`/downloads`):** Served from `web/public/downloads/`
