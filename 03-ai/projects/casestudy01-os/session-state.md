# CaseStudy01 — OS Multithreading

**Path:** `~/Documents/University/Year-3/OS/CaseStudy01`
**Last updated:** 2026-08-08

## Project

OS course case study. C# (.NET 9) single-file program measuring multithreaded performance of a black-box `Calculate1` function.

## Stack

- `Program.cs` — entry point, thread setup, Stopwatch timing
- `DLL/CalculatingFunctions.dll` — precompiled; `CalClass.Calculate1(ref decimal[] value, ref long idx)`
- `data.bin` — 11,000,001 single-precision floats (loaded and scaled ×36)

## Experiment design

- 30 outer iterations, 10M elements per iteration
- `result` and `index` are shared statics — no synchronization by design
- Add threads by uncommenting `Th2` lines in `Main`

## Session log

### 2026-08-08
- Created `CLAUDE.md` (excluded from git via `.gitignore`)
- Created `.gitignore` — excludes `bin/`, `obj/`, `.vs/`, and all AI config files

### 2026-08-09
- Rewrote `Program.cs` with proper multi-worker implementation (replacing naive single-thread baseline)
- Key changes over friend's version: CLI arg for worker count (`dotnet run -- 4`), defaults to `Environment.ProcessorCount`; closure capture replaces `ThreadParameter` class (no boxing); `using`/try-catch on file load; load time outside stopwatch; Debug/Release build label printed
- `(decimal)(f * 36)` float multiply preserved — rewriting as `(decimal)f * 36m` changes result
- `max_accessible_elements = 10000000` intentional — last ~1M elements excluded by design
- Run with `-c Release`. Sweep: `for n in 1 2 4 8 16; do dotnet run -c Release -- $n; done`
- Opus planning agent used for analysis; Fable 5 review hit spend limit — self-reviewed instead
- Upgraded csproj from net9.0 → net10.0 (homebrew only ships .NET 10)

### Benchmark results (2026-08-09, Apple Silicon arm64, Release)

| Workers | Time (ms) | Speedup | Efficiency |
|---------|-----------|---------|------------|
| 1       | 19144     | 1.00×   | 100%       |
| 2       | 9804      | 1.95×   | 97%        |
| 4       | 4857      | 3.94×   | 98%        |
| 8       | 3707      | 5.17×   | 65%        |
| 16      | 3376      | 5.67×   | 35%        |

- Scaling cliff at 8: Apple Silicon 4 P-cores + 4 E-cores. E-cores weak on decimal compute.
- Sweet spot: 4 workers (98% efficiency)
- Friend's 16 beats my default-8 by ~9% on this machine (E-cores still contribute)
- All runs produced correct result: 4686980924312.00

### 2026-08-09 (continued)
- Added `Program.Ref1.cs` — naive shared-state race condition version, excluded from build via csproj `<Compile Remove>`
- Renamed from "cheesy" to "Ref1"
- Updated CLAUDE.md: fixed stale description (was still describing original single-thread version), added benchmark table, documented both files
- Committed to git: `Program.cs`, `Program.Ref1.cs`, `CaseStudy01.csproj`, `CaseStudy01.sln`, `DLL/`, `data.bin` — AI files excluded via .gitignore
- CLAUDE.md guidelines now match actual implementation
