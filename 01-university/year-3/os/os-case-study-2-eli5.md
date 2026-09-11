---
title: OS Case Study 2 — ELI5 Explanation
tags:
  - university
  - os
  - synchronization
  - reference
status: reference
created: 2026-09-11
subject: os
---

# OS Case Study 2 — ELI5 Explanation

> Full breakdown of the thread-safe bounded buffer problem. See [[os-case-study-2]] for the solution code and variant comparison.

---

## The Problem in One Sentence

Five threads share one array. Two threads write into it, three threads read from it — at the same time — with no coordination. Everything breaks.

---

## The Analogy

Conveyor belt sushi restaurant (10 plates max on the belt):
- **2 chefs** (producers `th01`, `th011`) — keep putting plates on
- **3 customers** (consumers `th02` × 3) — keep taking plates off
- **No rules** → chefs put a plate where one already sits (overwrite), customers grab the same plate simultaneously (duplicate), customers grab empty space (garbage)

The assignment: add rules so plates move correctly.

---

## The Baseline Code (Broken)

```csharp
static int[] TSBuffer = new int[10];   // the belt — 10 slots
static int Front = 0, Back = 0, Count = 0;

static void EnQueue(int eq) {
    TSBuffer[Back] = eq;
    Back++;
    Back %= 10;            // wrap around (ring buffer)
    Count += 1;
}

static int DeQueue() {
    int x = TSBuffer[Front];
    Front++;
    Front %= 10;
    Count -= 1;
    return x;
}
```

### Variables

| Variable | Role |
|---|---|
| `TSBuffer[10]` | Ring buffer — 10-slot array |
| `Front` | Index of next item to read |
| `Back` | Index of next empty slot to write |
| `Count` | Items currently in buffer |

### Threads

| Thread | What it does | Sleep |
|---|---|---|
| `th01` | Enqueues 1–50 | 5ms each |
| `th011` | Enqueues 100–150 | 7ms each |
| `th02` (×3) | Each dequeues 60 times | 16ms each |

### Why it breaks

`Count++` is **not atomic** — three CPU instructions: read → add → write:

```
Thread A reads Count=5
Thread B reads Count=5       ← both see same value
Thread A writes Count=6
Thread B writes Count=6      ← B's write wins; A's increment lost
```

Result: lost writes, duplicate reads, garbage values — **data race**.

---

## The Fix: Lock + Monitor

### Core idea

Only **one thread** touches the buffer at a time. `lock` wraps `Monitor.Enter` / `Monitor.Exit`.

```csharp
static readonly object lockObj = new object();
```

`lockObj` is a token. Whoever holds it has exclusive access. Everyone else waits.

---

## EnQueue — Fixed

```csharp
static void EnQueue(int item)
{
    lock (lockObj)                          // grab token
    {
        while (Count == 10)                 // belt full?
            Monitor.Wait(lockObj);          //   release token, sleep

        TSBuffer[Back] = item;
        Back = (Back + 1) % 10;
        Count++;

        Monitor.PulseAll(lockObj);          // wake all waiters
    }                                       // release token
}
```

Steps:
1. Grab lock — exclusive access
2. If full → release lock and sleep (`Monitor.Wait`)
3. On wake → re-check condition (`while`)
4. Write item, advance `Back`, increment `Count`
5. Wake all sleeping threads (`PulseAll`)
6. Release lock

---

## DeQueue — Fixed

```csharp
static int DeQueue()
{
    lock (lockObj)
    {
        while (Count == 0)
            Monitor.Wait(lockObj);

        int x = TSBuffer[Front];
        Front = (Front + 1) % 10;
        Count--;

        Monitor.PulseAll(lockObj);
        return x;
    }
}
```

Same pattern — sleep if empty, wake all after taking.

---

## The Three Critical Decisions

### 1. `while` not `if`

```csharp
// WRONG:
if (Count == 0) Monitor.Wait(lockObj);

// RIGHT:
while (Count == 0) Monitor.Wait(lockObj);
```

C# uses **Mesa semantics**: when `Monitor.Wait` returns, thread re-competes for the lock. By the time it wins, another thread may have already consumed the item.

```
Consumer A wakes (Count was 1)
Consumer B wins lock first, takes item → Count=0
Consumer A gets lock — Count is 0 again → reads garbage without while
```

`if` skips re-check → bug. `while` re-checks → correct.

**Rule: always `while` around `Monitor.Wait`.**

---

### 2. `PulseAll` not `Pulse`

C# `Monitor` has **one** waiting room for both producers AND consumers. `Pulse` wakes **one random** sleeper.

```
Buffer has space. Pulse wakes a producer (also waiting).
Producer rechecks → still no space (just consumed) → sleeps again.
Consumer who could proceed: still sleeping → deadlock.
```

`PulseAll` wakes everyone. Each re-checks its own condition. The one that can proceed does; rest sleep again.

