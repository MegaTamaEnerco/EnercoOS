/**
 * PM2 Ecosystem Configuration for EnercoOS Portal (org.megatama-enerco.com)
 * Pre-configured for Cloudflare Tunnel (cloudflared) origin routing on port 3080.
 *
 * Usage:
 *   npm run build
 *   pm2 start ecosystem.config.cjs --env production
 *   pm2 save
 */
module.exports = {
  apps: [
    {
      name: "enercoos-web",
      script: "node_modules/next/dist/bin/next",
      args: "start -H 127.0.0.1 -p 3080",
      cwd: __dirname,
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      watch: false,
      max_memory_restart: "512M",
      env: {
        NODE_ENV: "development",
        PORT: 3080,
        HOSTNAME: "127.0.0.1",
        NEXT_TELEMETRY_DISABLED: "1",
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 3080,
        HOSTNAME: "127.0.0.1",
        NEXT_TELEMETRY_DISABLED: "1",
        SITE_URL: "https://org.megatama-enerco.com",
        MTERP_URL: "https://mterp.megatama-enerco.com",
      },
      error_file: "./logs/pm2-error.log",
      out_file: "./logs/pm2-out.log",
      merge_logs: true,
      time: true,
    },
  ],
};
