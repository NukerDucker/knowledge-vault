---
title: Home Network
tags: [homelab]
status: active
updated: 2026-10-11
---

# Home Network

Subnet `192.168.1.0/24`. Gateway `.1`.

## Core

| IP | Device | Notes |
|---|---|---|
| 192.168.1.1 | Huawei router | Gateway, DNS :53, web admin, dropbear SSH |
| 192.168.1.3 | Wavlink WL-WN586X3 (MediaTek Filogic), OpenWrt 24.10 | Dumb AP: static `.3`, DHCP server **off**, firewall zone lan accept, flow-offloading on, 802.11k/v roaming on. Note: radio0 country `TH`, radio1 `US` (mismatch) |
| 192.168.1.112 | Proxmox host `homehug` | Gigabyte board, Debian 13. Web UI https://192.168.1.112:8006. Root SSH key auth from Mac works |
| 192.168.1.111 | Nuker's Mac | en0, private Wi-Fi MAC (rotates) |

## Proxmox containers (all LXC on vmbr0, no QEMU VMs)

| CT | IP | Name | Service |
|---|---|---|---|
| 110 | .100 | alpine-dns | AdGuard Home (:80). Upstream → `127.0.0.1:5335` unbound (local recursive, DNSSEC). unbound crash-loop fixed 2026-10-11: `root.key` in root-owned dir, chown'd to `unbound` user. Cron watchdog (`*/5`) restarts unbound if down |
| 111 | .101 | nginxproxymanager | Reverse proxy, admin :81 |
| 100 | .200 | docker-media-stack | *arr stack, Debian 12; web ports proxied via NPM |
| 101 | .201 | jellyfin | Jellyfin :8096, Ubuntu 24.04 |
| 102 | .88 | ubuntu | Stopped. Gateway fixed 2026-10-11 (`gw` was `.100`, now `.1`) |

## Other devices

| IP | MAC vendor | Guess |
|---|---|---|
| .96 | iComm Semiconductor | WiFi device (cam/IoT) |
| .97 | Tuya Smart | smart device |
| .107 | FN-LINK | WiFi-module device |
| .109 | Tuya Smart | smart device |
| .114/.207 | Xiaomi | Xiaomi device(s) |
| .138 | Espressif | ESP32 |
| .181 | Apple | iPhone/iPad |
| .218 | Trolink | smart device |

MAC vendors for IoT = chip makers, not brands. Product unknown — no open ports.

## Open items

- [x] unbound crash-loop on CT 110 fixed (`root.key` perms) — 2026-10-11
- [x] `.3` inspected: already a correct dumb AP (2026-10-11)
- [x] LAN DNS → AdGuard live: Huawei DHCP primary `.100`, secondary `1.1.1.1` kept as resilience fallback (2026-10-11)
- [ ] Optional: unify `.3` radio country to `TH` (radio1 currently `US`)
- [ ] ID IoT devices .96/.97/.107/.109/.218
- [ ] Decide .3 OpenWrt role / config — needs LuCI creds
- [ ] .2 unused

## Access cheat sheet

- Proxmox: https://192.168.1.112:8006
- AdGuard: http://192.168.1.100
- NPM admin: http://192.168.1.101:81
- Jellyfin: http://192.168.1.201:8096
- Proxmox SSH: `ssh root@192.168.1.112`

---

Scanned 2026-10-11: ping-sweep + ARP + port probe. No nmap on Mac.

Incident 2026-10-11: short total-outbound blip (router DHCP-DNS save moment) wedged unbound → SERVFAIL + AdGuard fallback timeouts → whole-LAN DNS outage until `rc-service unbound restart`. Watchdog cron added to prevent recurrence. Secondary DNS `1.1.1.1` kept so a dead AdGuard degrades rather than kills connectivity.