Cost: a few extra wakeups. Irrelevant — sleep timers (5/7/16ms) cap throughput at ~200 ops/sec. Thundering herd cost: immeasurable.

**Rule: one wait-set = must use `PulseAll`.**

---

### 3. Lock spans the whole method

Acquire on entry, release on exit. No other thread ever sees a half-modified buffer.

---

## Clean Shutdown

```csharp
static int ProducersRemaining = 2;
static bool AllDone = false;

static void SignalProducerDone()
{
    lock (locker)
    {
        ProducersRemaining--;
        if (ProducersRemaining == 0)
        {
            AllDone = true;
            Monitor.PulseAll(locker);
        }
    }
}
```

Problem: consumers loop 60× each but only 101 items are produced. 79 remaining dequeue calls would block forever.

Fix: when both producers finish, set `AllDone = true`, wake consumers. `DeQueue` returns `-1` sentinel:

```csharp
while (Count == 0 && !AllDone) Monitor.Wait(locker);
if (Count == 0 && AllDone) return -1;
```

Consumer sees `-1` → breaks loop → thread exits → `Join()` unblocks → program ends.

---

## Print Inside the Lock (FIFO Transcript)

```csharp
lock (locker)
{
    int j = DeQueue();
    if (j == -1) break;
    Console.WriteLine("j={0}, thread:{1}", j, t);  // inside lock
}
Thread.Sleep(16);
```

Without outer lock: consumer A dequeues `5`, consumer B dequeues `6`, B prints first → output `6` before `5`. Violates FIFO.

With outer lock: dequeue+print is one atomic operation → output order = dequeue order = FIFO. ✅

C# `lock` is **reentrant** — same thread re-enters same lock without deadlock. `DeQueue()` calling `lock(locker)` inside `th02`'s `lock(locker)` just increments recursion count. `Monitor.Wait` inside releases all levels.

---

## Concepts Employed

| Concept | What it is | Where used |
|---|---|---|
| **Mutual exclusion** | One thread in critical section at a time | `lock(lockObj)` |
| **Condition variable** | Sleep until condition changes | `Monitor.Wait` / `PulseAll` |
| **Mesa semantics** | Woken threads re-compete for lock | Reason for `while` loop |
| **Ring buffer** | Fixed array used as circular queue | `Back %= 10`, `Front %= 10` |
| **Producer-consumer pattern** | Classic sync problem | Entire assignment |
| **Bounded buffer** | Queue with max capacity | `Count == 10` check |
| **Sentinel value** | Signal "no more data" | `-1` from `DeQueue` |
| **Reentrant lock** | Same thread re-enters own lock | Outer lock + `DeQueue` inner lock |

---

## Efficiency

**Bottleneck:** `Thread.Sleep` calls, not the lock. Lock contention ~1μs; sleep ~15.6ms (Windows rounds to 64Hz scheduler quantum). Sync overhead < 0.01% of total time.

**`PulseAll` cost:** wakes ≤4 threads per op. Each does a condition check. At 200 ops/sec → 800 spurious wakeups/sec × ~1μs = 0.08% CPU. Negligible.

**Memory:** fixed 10-slot O(1) enqueue/dequeue.

---

## Where This Pattern Is Useful

- **Download manager:** network thread downloads chunks → UI thread shows progress
- **Log system:** app threads write logs → flush thread writes to disk
- **Video player:** decoder produces frames → renderer consumes them
- **Web server:** listener receives connections → worker pool processes them

Any "producer faster or slower than consumer" scenario.

---

## Alternatives Rejected

### Two condition variables (textbook §5.4.3/§5.6.3)

```
itemAdded  → signal consumers only
itemRemoved → signal producers only
```

Cleaner on paper. C# `Monitor` has one wait-set per lock — no built-in two-CV equivalent. Workaround (per-thread dummy locks) loses wakeups if waiter throws before `Wait`. Rejected.

### `ConcurrentQueue<T>` / `SemaphoreSlim`

Banned. Solves it in 5 lines. Assignment requires manual primitives.

### Spin-wait

```csharp
while (Count == 0) { /* spin */ }
```

Burns CPU at 100% waiting for a condition that changes on 16ms timescales. Never in production.

---

## Summary

Two producers and three consumers share a 10-slot ring buffer. Without coordination, data races on `Front`, `Back`, `Count` corrupt everything. Fix: `lock(lockObj)` for mutual exclusion; `Monitor.Wait` to sleep (not spin) when full/empty; `while` loop to re-check after wake (Mesa semantics); `PulseAll` because producers and consumers share one wait-set; shutdown flag so consumers exit cleanly; print inside the lock for FIFO transcript. Result: no lost data, no duplicates, no garbage reads, clean exit.

---

*See also: [[os-case-study-2]] [[os-case-study-2-presentation]]*
