---
title: OS Case Study 2 — Synchronization
tags:
  - university
  - os
  - group-work
  - synchronization
status: active
created: 2026-08-30
due: 2026-09-11
points: 15%
subject: os
---

# OS Case Study 2 — Synchronization

> [!warning] Deadlines
> - **Submission:** September 11, 2026, 11:59 PM
> - **Presentation:** Next class, 10 min per group
> - **Attendance mandatory** — absent = 0 for 15% group work section

## Assignment

Study `Program.cs`, then modify it to turn the `TSBuffer` array into a **thread-safe FIFO queue**. Reference output: youtu.be/i-aouW0J-D4.

- **Must use:** basic sync primitives — `lock`, condition variables
- **Banned:** high-level thread-safe collections / built-in concurrency libs (`ConcurrentQueue`, `Channels`, etc.)
- **Forbidden to touch:** any line marked `//ห้ามแก้ไขหรือเปลี่ยนแปลงบรรทัดนี้` — the three `Thread.Sleep(...)` calls in `th01`, `th011`, `th02`
- **Requirements:**
  - No data entered into the queue may be lost
  - Output must be strict FIFO — no missing, no extra, no duplicate entries

### Baseline program shape (`Program.cs`)

`TSBuffer` is a 10-slot ring buffer (`Front`/`Back`/`Count`, no wraparound guard, no locking):

```csharp
static int[] TSBuffer = new int[10];
static int Front = 0, Back = 0, Count = 0;

static void EnQueue(int eq) { TSBuffer[Back] = eq; Back++; Back %= 10; Count += 1; }
static int DeQueue() { int x = TSBuffer[Front]; Front++; Front %= 10; Count -= 1; return x; }
```

Threads:
- `th01` — enqueues 1..50, `Sleep(5)` each (producer)
- `th011` — enqueues 100..150, `Sleep(7)` each (producer)
- `th02` × 3 (t2, t21, t22) — each dequeues 60 times, `Sleep(16)` each (3 consumers)

**Race hazards as given:** two producers writing `Back`/`Count` unsynchronized → lost/overwritten slots; three consumers reading `Front`/`Count` unsynchronized → duplicate/skipped reads; buffer has no full/empty blocking → consumers can read stale/garbage slots when queue is empty, producers can overwrite unread slots when full.

### Verified solution (NotebookLM research + Opus recheck)

