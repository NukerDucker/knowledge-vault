> Related: [[Keep Alive]] | [[WallKeeper]]

## Uptime Kuma Setup

Step-by-step for the monitoring host described in [[Keep Alive]]. Goal: ping +
HTTP monitors on each video wall NUC, with **email** alerts.

---

### 0. Install Proxmox on OptiPlex #1
- Flash the Proxmox VE ISO to USB (Rufus / balenaEtcher) and boot OptiPlex #1 from it.
- In BIOS, enable **VT-x / VT-d** (virtualization) — needed for VMs/containers.
- Install Proxmox, give the host a static IP, then reach the web UI at `https://<host-ip>:8006`.
- OptiPlex #2 = the test target: install Windows + a browser pointed at a Grafana page, so there's something realistic to monitor. (See test bed in [[Keep Alive]].)

### 1. Provision the LXC on Proxmox
- Create a Debian LXC (the Proxmox community helper script is the quickest path).
- Minimum spec is fine for 1–5 monitors: 1 vCPU, 512 MB–1 GB RAM, 4 GB disk.
- Make sure it has network access to the NUC subnet (so ICMP ping reaches the devices).
- Give it a static IP / DNS name so the status page URL stays stable.

### 2. Install Uptime Kuma
Direct install (no Docker) inside the LXC:
```bash
# as root in the LXC
apt update && apt install -y git npm
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma
npm run setup
# run it as a service so it survives reboots
npm install pm2 -g
pm2 start server/server.js --name uptime-kuma
pm2 save
pm2 startup    # follow the printed command to enable on boot
```
Then open `http://<lxc-ip>:3001` and create the admin account.

### 3. Add monitors (repeat per NUC)
**Ping monitor**
- Monitor Type: `Ping`
- Friendly Name: e.g. `Video Wall — Floor 3 (ping)`
- Hostname: NUC IP
- Heartbeat Interval: `60` seconds
- Retries: `2`

**HTTP monitor** (catches the frozen-dashboard case)
- Monitor Type: `HTTP(s)`
- Friendly Name: e.g. `Video Wall — Floor 3 (grafana)`
- URL: the local Grafana/MagicSign URL the NUC displays
- Heartbeat Interval: `60` seconds
- Retries: `2`
- If Grafana needs login, point at a health/login endpoint that returns 200 without auth.

### 4. Email (SMTP) notification
Settings → Notifications → Setup Notification → Type = **Email (SMTP)**.
- Host / Port: Agoda internal SMTP relay (confirm the relay host + port with IT infra — many internal relays allow unauthenticated send from a known subnet on port 25).
- From: a sender like `keepalive-monitor@agoda.com`
- To: the IT distribution list / your inbox
- Send a **Test** to confirm it lands before relying on it.
- Then edit each monitor → enable this notification → it fires on Down and on Recovered.

### 5. Status page
- Status Pages → New → add all the monitors.
- Publish on the internal network; share the URL as the video wall health board.

---

### Verify it works
- Unplug a NUC's network (or stop Grafana) → confirm Uptime Kuma flips to Down after ~2 misses and an email arrives.
- Restore → confirm a Recovered email arrives.

---

### 6. Feed uptime into Grafana (optional — Phase 5)

Uptime Kuma can't push to Grafana directly; Prometheus sits in between and
Grafana reads from it.

**a. Get Uptime Kuma's metrics endpoint**
- Settings → API Keys → create one. Kuma exposes Prometheus-format metrics at:
  `http://<lxc-ip>:3001/metrics`
- It's protected with HTTP Basic auth: username blank, password = the API key.

**b. Stand up Prometheus** (new LXC, or alongside Kuma on OptiPlex #1). Scrape config:
```yaml
scrape_configs:
  - job_name: 'uptime-kuma'
    scrape_interval: 30s
    metrics_path: /metrics
    basic_auth:
      password: '<your-api-key>'   # username left blank
    static_configs:
      - targets: ['<lxc-ip>:3001']
```

**c. Wire into Grafana**
- In Grafana: Connections → add **Prometheus** datasource → URL `http://<prometheus-ip>:9090`.
- Build panels from Kuma's metrics (e.g. `monitor_status`, `monitor_response_time`).
- A known starting point: Grafana dashboard ID **18570** (community Uptime Kuma board) — import and adjust.
- Put these panels on the **same Grafana the video wall displays** so the wall shows its own health.

> This is visualization only. Email alerting (step 4) is the primary path and
> works independently of this.
