---
title: DumbassCPU
tags: [programming, hardware]
status: stable
---

# DumbassCPU

8-bit CPU designed from scratch in VHDL. Xilinx Vivado project targeting FPGA.
Code: `~/Code/DumbassCPU`. GitHub: `FriedHamCheese/DumbassCPU`.

## What it is

Single-cycle, Harvard-ish architecture.

- 2 general-purpose registers: **A**, **B** (8-bit each)
- 16-byte RAM (`memory16x8`)
- 64-slot hardcoded **program ROM** (constants wired into MUX inputs)
- 8-bit program counter
- 7-segment display output via `CPUInterface`
- Loaded program: multiplies two numbers stored in `mem[0]` × `mem[1]` → `mem[2]`

## How it works

**Dual-mode opcode source:**
- `opcode(7) = 0` → use externally-fed opcode/immediate (manual step mode via FPGA switches)
- `opcode(7) = 1` → fetch from ROM (PC-driven auto-run)

Switched with AND-gate masking: no multiplexer, just `AND` with the mode bit.

**Register input routing:**
Two `Core_ByteMultiplexer` instances (64-to-1, 8-bit wide) select which ALU result feeds into reg A or B. The **opcode value is the mux select directly** — no separate control decoder. Every ALU unit runs simultaneously; the mux picks the right result.

**Program counter:**
- Increments via an `Adder8Bit` (A + 0 + carry=1)
- `SET PC, A` (opcode 63) or `JMP A` (opcode 129) override it with reg A value
- AND-gate masking selects increment vs. jump

**ROM:**
Two more `Core_ByteMultiplexer` instances. Each of the 64 opcode/immediate slots is a constant `std_logic_vector` wired to a mux input. Address = mux select.

## ISA

| Opcode | Instruction |
|---|---|
| 0 | `SET A, imm` |
| 1 | `SET A, B` |
| 2 | `SET B, A` |
| 3 | `SET A, mem[A]` |
| 4 | `SET mem[A], B` |
| 5 | `SET B, imm` |
| 6 | `SUB A, B` → A = A−B |
| 7 | `ADD A, B` → A = A+B |
| 8 | `AND A, B` |
| 9 | `OR A, B` |
| 10 | `NOT A` |
| 11 | `XOR A, B` |
| 12 | `PROP B, 0` — fill all bits of B with B[0] |
| 16 | `SHL A, B` |
| 17 | `SHR A, B` |
| 18 | `MUL A, B` |
| 19 | `RDIV A, B` — approximate: right-shift by log₂(B) |
| 62 | `NOP` |
| 63 | `SET PC, A` |
| 129 | `JMP A` |

`RDIV` is lossy — divides by nearest power of 2 via priority-encoder + shift.

## Gate count

Counted from source (combinational logic gates; DFFs separate).

| Block | Gates | DFFs |
|---|---|---|
| 3× ByteRegister (A, B, PC) | ~96 | 24 |
| 2× Adder8Bit (ALU + PC increment) | ~96 | — |
| Subtracter | ~64 | — |
| ShiftLeft | ~128 | — |
| ShiftRight | ~88 | — |
| Multiplier8Bit (7 adders + partial-product ANDs) | ~400 | — |
| RoughDivide (priority encoder + ShiftRight) | ~132 | — |
| ByteComparator (8× BitComparator chain) | ~104 | — |
| 2× Core_ByteMultiplexer (reg A/B input routing) | ~4,896 | — |
| ProgramROM (2× Core_ByteMultiplexer) | ~4,896 | — |
| RAM 16×8 (reg8 array + decoders + mux) | ~768 | 128 |
| CPU control logic (opcode decode, mux selects) | ~284 | — |
| **Total** | **~11,952** | **~152** |

The 4 `Core_ByteMultiplexer` instances account for ~82% of all logic gates.
Each is a 64-input, 8-bit-wide MUX built from two stages of `EightBitToOneBitMultiplexer` repeated 8 times.

## Key design choices

- No microcode, no control ROM — opcode feeds MUX select directly
- All ALU units are always active; mux discards unused results
- ROM is pure combinational (MUX with hardwired constants), not BRAM
- `PROP B, 0` (opcode 12) replicates LSB across all 8 bits — used in the multiply loop to test a bit
