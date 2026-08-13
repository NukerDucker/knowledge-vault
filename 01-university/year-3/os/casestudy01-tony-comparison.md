# OS CaseStudy01 — Full Benchmark + Comparison

**Last updated:** 2026-08-12 (rerun with 3-run averages + original baseline + W=8)
**Groups:**
- **Napaul + Tony (same group)**
  - Napaul → `~/Documents/University/Year-3/OS/CaseStudy01/Program.cs`
  - Tony → `~/Documents/University/Year-3/OS/Tony-OS-Case-Study-01/Program.cs`
  - `original.txt` = single-thread starting template given to all groups
- **Cream Bun/Cheesy group** → Ref1 (race-condition, shared-state). Tested from job tmp.

---

## Algorithm — Calculate1

- Reads `data[idx]`, conditionally assigns `sum` via `(int)value[i] % N` (divisible by 2, 3, 5, 7, else)
- Mutates `data[idx] *= 0.1` in-place; increments `idx` by ref
- Result: `(long)sum % 2 == 0` → `Math.Round(sum * 0.5)` else `Math.Round(sum * -0.3)`
- **Why partition array, not iterations?** Iterations are serially dependent (pass N reads mutated data from pass N-1). Array slices are independent → safe to partition, zero locks needed.

---

## Workload parameters

| Parameter | Value |
|-----------|-------|
| Array allocated | 11,000,001 elements |
| Elements processed | **10,000,000** (`max_accessible_elements`) — last ~1M excluded by design |
| Passes | 30 |
| Total ops | **300M** (10M × 30) |
| Expected result | `4686980924312.00000000` |

---

## Hardware + build

| Field | Value |
|-------|-------|
| Chip | Apple M2 |
| Cores | 4 P-cores + 4 E-cores (8 logical) |
| RAM | 16 GB |
| OS | macOS 26.5.2 arm64 |
| .NET | 10.0.302 |
| Build | `dotnet run -c Release` |

---

## Benchmark results (3-run averages, Release, 2026-08-12)

### Original (single-thread starting template)

| Threads | Avg (ms) | Raw (ms) |
|---------|----------|----------|
| 1 | **19,198** | 18958, 19286, 19351 |

### Napaul

| Threads | Avg (ms) | Raw (ms) | Speedup vs original | Efficiency |
|---------|----------|----------|---------------------|------------|
| 1 | 19,382 | 19383, 20092, 18672 | ~1.00× | — |
| 2 | 9,567 | 9572, 9579, 9549 | 2.01× | 100% |
| 4 | 5,131 | 5183, 5055, 5154 | 3.74× | 94% |
| 8 | 4,204 | 4156, 4477, 3980 | **4.57×** | 57% |
| 16 | 4,321 | 4340, 4376, 4247 | 4.44× | 28% |

### Tony

| Threads | Avg (ms) | Raw (ms)            | Speedup vs original | Efficiency |
| ------- | -------- | ------------------- | ------------------- | ---------- |
| 1       | 19,754   | 19298, 19774, 20191 | ~1.00×              | —          |
| 2       | 9,831    | 10115, 9648, 9730   | 1.95×               | 98%        |
| 4       | 5,439    | 5320, 5430, 5566    | 3.53×               | 88%        |
| 8       | 3,888    | 3577, 3885, 4202    | **4.94×**           | 62%        |
| 16      | 4,375    | 4365, 4327, 4432    | 4.39×               | 27%        |

> Tony W=8 high variance (625ms spread) — thermal/scheduler luck, not code advantage. Same algorithm.

### Ref1 — Cream Bun/Cheesy (single run, race-condition)

| Workers | Time (ms) | Correct? |
|---------|-----------|----------|
| 1 | 19,379 | ✓ |
| 2 | 18,369 | ✗ (got 2,699,343,111,381) |
| 4 | 24,905 | ✗ (got 1,934,420,221,372) |
| 6 | HANG ∞ | — |
| 16 | HANG ∞ | — |