Researched via NotebookLM (OS course notebook — Ganger's OS book §5.3–5.4 on shared objects and Mesa-semantics condition variables) and cross-checked with Opus. **Verdict: correct as designed.**

```csharp
static readonly object lockObj = new object();

static void EnQueue(int item)
{
    lock (lockObj)
    {
        while (Count == 10)
            Monitor.Wait(lockObj);          // block on full, don't spin

        TSBuffer[Back] = item;
        Back = (Back + 1) % 10;
        Count++;

        Monitor.PulseAll(lockObj);          // must be PulseAll, see below
    }
}

static int DeQueue()
{
    lock (lockObj)
    {
        while (Count == 0)
            Monitor.Wait(lockObj);          // block on empty, don't spin

        int x = TSBuffer[Front];
        Front = (Front + 1) % 10;
        Count--;

        Monitor.PulseAll(lockObj);
        return x;
    }
}
```

**Why this is correct, not just working:**
- **`while`, never `if`, around `Monitor.Wait`** — C#/.NET use Mesa semantics: a woken thread must re-acquire the lock before it resumes, and by then another thread may have already changed `Count`. Skipping the re-check race-conditions the buffer.
- **`PulseAll`, not `Pulse`** — C#'s `lock` monitor has exactly **one** wait queue shared by both producers and consumers. `Pulse` wakes one arbitrary waiter; if it wakes the wrong class (e.g. another producer while the queue is still full), that thread re-checks, finds its predicate still false, and goes back to sleep — the thread that could actually proceed stays parked. That's a livelock/deadlock risk, not a style choice. `PulseAll`'s thundering-herd cost is irrelevant here: throughput is capped by the 5/7/16 ms `Sleep`s (~200 ops/sec), so a handful of extra spurious wakeups costs nothing measurable.
- **Lock spans the whole method** — acquired first line, released last line (no lock acquired/released mid-method), so no inconsistent intermediate state is ever visible.
- **`Sleep` calls stay outside the lock** (in `th01`/`th011`/`th02`, wrapping the `EnQueue`/`DeQueue` calls) — moving them inside would serialize all 5 threads behind the slowest sleep, killing throughput, though it wouldn't deadlock (`Monitor.Wait` releases the lock while parked).

**One real gap Opus flagged — output ordering:** `DeQueue()` returns the value *after* releasing the lock, so `Console.WriteLine` in `th02` runs unsynchronized. Dequeue *order* is provably FIFO (protected by the lock), but the printed *transcript* isn't — two consumers can interleave their prints out of dequeue order. Since the assignment grades against a reference video (visible output), print **inside** the critical section: replace the bare `DeQueue()` call with a combined `DeQueueAndPrint(t)` that does `Console.WriteLine(...)` before leaving the `lock` block, if the printed order needs to match FIFO exactly. (Minor: replace hardcoded `10` with `TSBuffer.Length` — cosmetic only.)

### Empirically tested (dotnet 10, scratch harness, not the graded submission)

Ran both versions with `Join()`/instrumentation added on top (never touching the forbidden `Sleep` lines) to count produced vs. consumed items, duplicates, and per-stream FIFO order.

| Metric | Baseline (unsynced) | Fixed (`lock`+`while`+`PulseAll`) |
|---|---|---|
| Items produced | 101 (50 + 51, fixed by the loops) | 101 |
| Items consumed | 180 (3 × 60 — consumers never block) | 101, then **correctly blocks** |
| Duplicate values read | 109–111 per run (never zero, 3 runs) | 0 |
| Every consumed value actually produced | — (garbage reads) | ✅ true |
| FIFO order within each producer's stream | — (not meaningful, data is garbage) | ✅ true (both th01's 1..50 and th011's 100..150) |

**Important thing this surfaced: the workload itself is imbalanced.** `th01`+`th011` only ever produce 101 items total, but the 3×`th02` consumers each loop 60 times — 180 dequeue attempts. The **baseline "succeeds" only because it's broken**: since it never blocks, every over-read just returns duplicate/stale data instead of stopping, which is exactly the 109–111 duplicate count above. The **fixed version correctly blocks** on the remaining 79 dequeue calls once producers are done — it never "finishes" the full 180-iteration run, and that's expected, correct producer-consumer behavior (a consumer waiting for work that hasn't arrived yet is not a bug), not a defect to engineer around. Confirmed this is real and reproducible, not a fluke, by running each version 3× fresh.

**Practical implication for the demo:** don't expect the fixed program to print 180 lines and exit — it'll print 101 correct lines (in strict FIFO order) and then sit blocked waiting for more input that never comes, same as the original given `Program.cs` (which also never calls `Join()` or terminates cleanly either way). If the reference video shows fewer than 180 output lines or the program just idling at the end, this matches.

### Reference video output format (youtu.be/i-aouW0J-D4, extracted via ffmpeg frames)

```
...........[Thread-100]:Queue full, waiting...........    ← th01 blocked (prints each wakeup that still finds full)
...........[Thread-200]:Queue full, waiting...........    ← th011 blocked
j=<value>, thread:<1|2|3>                                 ← consumer dequeued; printed inside lock
...
j=50, thread:2
j=149, thread:1
j=150, thread:3
Press any key to exit...
```

Program exits cleanly — confirms consumers are background threads and Main drains queue before `ReadKey`.

### Changes made to Program.cs (2026-09-03)

Three diffs applied:

1. `EnQueue(int eq)` → `EnQueue(int eq, object t)` — adds threadId param; prints `Queue full, waiting` inside the `while` loop (inside the lock, so `Count` is authoritative).
2. `th01`/`th011` — `EnQueue(i, t)` (pass thread param through).
3. `Main` — consumers set `.IsBackground = true`; producers `.Join()`'d; drain `lock { while (Count > 0) Monitor.Wait }` after Join; then `Console.WriteLine("Press any key to exit..."); Console.ReadKey()`.

Removed: `DeQueue()` (dead code — `DeQueueAndPrint` subsumes it).

### Alternative considered, not adopted: two condition variables

Course text §5.4.3/§5.6.3 describes a "better" pattern: separate wait-queues for producers (`itemRemoved`) and consumers (`itemAdded`), so a single `Monitor.Pulse` wakes exactly the right role — no thundering herd, and (claimed) FIFO wakeup fairness. C# monitors only expose **one** wait-queue per lock object though, so a real implementation needs a workaround (per-thread dummy lock objects held in explicit FIFO queues, with manual `Monitor.Exit`/`Enter` balancing around each `Wait`).

**Verified as genuinely correct C#** (Opus: no missed-wakeup race, no deadlock) — but rejected for two reasons that hold up:
- **The FIFO-fairness claim is false.** .NET's `Monitor` isn't fair on reacquisition, so queue order decides who gets *pulsed*, not who gets the slot — a barging thread can win anyway.
- **Loses wakeups permanently on abandonment.** If a waiter throws/gets interrupted between queuing its dummy and calling `Wait`, that dummy sits in the queue; a later signaler pulses an object nobody's waiting on and the wakeup vanishes. `PulseAll` self-heals from this; targeted `Pulse` can't. It also breaks silently under the natural "reuse one dummy per thread instead of `new object()` each time" optimization.

At 5 threads capped ~200 ops/sec by the fixed `Sleep`s, the herd `PulseAll` wakes costs nothing measurable. C# having one wait-set per monitor means the two-CV pattern (trivial in Java's two-`Condition`/`ReentrantLock` or a `SemaphoreSlim` design — both banned here) has no direct equivalent; under these exact constraints, `PulseAll` isn't a compromise, it's the idiomatic answer. Worth citing in the presentation as "considered and rejected," not just unconsidered.

**Sources:**
- NotebookLM notebook "The Evolution and Fundamentals of Operating Systems" — [notebooklm.google.com/notebook/8284cfe4-738f-45d5-a105-a5554832f078](https://notebooklm.google.com/notebook/8284cfe4-738f-45d5-a105-a5554832f078) — queried against course-uploaded sources:
  - Ganger, *Operating Systems in Three Easy Pieces*–style course text (uploaded as source, cited as "osppv2.pdf" in-notebook) — §5.2 "Structuring Shared Objects", §5.3 "Case Study: Thread-Safe Bounded Queue" (circular buffer w/ `front`/`nextEmpty`/lock), §5.4 "Condition Variable Definition" + "Case Study: Blocking Bounded Queue" (the exact `BBQ::insert`/`BBQ::remove` pattern this fix mirrors, including the `while` mandate and Mesa-vs-Hoare semantics sidebar), §5.5 "always acquire lock at method start, release at return" rule, §5.7 uniprocessor queueing locks
  - `05-Synchronization-part1_v2.pdf` — course lecture slides, C# `lock`/`Monitor.Wait`/`Monitor.Pulse`/`PulseAll` syntax reference (single-wait-queue-per-monitor point)
  - Course-provided `CaseStudy02.pdf` + this session's `Program.cs` (added as notebook sources this session)
- Opus (claude-opus-5) recheck of the drafted solution — confirmed `while`+`PulseAll` correctness, flagged the print-ordering gap above; the Monitor.Wait/PulseAll code block was jointly derived from the NotebookLM answer and Opus's correctness pass, not copy-pasted verbatim from either.

## Files

`~/Documents/University/Year-3/OS/CaseStudy02/`
- `Program.cs` — starting point (Thread_safe_buffer class, namespace OS_Problem_02)
- `CaseStudy02.pdf` — spec (Thai + English)

## Submission

- One representative submits best `program.cs` + presentation file
- Peer + cross-group evaluation forms, same as CaseStudy01

## Variant Comparison (2026-09-05)

Four team solutions compared on: (a) locking, (b) Mesa `while` loop, (c) `PulseAll` not `Pulse`, (d) print inside lock for FIFO transcript, (e) clean shutdown.

| Criterion | Baseline | Napaul | Tony | Yu | **Final** |
|---|---|---|---|---|---|
| Lock object | ❌ none | ✅ `readonly` | ⚠️ not `readonly` | ⚠️ not `readonly` | ✅ `readonly` |
| `while` + `Monitor.Wait` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `PulseAll` (not `Pulse`) | ❌ | ✅ | ❌ `Pulse` | ✅ | ✅ |
| Print inside lock (FIFO transcript) | ❌ | ✅ `DeQueueAndPrint` | ❌ outside | ❌ outside | ✅ `DeQueueAndPrint` |
| Clean consumer shutdown | ❌ | ⚠️ background kill | ✅ `producersFinished` + `Join` | ✅ `Join` (hardcoded counts) | ✅ `producersFinished` + `Join` |
| No hardcoded sizes / counts | ❌ | ✅ `.Length` | ❌ hardcoded 10 | ⚠️ 34/34/33 | ✅ `BufferCapacity` |
| Termination tracking | ❌ | ❌ | ❌ | ✅ | ✅ |

### Per-variant notes

**Baseline** — no synchronisation → data races on `Front`/`Back`/`Count`; consumers never block → 109–111 duplicates per run.

**Napaul (`Program.cs`)** — pros: `readonly` lock, `while`+`PulseAll`, print inside lock (correct FIFO transcript). Con: consumers are background threads terminated by process exit rather than `Join`'d; relies on drain loop in Main, which can fail in edge-case schedules.

**Tony (`tony-Program.cs`)** — pros: `producersFinished` flag + `PulseAll` on exit + `Join` all consumers (cleanest shutdown). Cons: `Monitor.Pulse` not `PulseAll` (wrong-role wakeup risk → livelock/deadlock); print outside lock (transcript order not guaranteed); lock field not `readonly`.

**Yu (`yu-Program.cs`)** — pros: `Join` all consumers, thread termination order tracking. Cons: consumer loop hardcodes 34/34/33 items (breaks if producer ranges change); print outside lock; lock field not `readonly`.

### Super-version rationale (textbook citations)

Implemented in `Program.Final.cs`. Each design decision backed by osppv2.pdf (NotebookLM notebook `8284cfe4-738f-45d5-a105-a5554832f078`):

- **`while` around `Monitor.Wait`** — textbook §5.4 (Mesa semantics): *"wait must always be called from within a loop...the state variables might have changed — in fact, they are almost certain to have changed"*. Between PulseAll and when the woken thread re-acquires the lock, another thread may have consumed the slot; rechecking is mandatory.
- **`PulseAll` not `Pulse`** — textbook §5.5: *"broadcast is needed when...different threads are using the same condition variable to wait for different predicates"*. C# `Monitor` exposes one wait-set per lock object; producers and consumers both park there. `Pulse` wakes one arbitrary waiter — if it wakes the wrong role the wakeup is consumed and the thread that could proceed stays parked → deadlock. *"It is always safe to use broadcast."*
- **Lock at method entry, release at return** — textbook §5.5: *"Always acquire the lock at the beginning of a method and release it right before the return...compilers and processors never re-order instructions across lock operations"*.
- **Print inside critical section** — only way to guarantee printed transcript matches FIFO dequeue order. Trade-off: Console serialises threads briefly; acceptable because throughput is already capped by the fixed `Sleep` calls (~200 ops/sec).
- **`producersFinished` + `Join` consumers** — `readonly` lock field prevents accidental reassignment; flag written and read under the lock (no `volatile` needed — lock boundary is the memory barrier); `PulseAll` after setting flag ensures no consumer sleeps forever on an empty queue.

### Build isolation

All four `.cs` files declare `class Thread_safe_buffer` with a `Main`. Compile super version standalone:

```bash
csc Program.Final.cs -out:SuperCase.exe && mono SuperCase.exe   # macOS/Linux
csc Program.Final.cs -out:SuperCase.exe && .\SuperCase.exe      # Windows
```

Or with a `.csproj`: add `<Compile Remove="Program.cs" Remove="tony-Program.cs" Remove="yu-Program.cs" Remove="Program.Baseline.cs" />`.

## Status

| Item | Status |
|---|---|
| Files downloaded | ✅ |
| Solution designed + researched (NotebookLM + Opus) | ✅ |
| Solution empirically tested (dotnet 10 scratch harness) | ✅ |
| Program.cs modified | ✅ |
| Variant comparison written | ✅ |
| Program.Final.cs authored | ✅ |
| Presentation prepared | ✅ |
| Submitted | ⬜ |

## Group Members

1. 67011081 Aphichaphon Phatthanakun
2. 67011178 Napaul Intharasing
3. 67011214 Nuttawee Wachiratienchai
4. 67011717 Phyo Arkar Win
5. 67011736 Yu Yu Khaing

## Notes

---
*See also: [[os-case-study-1]] [[assignments-tracker]]*
