# EnercoOS Web Portal & Documentation Hub (`org.megatama-enerco.com`)

Official Next.js App Router portal, documentation hub (`/docs`), and direct ISO release center (`/releases`) for **EnercoOS 2026 Enterprise Workstation** by **PT Mega Tama Enerco**.

---

## Quick Start (PM2 + Cloudflared Production Deployment)

```bash
cd web

# 1. Install dependencies & link built ISOs from ../dist/ into public/downloads/
npm install
npm run sync:iso

# 2. Build production bundle
npm run build

# 3. Start under PM2 (binds to 127.0.0.1:3080 via ecosystem.config.cjs)
npm run pm2:start
pm2 save
```

### Cloudflared Tunnel Origin Mapping

Point `org.megatama-enerco.com` in your existing Cloudflare Tunnel (`cloudflared`) to:

```text
http://127.0.0.1:3080
```

See the full guide inside [`content/docs/deployment-pm2-cloudflared.md`](content/docs/deployment-pm2-cloudflared.md) (or at `https://org.megatama-enerco.com/docs/deployment-pm2-cloudflared`).

---

## Updating Documentation & Publishing New Releases

- **Add/Edit Documentation:** Edit or drop a Markdown (`.md`) file in `web/content/docs/`
- **Add/Edit Releases:** Drop a new release `.md` file in `web/content/releases/` and run `npm run sync:iso`
- **Reload Live Site with Zero Downtime:**
  ```bash
  npm run pm2:reload
  ```
