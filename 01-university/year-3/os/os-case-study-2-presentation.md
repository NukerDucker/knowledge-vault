---
title: OS Case Study 2 — Presentation Outline
tags:
  - university
  - os
  - group-work
  - synchronization
  - presentation
status: active
created: 2026-09-06
due: 2026-09-11
subject: os
---

# OS Case Study 2 — Presentation Outline

10-minute group presentation. ~6–8 slides.

---

## Slide 1 — Title

- OS Case Study 2: Thread-Safe FIFO Queue
- Group 5 members list
- Date: Sep 11, 2026

---

## Slide 2 — The Problem

- Baseline `TSBuffer`: 10-slot ring buffer, zero locking
- 2 producers (`th01` 1..50 @ 5ms, `th011` 100..150 @ 7ms)
- 3 consumers (`th02` × 3, 60 dequeues each @ 16ms)
- Race hazards:
  - Two producers write `Back`/`Count` unsynchronized → lost/overwritten slots
  - Three consumers read `Front`/`Count` unsynchronized → duplicate/skipped reads
  - No full/empty blocking → stale reads, overwrites

---

## Slide 3 — Empirical Evidence (What Goes Wrong)

| Metric | Baseline | Fixed |
|---|---|---|
| Items produced | 101 | 101 |
| Items consumed | 180 (never blocks) | 101 ✅ |
| Duplicates | 109–111 per run | 0 |
| FIFO order | ❌ garbage | ✅ |

---

## Slide 4 — The Fix: Design Decisions

Three decisions, each with a reason:

1. **`lock` + `Monitor.Wait/PulseAll`** — mutual exclusion covers whole method (acquire at entry, release at return)
2. **`while` not `if` around `Wait`** — Mesa semantics: woken thread must re-acquire lock; another thread may have consumed slot by then → must re-check predicate (textbook §5.4)
3. **`PulseAll` not `Pulse`** — C# `Monitor` has **one** wait-set for both producers and consumers; `Pulse` wakes one arbitrary waiter — if wrong role, wakeup is wasted → deadlock risk (textbook §5.5: *"always safe to use broadcast"*)

---

## Slide 5 — Key Code (EnQueue / DeQueueAndPrint)

```csharp
// EnQueue
lock (lockObj) {
    while (Count == BufferCapacity) {
        Console.WriteLine($"[Thread-{t}]:Queue full, waiting");
        Monitor.Wait(lockObj);
    }
    TSBuffer[Back] = item; Back = (Back + 1) % BufferCapacity; Count++;
    Monitor.PulseAll(lockObj);
}

// DeQueueAndPrint — print INSIDE lock → transcript is strict FIFO
lock (lockObj) {
    while (Count == 0) Monitor.Wait(lockObj);
    int x = TSBuffer[Front]; Front = (Front + 1) % BufferCapacity; Count--;
    Console.WriteLine($"j={x}, thread:{t}");
    Monitor.PulseAll(lockObj);
}
```

---

## Slide 6 — Variant Comparison

| Criterion | Napaul | Tony | Yu | **Final** |
|---|---|---|---|---|
| `readonly` lock | ✅ | ❌ | ❌ | ✅ |
| `while`+`Wait` | ✅ | ✅ | ✅ | ✅ |
| `PulseAll` | ✅ | ❌ Pulse | ✅ | ✅ |
| Print inside lock | ✅ | ❌ | ❌ | ✅ |
| Clean shutdown | ⚠️ bg kill | ✅ flag+Join | ✅ Join | ✅ flag+Join |

Final version takes best of each. `producersFinished` flag + `Join` consumers → clean exit.

---

## Slide 7 — Alternative Considered: Two Condition Variables

- Textbook §5.4.3/5.6.3 describes separate wait-queues for producers/consumers
- **Problem:** C# `Monitor` only exposes **one** wait-set per lock object → no direct equivalent
- Workaround (per-thread dummy locks in explicit FIFO queues) is correct but fragile — loses wakeups permanently if waiter throws before `Wait`
- At ~200 ops/sec (capped by fixed `Sleep` calls), `PulseAll` thundering-herd cost is unmeasurable
- **Decision: rejected.** `PulseAll` is idiomatic C# here, not a compromise.

---

## Slide 8 — Summary

- Root cause: no mutual exclusion + no blocking on full/empty
- Fix: `lock` + `while`+`Monitor.Wait` + `Monitor.PulseAll` + print inside critical section
- Every decision textbook-backed (osppv2.pdf §5.3–5.5)
- 0 duplicates, strict FIFO, clean shutdown — verified empirically

---

## Speaker Split (10 min)

| Slides | Topic | Time |
|---|---|---|
| 1–2 | Problem | 1.5 min |
| 3 | Evidence | 1 min |
| 4–5 | Design + code walkthrough | 3.5 min |
| 6 | Variant comparison | 2 min |
| 7–8 | Alternative + summary | 2 min |

---

*See also: [[os-case-study-2]] [[assignments-tracker]]*