**Ref1 failure modes:**
- W=1: correct (no contention)
- W=2–4: threads race `index` + `result` → wrong value, slower than serial
- W=6+: threads reset `index=0` faster than any can advance past 10M → inner while never exits → hang

---

## Code differences (Napaul vs Tony)

| Aspect | Napaul | Tony |
|--------|--------|------|
| Worker count | CLI arg / `Environment.ProcessorCount` | Hardcoded `16` |
| Result validation | Compares vs expected, prints PASS/FAIL | None |
| Output precision | F8 | F2 |
| FileStream dispose | `using` ✓ | No `using` → resource leak |
| Unused imports | None | `System.Text.Json`, `CodeAnalysis`, dup `using System` |
| Unused param | None | `threadIndex` in `ThreadWork` never read |
| Build mode | `#if DEBUG` warning | None |
| Last thread boundary | Unified in `WorkerFunc` | Separate explicit line outside loop |

---

## Key conclusions

1. **W=2: 2.01×, 100% efficiency** — zero contention; partition = natural isolation
2. **W=4: 3.74×, 94%** — four P-cores fully saturated; efficiency sweet spot
3. **Cliff at W=8: 57% efficiency** — E-cores weak on `decimal` arithmetic (software fixed-point)
4. **W=16 regresses vs W=8** — slice too small; `Thread.Start()` + scheduler overhead visible
5. **Partition-over-slices only correct strategy** — iterations are serially dependent; slices are independent
6. **Cheesy: correctness failure** — wrong result W=2–4, infinite hang W=6+; not competitive

---

## Submission decision (2026-08-13)

**Submit: old static-slice implementation** — presentation slides already done with those numbers.
New optimized version documented below as "future improvement" for Q&A/discussion.

---

## How to improve the previous design (post-presentation analysis)

Discovered by analyzing `2026-os` group's implementation. Two optimizations derived from
Anderson & Dahlin textbook (course reference osppv2.pdf).

### Optimization 1 — Dynamic scheduling (§7.2.2)

**Problem:** Static equal slices give E-cores same work as P-cores. E-cores are ~31% as fast
(derived from W=4 vs W=8 benchmark data: 23.7/76.3 = 0.31). P-cores finish early and sit idle.

**Fix:** Atomic work counter. Workers claim small slices via `Interlocked.Add`.
Fast cores claim more slices automatically.

**E-core speed derivation:**
- 4 P-cores alone: 4857ms (W=4 benchmark)
- 8 workers (4P+4E), equal slices: 3707ms
- P-cores did 3707/4857 = 76.3% of work → E-cores did 23.7%
- Per-core ratio = 23.7/76.3 = **0.31×** (E-core is ~31% speed of P-core)

### Optimization 2 — Near-zero early exit

**Problem:** Calculate1 does `value[i] *= 0.1` each call. After ~2 calls most values
decay below 5 → Calculate1 returns 0. Rounds 3–30 add nothing. Original runs all 30.

**Fix:** Invert loop (value-outer, rounds-inner). Break when `|data[i]| < 5`.
Safe: Calculate1 only touches `data[i]` — per-element independent.

**Speedup math:**
- Old: 30 × 10M = 300M calls
- New: ~2 × 10M = 20M calls → 15× fewer (theoretical)
- Actual 1T: 19,144ms → 5,663ms = **3.38×** (memory overhead is now bottleneck)

### Combined benchmark (M2 Air, Release, 2026-08-13)

| Workers | Old (ms) | New (ms) | Speedup vs old 1T |
|---------|----------|----------|--------------------|
| 1 | 19,144 | 5,663 | 3.38× |
| 2 | 9,567 | 3,106 | 6.16× |
| 4 | 5,131 | 1,652 | 11.59× |
| 8 | 4,204 | 1,264 | 15.14× |

Result correct: `4686980924312.00` ✓ on all counts.
Committed: `github.com/NukerDucker/os-case-study-1` → `93de84d`

---

## Pending

- Cream Bun's group: cross-device bar chart (4-core machine)
- Command: `for n in 1 2 4 6 16; do dotnet run -c Release -- $n; done`
