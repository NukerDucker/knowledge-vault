---
title: SysAdmin Assignment 02 — Basic Linux Server Config
tags: [assignment, kmitl]
status: active
updated: 2026-10-09
due: TBA
points: 15
subject: sysadmin
course: 01276521
---

# SysAdmin Assignment 02 — Basic Linux Server Config

> **2026-10-09 — merged into Assignment 03.** This assignment is no longer
> separately due; it is folded into A03, whose brief will be announced later.
> `due:` is `TBA` until that brief lands.

**Course:** 01276521 Practice of System Administration  
**Weight:** 15% of total score  
**Type:** Individual work  
**Machine:** VM prepared by instructor (Ubuntu Server 24.04 or 26.04 LTS)

## Schedule

Held in-class **2026-09-30**. Randomly assigned to one of 3 rounds:

| Round | Time | Duration |
|---|---|---|
| 1 | 09:30 | 30 min |
| 2 | 10:30 | 30 min |
| 3 | 11:30 | 30 min |

**Rules:** No communication with anyone except the instructor. Stop immediately when time is up or receive 0 points.

## Tasks & Marks

| # | Task | Points |
|---|---|---|
| 1 | SSH to the Linux server using the given private key | 3 |
| 2 | Configure an additional IP on the network interface | 3 |
| 3 | Install Apache HTTP server or Nginx (instructor assigns which) | 3 |
| 4 | Change Apache/Nginx port to **8008** | 3 |
| 5 | Find and kill a high CPU-consuming process | 3 |
| | **Total** | **15** |

## Prep Checklist

- [ ] Know how to SSH with a private key: `ssh -i key.pem user@host`
- [ ] Know how to add IP via netplan (`/etc/netplan/`) or `ip addr add`
- [ ] Know how to install Apache: `apt install apache2` / Nginx: `apt install nginx`
- [ ] Know how to change port in `/etc/apache2/ports.conf` + vhost, or `/etc/nginx/sites-available/default`
- [ ] Know how to find high-CPU process: `top`, `htop`, or `ps aux --sort=-%cpu | head`
- [ ] Know how to kill: `kill -9 <PID>`
