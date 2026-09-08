---
title: NaCL CE Cloud Infrastructure Planning
tags: [nacl, networking, cloudstack, infrastructure, mikrotik, dgx]
status: active
updated: 2026-09-06
---

# NaCL CE Cloud Infrastructure Planning

Meeting/chat log summary from 2026-09-06.

## Team Structure

- **Core team** — hands-on, network-competent; handles tasks 1–5
- **Observers** — join inventory review + design review; one-time physical hardware access; handle docs and onboarding (tasks 6–7)
- Communication overhead concern → keep core team small

## High-Level Task List

1. Gather and organize physical/logical config → item inventory + diagrams
2. Review inventory and design → architecture decisions
3. Re-wire and configure network devices
4. Install and configure OS + essential services (DNS, NTP, Syslog, NFS, etc.)
5. Install and configure CloudStack core services
6. Integration and system tests → admin guide / troubleshooting docs *(observers assist)*
7. Onboarding → user guides / tutorials *(observers handle)*

**Target:** System ready ~6–7 Dec (1 week after Sem 2 opens 30 Nov)  
**Bottleneck:** Tasks 1–2 must finish within 2 weeks; network design finalization is the risk.

## Proposed Network Zones (5 logical zones)

1. Internet
2. KMITL internal network
3. **CE core network** — common services: DNS, IAM, VPN, web proxy, monitoring, logging
4. **CE Cloud** — CloudStack
5. **AI infrastructure** — NVIDIA DGX B200

> Workstation (5090) placement: TBD

## Key Technical Decisions

### DGX Dependency

- DGX currently shares MikroTik CCR2004 in CE Cloud rack for NAT
- **Decision:** Reconfigure MikroTik so DGX existing network stays untouched → CE Cloud scope stays clean
- After reconfigure: นัท (DGX users) must verify DGX still works
- Avoids need to touch DGX internals or negotiate with G-able (Extreme Networks 7520 access uncertain)

### VPN

- Must be **centralized in CE core** — not per-subsystem
- Avoids per-subsystem access fragmentation as new systems are added

### Routers

| Router | Spec | Role |
|---|---|---|
| CCR2116-12G-4S+ | SFP+ only | CE core — VPN, routing (new, arriving soon) |
| CCR2004 | Has SFP28 | High-speed links; stays with workloads needing SFP28 |

CCR2116 model confirmed as `CCR2116-12G-4S+` (not the higher-spec CCR2216).

### Network Switches

- **Dell switches** — Cisco-like CLI; learnable; no urgency to add people
- **Extreme Networks 7520** — came with DGX project; L3 switch; capabilities not yet reviewed; G-able may restrict access

## Open Issues

- [ ] Confirm: does DGX currently use CE Cloud MikroTik for NAT? (determines scope)
- [ ] Get อ.จิระศักดิ์ to call final network design decisions — he is key approver
- [ ] Verify Extreme Networks 7520 access with นัท
- [ ] Confirm CCR2116 arrival date
- [ ] Determine where RTW workstations (5090) sit in zone topology
- [ ] Security policy: subnet/VLAN layout OK to share internally; software versions more sensitive
