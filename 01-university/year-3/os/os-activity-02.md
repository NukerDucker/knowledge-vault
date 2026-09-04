---
title: OS Activity 02 — Synchronization I
tags:
  - university
  - os
  - individual
  - synchronization
status: submitted
created: 2026-08-30
due: 2026-09-04
subject: os
---

# OS Activity 02 — Synchronization I

> [!warning] Deadline
> September 4, 2026, 11:59 PM. **No code submission** — explain what you learned only.

## Assignment

- `Ex01.cs` — single-thread baseline
- `Ex02.cs` — 2-thread version derived from Ex01, **result is wrong**

Questions:
1. Why is Ex02.cs's result wrong?
2. Improve Ex02.cs with `lock` to get the correct result.

## Files

`~/Documents/University/Year-3/OS/Activity02/`
- `Ex01.cs` — single-thread: `plus()` sums 1..1,000,000 into static `sum`, then `minus()` subtracts 0..999,999 from it, sequentially. Correct result: `sum = 1000000` (`Σ1..N − Σ0..N-1 = N`).
- `Ex02.cs` — same `plus`/`minus`, but run as two `Thread`s (`P`, `M`) with `P.Start(); M.Start(); P.Join(); M.Join();`. Result is **wrong and non-deterministic** across runs.

*(No PDF for this activity — full spec is the goedu.kmitl.ac.th assignment text; `Ex03.cs` + its PDF are Activity 3, a continuation — see [[os-activity-03]])*

## Answer

### 1. Why wrong

Ex01.cs is correct because summing 1 through N then subtracting 0 through N-1 leaves N, and it runs sequentially so `sum = 1000000` every time.

`sum += i` compiles to read, add, write, three steps not one. Ex02.cs runs plus() and minus() as separate threads on the same static sum, so one thread's write can get overwritten by the other reading a stale value first, for example:

```
P reads sum = 100
M reads sum = 100   (stale, P has not written yet)
P writes 100 + 5 = 105
M writes 100 - 3 = 97   (P's +5 is lost)
```

That is a lost update, the textbook race condition. `Join()` waits for both threads to finish, but does nothing about what happens to sum before that, while they are both still writing to it. I actually ran Ex02.cs 5 times to check this, and got `1903975083` on the first try, then `-1461665461`, `1731981328`, `-1733168586`, and `-1322193061` on the next four. Not one of them was `1000000`, and no two were even close to each other.

### 2. Fix with `lock`

Wrap the read-modify-write in a shared lock so only one thread touches `sum` at a time:

```csharp
private static readonly object sumLock = new object();

static void plus() {
    for (int i = 1; i < 1000001; i++)
        lock (sumLock) { sum += i; }
}
static void minus() {
    for (int i = 0; i < 1000000; i++)
        lock (sumLock) { sum -= i; }
}
```

Result is now always `1000000`. Cost is lock contention, every iteration waits its turn. Locking the whole loop also works but removes all concurrency between the two threads. `Interlocked.Add` would be lighter, but activity asks for `lock`.

## Status

| Item | Status |
|---|---|
| Files downloaded | ✅ |
| Analysis written | ✅ |
| Submitted (explanation) | ✅ |

## Notes

---
*See also: [[os-case-study-2]] [[assignments-tracker]]*
