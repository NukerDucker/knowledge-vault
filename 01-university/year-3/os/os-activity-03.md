---
title: OS Activity 03 — Synchronization II
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

# OS Activity 03 — Synchronization II

Continuation of [[os-activity-02]]. `Ex03.cs` builds on the Ex01/Ex02 pair. This one **is** submitted — the PDF spec ended up filed under Activity02's downloads by mistake (course portal naming), moved here since it's Ex03's spec.

## Baseline (`Ex03.cs`)

Two threads share `x` (string) and `exitflag` (int), no synchronization:

```csharp
static void ThReadX(object i) {
    while (exitflag == 0)
        Console.WriteLine("Thread-{0} : X = {1}", i, x);   // busy-spins, prints constantly
}
static void ThWriteX() {
    while (exitflag == 0) {
        Console.Write("Input: ");
        var xx = Console.ReadLine();
        if (xx == "exit") exitflag = 1; else x = xx;
    }
}
```

`ThReadX` busy-loops printing `x` as fast as possible — floods the console instead of printing once per input.

## Verified against official spec (`Activity02-1.pdf`, downloaded 2026-09-03)

Confirmed R-01/R-02 wording and screenshots match this note exactly.

**Bug found on recheck:** original Q01/Q02 code only pulsed *readers* — the writer
(`ThWriteX`) never waited for a value to be consumed before overwriting it. Under
piped/fast input (no human typing delay) this drops values: writer races ahead,
overwrites `x`/`hasNewValue` before any reader wakes up, previous value lost.
Reproduced with piped R-02 input: `4` and `7` silently dropped (7/9 values printed).

**Fix:** writer blocks on `hasNewValue` until the reader drains it; reader calls
`Monitor.PulseAll` after consuming (not just on exit) to wake the writer:

```csharp
// writer, before setting a new value
lock (gate) {
    while (hasNewValue) Monitor.Wait(gate);
    if (xx == "exit") { exitflag = 1; Monitor.PulseAll(gate); }
    else { x = xx; hasNewValue = true; Monitor.Pulse(gate); }
}

// reader, after consuming
Console.WriteLine(...);
hasNewValue = false;
Monitor.PulseAll(gate);   // wake writer waiting on hasNewValue == false
```

Applied to both `Ex03_Q01.cs` and `Ex03_Q02.cs`. Stress-tested 10 runs each with
piped R-01/R-02 input after the fix: 11/11 and 9/9 values every run, zero drops,
zero hangs. (First naive attempt at the writer-side fix only touched the writer
side and missed the reader-side `PulseAll` — that left the writer able to
deadlock, waiting forever with no one to wake it; caught by a 10-run stress test
under `timeout`, not by a single manual run.)

## Q01 — enhance with `lock` → match R-01

**Target (R-01):** exactly one `X = <value>` line per `Input:` line, single reader thread (id 1), ends with `Thread 1 exit`.

Need `ThReadX` to *block* until new input arrives instead of spinning — `lock` alone can't block-and-wait, need `Monitor.Wait`/`Monitor.Pulse` on the lock object:

```csharp
private static readonly object gate = new object();
private static bool hasNewValue = false;

static void ThReadX(object i) {
    lock (gate) {
        while (true) {
            while (!hasNewValue && exitflag == 0) Monitor.Wait(gate);
            if (hasNewValue) {
                Console.WriteLine("X = {0}", x);
                hasNewValue = false;
                Monitor.PulseAll(gate);   // wake writer waiting to send next value
            }
            if (exitflag == 1) break;
        }
    }
    Console.WriteLine("Thread {0} exit", i);
}

static void ThWriteX() {
    while (exitflag == 0) {
        Console.Write("Input: ");
        var xx = Console.ReadLine();
        lock (gate) {
            while (hasNewValue) Monitor.Wait(gate);   // don't overwrite an unread value
            if (xx == "exit") { exitflag = 1; Monitor.PulseAll(gate); }
            else { x = xx; hasNewValue = true; Monitor.Pulse(gate); }
        }
    }
}
```

## Q02 — extend Q01 → match R-02

**Target (R-02):** 3 reader threads (ids 1, 2, 3), labeled `***Thread N : x = value***`, only **one** thread wakes per input (`Monitor.Pulse`, not `PulseAll`, on the value-ready path) — matches R-02's output where each input is consumed by exactly one thread, round-robin-ish depending on scheduler. On `exit`, `PulseAll` so **all three** print `---Thread N exit---`, even threads that never got a chance to consume a value (Thread 2 in R-02 exits without ever printing).

```csharp
static void Main() {
    Thread A1 = new Thread(ThReadX);
    Thread A2 = new Thread(ThReadX);
    Thread A3 = new Thread(ThReadX);
    Thread B  = new Thread(ThWriteX);
    A1.Start(1); A2.Start(2); A3.Start(3);
    B.Start();
}
```

`ThReadX` prints `***Thread {0} : x = {1}***` / `---Thread {0} exit---` instead of Q01's plain format; `ThWriteX` identical to Q01 (including the writer-waits-on-`hasNewValue` fix above).

## Files

`~/Documents/University/Year-3/OS/Activity03/`
- `Ex03.cs` — baseline (unsynchronized)
- `Activity02.pdf` — spec (Q01/Q02 + R-01/R-02 expected console output)

## Status

| Item | Status |
|---|---|
| Files organized | ✅ |
| Q01 (lock, single reader) | ✅ |
| Q02 (3 readers, Pulse/PulseAll) | ✅ |
| Submitted | ✅ |

## Notes

Same due date as Activity02, opened 2026-08-27. Unlike Activity02 (explain-only), this one has concrete expected outputs (R-01/R-02) — confirmed against `Activity02.pdf` spec (Q01/Q02 wording, R-01/R-02 screenshots match this note's design exactly). Submission platform: goedu.kmitl.ac.th (not Moodle). Likely requires submitting the modified code.

Built and ran both as real dotnet console apps at `~/Documents/University/Year-3/OS/Activity03/Ex03_Q01.cs` and `Ex03_Q02.cs`. Found and fixed one bug during testing: original design checked `exitflag` before printing a pending value, so a value written right before `exit` could get silently dropped. Fixed by draining `hasNewValue` first, then checking `exitflag` (code above already updated). Confirmed Q02's Pulse/PulseAll split works: `Monitor.Pulse` wakes exactly one reader per value, `Monitor.PulseAll` on exit wakes all three so a reader that never got a turn still prints its exit line, matching R-02's "Thread 2 exit" with no prior output from Thread 2.

---
*See also: [[os-activity-02]] [[assignments-tracker]]*
