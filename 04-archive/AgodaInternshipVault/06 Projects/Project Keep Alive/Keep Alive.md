> Related: [[WallKeeper]] | [[Uptime Kuma Setup]]

## Project Keep Alive

Monitoring for the Grafana video wall NUC machines. Detect when a NUC goes
offline or its Grafana dashboard freezes, alert IT by **email**, and show
overall health on a status board.

**Scope right now (intern phase):** monitoring + email alerting only. A human
responds to the alert. Automated recovery (power cycling) and root-cause
diagnostics are documented at the bottom as future phases — **not built yet**.

- **Devices:** 1–5 Windows NUCs (video wall, running MagicSign + Grafana in a browser)
- **Tool:** Uptime Kuma on a Proxmox LXC
- **Alert channel:** Email (SMTP)
- **Test bed:** 2× Dell OptiPlex (see below) — build & validate before touching the live wall
- **Status:** Planning → setup

---

### Test bed — 2× Dell OptiPlex

Two OptiPlex were handed over to prototype on. Build the whole pipeline here
first, on hardware that's safe to break, then point the finished setup at the
real NUCs (just add them as new monitors — no rebuild).

| Box | Role | What runs on it |
|---|---|---|
| **OptiPlex #1** | Monitoring host | Proxmox → Uptime Kuma LXC (+ optional Prometheus) |
| **OptiPlex #2** | Test target ("fake NUC") | Windows + browser on a Grafana page — the thing being monitored |

Two physical boxes is the more realistic rehearsal because the network path
between monitor and target is real. (Alternative: run everything on #1 with a
Windows test VM, keep #2 as spare — simpler, less realistic.)

**Test cases to rehearse on #2 before going live:**
- **Offline** — unplug #2's network → ping monitor flips to Down + email arrives.
- **Freeze** — kill the browser / block the Grafana URL while #2 stays pingable → the **HTTP monitor** catches it (ping wouldn't). This is the case that matters most for the wall.
- **Recovery** — restore → confirm the "Up" email arrives.

---

### The problem, in layers

The video wall NUCs don't just go offline — the browser-based Grafana dashboard
can **freeze while the machine is still powered on and pingable**. So "alive"
has more than one meaning, and monitoring has to catch both:

| Failure mode | Symptom | Caught by |
|---|---|---|
| NUC offline / crashed | No network response at all | Ping monitor |
| Dashboard frozen, machine still on | Pings fine, but Grafana page is dead | HTTP monitor |

A ping-only setup would miss the freeze case entirely — which is the *main*
symptom we're chasing. That's why both monitor types below matter.

> Note: a whole-machine hang (the suspected cause) can't be recovered from
> inside the box — see future phases. For now we only need to **see** it.

---

### Phase 1 — Monitoring host
- Provision one **Uptime Kuma LXC** on Proxmox (Debian, community helper script — direct install, no Docker needed at this scale).
- Ensure the container can reach the NUC subnet so ping monitors work.
- See [[Uptime Kuma Setup]] for step-by-step.

### Phase 2 — Monitors (per NUC)
- **Ping monitor @ 60s interval** — is the machine reachable. (1-hour intervals are too slow — a Friday-night freeze wouldn't be seen until Monday.)
- **HTTP(S) monitor** against the local Grafana/MagicSign URL — catches "pings fine but the dashboard is frozen."
- Label each monitor by physical location, e.g. `Video Wall — Floor 3`.

### Phase 3 — Email alerting
- Add an **SMTP (email)** notification in Uptime Kuma — see [[Uptime Kuma Setup]].
- Attach it to every monitor, on both **Down** and **Recovered (Up)**.
- Fire after **2 consecutive misses** (Retries = 2) so brief network blips don't spam the inbox.

### Phase 4 — Status board
- Publish Uptime Kuma's built-in **Status Page** on the internal network as IT's at-a-glance health view for the wall.

### Phase 5 — Feed uptime into Grafana (optional)
Since the wall already runs Grafana, we can surface its own health on it.
**Uptime Kuma can't push to Grafana directly** — Grafana only reads from a
datasource, so Prometheus goes in between:

```
Uptime Kuma  ──/metrics──►  Prometheus  ──datasource──►  Grafana
 (exposes Prometheus-                (scrapes &            (panels on the
  format metrics)                     stores)               existing wall)
```

- Uptime Kuma has a built-in `/metrics` endpoint (Prometheus format), behind an API key.
- Stand up Prometheus (another LXC, or alongside Kuma on OptiPlex #1) to scrape it.
- Add Prometheus as a Grafana datasource and build uptime panels — these can live on the **same Grafana the wall already displays**, so the wall shows its own status.
- See [[Uptime Kuma Setup]] for the metrics endpoint + scrape config.

> Email (Phase 3) is the primary alert path. This phase is for *visualization* —
> nice-to-have, and a good learning piece, but not required for alerting to work.

---

### Future phases (documented, NOT in scope yet)

- **Recovery — external power cycle.** A whole-machine freeze can't be fixed by
  a local script (the OS is hung) or by Wake-on-LAN (the NUC is still powered,
  not asleep). The only reliable fix is a **smart plug / networked PDU** per NUC
  plus BIOS set to "power on after power loss," triggered from a host-side script
  on a down event. Needs hardware budget + approval — revisit later.
- **Diagnostics — find the root cause.** Whole-NUC freezes usually trace to
  thermal (enclosed wall mounts overheat), memory exhaustion (browser leak), or
  GPU/display driver crashes. When ready: enable crash dumps, check Event Viewer
  after a freeze (clean shutdown vs hard hang), and log temp/RAM.
- **Prevention** is already partially handled by [[WallKeeper]] (biweekly restart).
