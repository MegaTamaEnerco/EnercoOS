---
title: "Deploy with PM2 & Cloudflared"
description: "Production deployment guide for running the EnercoOS Next.js portal under PM2 behind your existing Cloudflare Tunnel (cloudflared) for org.megatama-enerco.com."
category: "Operations & Deployment"
order: 6
updatedAt: "2026-11-07"
---

## Architecture Overview

The EnercoOS web portal (`web/`) is pre-configured with `web/ecosystem.config.cjs` to run as a managed **PM2** daemon bound to `127.0.0.1:3080`, allowing your existing **Cloudflare Tunnel (`cloudflared`)** to securely expose `https://org.megatama-enerco.com` to the public internet without opening inbound firewall ports.

```text
Internet Users (https://org.megatama-enerco.com)
       │
       ▼  Cloudflare Edge (TLS + DDoS Protection)
Cloudflare Tunnel (cloudflared daemon on host)
       │
       ▼  http://127.0.0.1:3080
PM2 Process ("enercoos-web" via web/ecosystem.config.cjs)
       │
       ├── Next.js App Router (/, /docs/*, /releases)
       └── Direct Static ISO Serving (/downloads/*.iso -> web/public/downloads/)
```

---

## 1. Build & Start with PM2

Ensure `pm2` is installed globally (`npm install -g pm2`), then build and launch the portal from the `web/` directory:

```bash
cd /path/to/EnercoOS/web

# 1. Install dependencies & link built ISOs from ../dist/ into public/downloads/
npm install
npm run sync:iso

# 2. Build the production Next.js bundle
npm run build

# 3. Start the PM2 service using ecosystem.config.cjs (binds to 127.0.0.1:3080)
npm run pm2:start

# 4. Persist PM2 process list across server reboots
pm2 save
pm2 startup
```

### Useful PM2 Management Commands

| Command | Description |
| :--- | :--- |
| `pm2 status` | Check status, PID, uptime, and memory usage of `enercoos-web` |
| `pm2 logs enercoos-web` | Stream live stdout/stderr logs (`web/logs/pm2-out.log` & `pm2-error.log`) |
| `npm run pm2:reload` | Rebuild Next.js and perform a zero-downtime PM2 reload (`build && pm2 reload`) |
| `pm2 restart enercoos-web` | Instant restart without rebuilding |
| `npm run pm2:stop` | Stop the `enercoos-web` process |

---

## 2. Connect Your Existing `cloudflared` Tunnel

Since you already have `cloudflared` configured, point `org.megatama-enerco.com` to `http://127.0.0.1:3080` using whichever method your tunnel uses:

### Option A: Cloudflare Zero Trust Dashboard (Remotely Managed Tunnel)

1. Open **Cloudflare Zero Trust Dashboard** -> **Networks** -> **Tunnels**.
2. Select your active tunnel and click **Configure** -> **Public Hostname** -> **Add a public hostname**:
   - **Subdomain:** `org`
   - **Domain:** `megatama-enerco.com`
   - **Service Type:** `HTTP`
   - **URL:** `127.0.0.1:3080`
3. Under **Additional application settings -> HTTP Settings**, enable **Chunked Encoding** (default) so large ISO streams smoothly.
4. Click **Save hostname**.

### Option B: Local `config.yml` (`/etc/cloudflared/config.yml` or `~/.cloudflared/config.yml`)

Add the `org.megatama-enerco.com` ingress rule above your catch-all `http_status:404` rule:

```yaml
tunnel: <YOUR-TUNNEL-UUID>
credentials-file: /etc/cloudflared/<YOUR-TUNNEL-UUID>.json

ingress:
  - hostname: org.megatama-enerco.com
    service: http://127.0.0.1:3080
    originRequest:
      noTLSVerify: true
      connectTimeout: 30s

  - hostname: mterp.megatama-enerco.com
    service: http://127.0.0.1:8080 # (Your existing MTERP service port)

  - service: http_status:404
```

Then route the DNS CNAME (if not already added) and restart `cloudflared`:

```bash
cloudflared tunnel route dns <YOUR-TUNNEL-NAME> org.megatama-enerco.com
sudo systemctl restart cloudflared
```

---

## 3. Cloudflare Cache Rule for Large ISO Downloads (`2.8 GB`)

Cloudflare's default proxy caches individual files up to `512 MB` on Free/Pro plans. To ensure direct ISO downloads (`https://org.megatama-enerco.com/downloads/enercoos-2026.11.07-x86_64.iso`) stream directly from your origin without hitting Cloudflare's cache-size cap:

1. In the **Cloudflare Dashboard** for `megatama-enerco.com`, go to **Caching** -> **Cache Rules** -> **Create rule**.
2. **Rule name:** `Bypass Cache for EnercoOS ISOs`
3. **When incoming requests match:**
   - **Field:** `URI Path` -> **Operator:** `starts with` -> **Value:** `/downloads/`
4. **Then -> Cache eligibility:** Select **Bypass cache**.
5. Click **Deploy**.

---

## 4. Zero-Downtime Update Workflow

Whenever you edit documentation in `web/content/docs/*.md`, add a release note in `web/content/releases/*.md`, or build a new ISO in `dist/`:

```bash
cd /path/to/EnercoOS/web
git pull
npm run sync:iso
npm run pm2:reload
```

Your changes go live on `https://org.megatama-enerco.com` within seconds.
