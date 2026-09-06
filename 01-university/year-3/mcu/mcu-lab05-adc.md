---
title: Lab 05 — ADC
tags: [mcu, stm32, adc, dma, lab]
status: active
due: 2026-09-08
updated: 2026-09-05
subject: mcu
---

# Lab 05 — ADC

Course: MCU Interfacing (01276314)
Board: STM32F767 (Cortex M7)

---

## 1. ADC Overview

STM32F767 has 3 ADCs (ADC1, ADC2, ADC3) on APB2 bus.
- Architecture: successive approximation
- Resolution: **12-bit** (values 0x000–0xFFF)
- 19 multiplexed channels: 16 external (CH0–CH15), CH16 unused, CH17 = V_REFINT, CH18 = temp sensor / V_BAT
- Max input voltage: 3.6 V

Pin → channel mapping example: **PC0 → ADC1/ADC2/ADC3 channel 10**

---

## 2. STM32CubeMX Config

- Enable PC0 as **ADC1_IN10** (analog input)
- ADC settings:
  - Clock Prescaler: PCLK2 / 4
  - Resolution: 12 bits (15 ADC clock cycles)
  - Data Alignment: **Right**
  - Continuous Conversion Mode: **Enabled**
  - Scan Conversion Mode: Disabled
  - DMA: Disabled (for basic polling)
  - EOC: at end of all conversions
  - Rank 1 → Channel 10, Sampling Time: 3 Cycles

Generated code configures in `MX_ADC1_Init()` (adc.c) and `HAL_ADC_MspInit()`.

---

## 3. Reading ADC by Polling

```c
volatile uint32_t adc_val = 0;

HAL_ADC_Start(&hadc1);
while (1) {
    while (HAL_ADC_PollForConversion(&hadc1, 100) != HAL_OK) {}
    adc_val = HAL_ADC_GetValue(&hadc1);
}
```

`HAL_ADC_GetValue()` returns `uint32_t`; reading DR register clears EOC flag.

---

## 4. Reducing Swing with Moving Average

ADC values swing due to noise. Moving average smooths it.

```c
int average_8(int x) {
    static int samples[8];
    static int i = 0;
    static int total = 0;
    total += x - samples[i];
    samples[i] = x;
    i = (i == 7 ? 0 : i + 1);
    return total >> 3;  // divide by 8
}

int average_16(int x) {
    static int samples[16];
    static int i = 0;
    static int total = 0;
    total += x - samples[i];
    samples[i] = x;
    i = (i == 15 ? 0 : i + 1);
    return total >> 4;  // divide by 16
}
```

Larger window → smoother but more lag.

---

## 5. Multichannel ADC with DMA

Polling multichannel is risky — overrun causes HardFault if ADC value replaced before read.
DMA transfers data without CPU involvement. Refer to lecture slides for config.

---

## Experiments

### Exp 1 — displayHEX via UART3
Create `void displayHEX(uint32_t)` — prints 8-digit hex via UART3.  
Example: `displayHEX(501)` → `0x000001F5`  
Use `sprintf` from `stdio.h`.

### Exp 2 — Potentiometer circuit
Wire potentiometer to Nucleo-F767:
- Pin 1 → GND
- Pin 2 → PC0
- Pin 3 → V_DD (3.3 V)

### Exp 3 — Read and display ADC value
Config per §2. Poll ADC, display via modified `displayHEX`:

```
ADC1_CH10 0x000001F5  Vin = 0.40 V
```

400 ms delay. Rotate pot and observe.

**Q: min/max ADC values?**  
Min: `0x00000000` (pot fully at GND)  
Max: `0x00000FFF` (4095, pot fully at 3.3 V)

**Q: Why max ≠ 0xFFFFFFFF?**  
ADC is 12-bit → only bits [11:0] used. Right-aligned in 32-bit register → upper 20 bits always 0. Max = 2¹² − 1 = 4095 = 0xFFF.

### Exp 4 — Swing reduction
Add `adc_avg_8` and `adc_avg_16` global vars. Compare all three in STM32CubeMonitor.

### Exp 5 — LED range display
4 LEDs, 5 ADC ranges (12-bit → 0–4095, each range ~819 wide):

| Range | ADC value | LEDs |
|-------|-----------|------|
| 1 | 0–819 | none |
| 2 | 820–1638 | LED0 |
| 3 | 1639–2457 | LED0 + LED1 |
| 4 | 2458–3276 | LED0 + LED1 + LED2 |
| 5 | 3277–4095 | LED0 + LED1 + LED2 + LED3 |

Keep display from Exp 3.

**Q (left alignment):** Left-aligned 12-bit in 16-bit DR register → value shifts left by 4 bits (×16). Multiply all thresholds by 16:

| Range | Right-aligned (Exp 5) | Left-aligned |
|-------|-----------------------|--------------|
| 1 | 0 – 819 | 0 – 13,104 |
| 2 | 820 – 1,638 | 13,120 – 26,208 |
| 3 | 1,639 – 2,457 | 26,224 – 39,312 |
| 4 | 2,458 – 3,276 | 39,328 – 52,416 |
| 5 | 3,277 – 4,095 | 52,432 – 65,520 |

Max left-aligned value = 4095 × 16 = 65,520 (not 65,535, because 12-bit max is 0xFFF not 0xFFFF).

---

## Special Problem 1 — Multichannel ADC via DMA

- 2 potentiometers × 4 ADC1 channels each = 8 channels total (avoid blue-label mbed pins e.g. PA7)
- DMA transfers values; LD2 ON after first half, OFF after second half
- Display via UART3

---

---

## Submission Questions (Lab 5 answer sheet)

**Q1: Which microcontroller pin can function as channel 1 of ADC2?**  
**PA1** — PA1 is ADC2_IN1.

**Q2: From Exp 5, adjust 5 ranges for left alignment to produce same result.**  
Left-aligned 12-bit in 16-bit register → MSB aligns to bit 15, shift left by 4 (16 − 12). DR value = raw × 16. In hex, every value gains a trailing `0` (e.g. `0x333` → `0x3330`). Max = `0xFFF0` (65,520), not `0xFFFF`. Multiply all boundaries by 16:

| Range | Right-aligned | Left-aligned (×16) |
|-------|--------------|--------------|
| 1 | 0 – 819 | 0 – 13,104 |
| 2 | 820 – 1,638 | 13,120 – 26,208 |
| 3 | 1,639 – 2,457 | 26,224 – 39,312 |
| 4 | 2,458 – 3,276 | 39,328 – 52,416 |
| 5 | 3,277 – 4,095 | 52,432 – 65,520 |

---

## Checkpoints

- [ ] Exp 3 & 4
- [ ] Exp 5

---

*See also: [[mcu-lab04-nvic-exti]] · [[mcu-stm32-project]]*
