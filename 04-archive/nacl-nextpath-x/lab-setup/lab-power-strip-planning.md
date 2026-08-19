# Lab Power Strip Planning

## Context

- **Location:** Lab room
- **Total desks:** 32
- **Layout:** 1 power strip per 2 desks
- **Primary use:** Laptops (docked) + monitors; few desktop PCs
- **Thailand mains:** 220V / 50Hz / 15A per circuit → max ~3,300W per circuit

---

## Desk Type Power Estimates

| Desk Type | Devices | Estimated Load |
|-----------|---------|---------------|
| Laptop docked (no ext monitor) | Charger 65W | ~70W |
| Laptop docked + 1 monitor | Charger 65W + Monitor 30W | ~100W |
| Laptop docked + 2 monitors | Charger 65W + 2× Monitor 30W + Hub 10W | ~140W |
| Desktop + 2 monitors | PC 200W + 2× Monitor 30W | ~270W |

> Worst-case per desk = **~140W** (laptop docked config). Desktop desks ~270W.

---

## Load Per Strip (2 Desks)

| Strip Scenario | Load Estimate | % of 2300W Strip |
|---------------|---------------|-----------------|
| 2× laptop docked + 2 monitors | 280W | 12% |
| 1× laptop + 1× desktop | 410W | 18% |
| 2× desktop + 2 monitors | 540W | 23% |

All well within a standard 10A/2300W strip. **No overload risk at desk level.**

---

## Layout Map (601 Network and Cloud Laboratory)

![[601-lab-layout.png]]


Each wall outlet has **2 plug slots**. Orange dots = **network switch dedicated outlet only**.

### Wiring topology per row

**Top row (desks 1–10) — direct:**
- Desk strip plugs directly into north wall outlet (2 plug slots = 2 desks)
- 1 outlet → 2 desk strips → 2 desks
- Outlets needed: 5

**Middle row (desks 11–22) — extended:**
- 1 floor panel outlet (16A, 2 plug slots) → 2 large extension strips (1 per plug slot)
- Each large strip → 3 small desk strips (2 desks each) → 6 desks per big strip
- 1 outlet → 2 big strips → 6 small strips → 12 desks
- Outlets needed: 1

> ⚠️ All 12 middle desks on 1 outlet. Worst case ~1,680W (12 × 140W) — within 15A limit but leaves little headroom. Confirm circuit is dedicated to middle row only.

**Bottom row (desks 23–32) — direct:**
- Same as top row, desk strip plugs directly into wall outlet
- 1 outlet → 2 desk strips → 2 desks
- Outlets needed: 5

**Network switches (orange dots — not desk power):**
- Desk 11 cluster: dedicated outlet → switch → blue cable run → RACK
- Desk 23 cluster: dedicated outlet → switch → right wall
- Outlets needed: 2

| Row | Desks | Desk strips | Wall outlets used | Topology |
|-----|-------|-------------|------------------|----------|
| Top | 1–10 | 5 | 5 | Direct |
| Middle | 11–22 | 6 small + 2 large | 1 | Outlet → 2 big strips → 6 small strips → 12 desks |
| Bottom | 23–32 | 5 | 5 | Direct |
| Switches | — | — | 2 | Dedicated |
| **Total** | **32** | **16 small + 2 large** | **13** | |

---

## Zone Breakdown

### Desks (32 total)

Adjust laptop/desktop count to match actual mix:

| Parameter | Value |
|-----------|-------|
| Total desks | 32 |
| Laptop desks (estimate) | 28 |
| Desktop desks (estimate) | 4 |
| Strips needed (1 per 2 desks) | **16 strips** |
| Recommended cord length | 3m (floor outlet to strip under desk) |
| Outlets needed per strip | Min 4 (2 chargers + 2 monitors) → use **5-outlet** |
| Individual switch per outlet | **Required** |
| Surge protection | **Required** (equipment-heavy lab) |

**→ Product: PlugThai E-02L (5 outlets, individual switches, surge protection, 3m cord)**
Qty: **16 units**

---

### Rack / Server Area

| Parameter | Value |
|-----------|-------|
| Typical devices | Switch, router, NAS, patch panel PSU, UPS |
| Amperage needed | 16A minimum (allow headroom) |
| Form factor | 1U rack-mount PDU preferred |
| Cord type | Without cord (hardwired to PDU input) |

**PDU: already installed. No additional unit needed.**
→ Need to add **UPS** after PDU for rack protection.

---

### Common Area / Shared Tables

| Parameter | Value |
|-----------|-------|
| Devices | Phone chargers, laptop top-up, general |
| Outlets needed | 4 |
| Special requirement | None (dry area) |

**→ Product: PlugThai E-02L 3m or any 4-outlet strip**
Qty: **2 units**

---

### Pantry / Fridge Area

| Parameter | Value |
|-----------|-------|
| Devices | Fridge, kettle, microwave |
| Load estimate | Fridge 150W + Kettle 1500W + Microwave 1000W |
| Special requirement | **Waterproof/splash-proof** (near sink) |
| Surge protection | Optional (fridge prefers dedicated outlet) |

> ⚠️ Fridge ideally on its own wall outlet — motor start surge causes trips on shared strips.

**→ Product: Nano rubber block waterproof 4-outlet (Shopee)**
Qty: **1 unit**

---

## Product Recommendation Summary

| Zone | Product | Why | Qty |
|------|---------|-----|-----|
| Desks | PlugThai E-02L 5-outlet, 3m | Individual switches + surge + slim | 16 |
| Rack | UPS (rack-mount) | PDU already installed; UPS still needed | 1 |
| Common area | PlugThai E-02L 3m or similar | Standard, surge | 2 |
| Pantry/fridge | Nano rubber waterproof block | Splash protection | 1 |

---

## Circuit Load Sanity Check

Thailand standard circuit: **15A / 220V = 3,300W max** (safe working load ~2,600W at 80%)

| Zone | Est. total load | Notes |
|------|----------------|-------|
| 16 desk strips × 280W avg | ~4,480W | Needs **2+ circuits** for desk area |
| Rack | ~500–800W | Separate dedicated circuit |
| Common area | ~200W | Can share |
| Pantry | ~1,800W (kettle peak) | Dedicated circuit recommended |

> ⚠️ Do not run all 16 desk strips on a single 15A circuit. Plan for at least **2 circuits** serving desks (8 strips each ≈ 2,240W peak).

---

## Shopping List

| Item                  | Spec                               | Qty | Cord | Status |
| --------------------- | ---------------------------------- | --- | ---- | ------ |
| PlugThai E-02L        | 5-outlet, individual switch, surge | 18  | 3m   | ☐      |
| UPS rack-mount        | Size TBD (rack load ~500–800W)     | 1   | —    | ☐      |
| Nano waterproof block | 4-outlet, 4000W                    | 1   | VCT  | ☐      |

---

## Open Questions

- [ ] How many circuits available at panel for desk area?
- [ ] Exact laptop/desktop desk count confirmed?
- [ ] UPS size — confirm rack load inventory to spec VA/W rating
- [x] Floor panel: 16A, 2 plug slots ✓
- [x] No standing desks ✓
- [x] Rack PDU already installed ✓
- [x] UPS needed — still to buy ✓
