---
title: OS Case Study 1 — Multithreading
tags:
  - university
  - os
  - group-work
  - threads
status: submitted
created: 2026-08-08
due: 2026-08-14
points: 65%
subject: os
---

# OS Case Study 1 — Multithreading

*Session log → [[casestudy01-os/session-state]]*

> [!warning] Deadlines
> - **Peer eval form:** August 13, 2026, 11:59 PM (link expires)
> - **Submission:** August 14, 2026, 11:59 PM
> - **Presentation:** Next class (10 min per group)
> - **Attendance mandatory** — absent = 0 for 35% group work section

## Assignment

Speed up `Program.cs` using manual threads.

- Download `Program.cs` from CaseStudy01 folder in course portal
- **Banned:** `Parallel.For` and any built-in thread management commands
- Must create and manage threads manually (`new Thread(...)`)

### What the baseline code does

Loads `data.bin` (11M decimals), runs `Calculate1()` on each element 30 times, sums results. Currently single-threaded.

```csharp
// Baseline — single thread
Thread Th1 = new Thread(ThreadWork);
Th1.Start();
Th1.Join();
```

**Goal:** Divide work across multiple `Thread` instances to reduce elapsed ms.

> [!caution] Shared state hazard
> Naive approach: `result` and `index` are static → race conditions when adding threads. See `Program.Ref1.cs` for what NOT to do.
> **Better fix: partition the array** — each thread owns a non-overlapping slice `[start, end)` and accumulates into a local variable. No lock needed, no contention, correct result.

## Submission

- **One** representative submits: `program.cs` + presentation file
- Submit best version only

## Scoring (total = 35 + 20 + 45)

### A — Peer Evaluation within Group (35%)

Evaluated by your own group members.

| Criterion | Points |
|-----------|--------|
| Attendance at scheduled meetings | 10 |
| Punctuality | 10 |
| Participation (ideas, opinions, consistency) | 20 |
| Cooperation (assisting, taking responsibility) | 15 |
| Support for group members (explaining concepts) | 15 |
| Documentation (slides, scripts, docs) | 10 |
| Presentation (preparation, readiness, participation) | 20 |

> Missing peer eval → **0 pts** for this section + group work score halved.

### B — Group Work Evaluation (65% split 20/45)

Evaluated by classmates from **other groups** (30%) + instructor (70%) → weighted 20:45 of total.

| Criterion | Points |
|-----------|--------|
| Assumptions about the identified problem | 15 |
| Reasoning to support assumptions | 15 |
| Problem-solving approach (original solutions) | 10 |
| Perspectives / key points from presentation | 10 |
| Output matching problem requirements | 20 |
| Quality of presentation | 30 |

> Missing group evaluation of others → **0 pts** for this section.

**Final score split: A:B(peer):B(instructor) = 35:20:45**

## Evaluation Rules

- Must evaluate **every** member of own group (one form per member)
- Must evaluate **all** other groups' presentations
- Use **KMITL institutional email** to access forms
- Check confirmation email box — use link to verify/revise
- Deductions are **individual** — only the failing student is affected

## Status

| Item                                | Status |
| ----------------------------------- | ------ |
| Group formed                        | ✅      |
| Group registered                    | ✅      |
| Program.cs downloaded               | ✅      |
| Multithreading implemented          | ✅      |
| Benchmark measured                  | ✅      |
| Presentation prepared               | ✅      |
| program.cs submitted                | ⬜      |
| Peer eval (members) submitted       | ✅      |
| Group eval (other groups) submitted | ⬜      |

## Group Members

1. 67011081 Aphichaphon Phatthanakun
2. 67011178 Napaul Intharasing
3. 67011214 Nuttawee Wachiratienchai
4. 67011717 Phyo Arkar Win
5. 67011736 Yu Yu Khaing

## Implementation (2026-08-09)

**Code:** `~/Documents/University/Year-3/OS/CaseStudy01/`

- `Program.cs` — proper partitioned implementation (submit this)
- `Program.Ref1.cs` — naive race-condition version (reference/contrast only)

**Approach:** Partition `[0, 10_000_000)` into N equal slices. Each thread owns its slice exclusively — no lock, no race, correct result. Worker count via CLI arg, default `Environment.ProcessorCount`.

**Run:**
```bash
dotnet run -c Release -- <N>   # always Release for timing
```

### Benchmark (Apple Silicon arm64, Release)

| Workers | Time (ms) | Speedup | Efficiency |
|---------|-----------|---------|------------|
| 1 | 19144 | 1.00× | 100% |
| 2 | 9804 | 1.95× | 97% |
| 4 | 4857 | 3.94× | 98% |
| 8 | 3707 | 5.17× | 65% |
| 16 | 3376 | 5.67× | 35% |

Cliff at 8 workers: machine has 4 P-cores + 4 E-cores. E-cores weak on `decimal` compute. Best efficiency at 4 workers.

> [!important] Submission note
> Submit `Program.cs` only. The file uses `new Thread(...)` with manual `.Start()` / `.Join()` — no `Parallel.For`, rule-compliant.

## Notes

---
*See also: [[os-case-study-1-2]] [[assignments-tracker]]*
