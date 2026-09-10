---
title: Lab 06 — Timer
tags: [mcu, stm32, timer, interrupt, lab]
status: active
updated: 2026-09-09
subject: mcu
---

# Lab 06 — Timer

Course: MCU Interfacing (01276314)
Board: STM32F767 (Cortex M7)
PDF: `~/Documents/University/Year-3/Microcon/2026-Lab-06-Timer.pdf`

---

## CubeMX Setup

### 1. Create project
- **File → New Project → Board Selector tab** (NOT MCU/MPU Selector)
- Search: `NUCLEO-F767ZI` → Start Project → Initialize all peripherals with default mode: **No**

### 2. System clock
- Clock Configuration tab → HCLK = **216 MHz**
- APB1 = 54 MHz (timer clock 108 MHz), APB2 = 108 MHz (timer clock 216 MHz)

### 3. UART3 (already configured from Lab 3)
- Connectivity → USART3 → Mode: Asynchronous, Baud: 115200

### 4. TIM1 (1 ms, APB2 → 216 MHz timer)
- Timers → TIM1 → Clock Source: **Internal Clock**
- Parameter Settings:
  - Prescaler: `216-1` (= 215)
  - Counter Mode: Up
  - Counter Period: `1000-1` (= 999)
  - Internal Clock Division: No Division
  - auto-reload preload: Disable
- NVIC Settings → **TIM1 update interrupt and TIM10 global interrupt**: ✅ Enabled
  - Preemption Priority: **1**, Sub Priority: 0

### 5. TIM2 (400 ms for Exp 2, APB1 → 108 MHz timer)
- Timers → TIM2 → Clock Source: **Internal Clock**
- Parameter Settings:
  - Prescaler: `108-1` (= 107)
  - Counter Mode: Up
  - Counter Period: `400000-1` (= 399999)
  - Internal Clock Division: No Division
- NVIC Settings → **TIM2 global interrupt**: ✅ Enabled
  - Preemption Priority: **2**, Sub Priority: 0

### 6. Generate code
- Project Manager → Project Name, toolchain: STM32CubeIDE → Generate Code

### 7. User code locations
- `main.c` → `/* USER CODE BEGIN 0 */` — declare `uint32_t ms_count`, `uint8_t flag400`
- `stm32f7xx_it.c` → inside `TIM1_UP_TIM10_IRQHandler` and `TIM2_IRQHandler`
- Include `<stdio.h>` and `<string.h>` in `main.c` for `sprintf`/`strlen`

---

## 1. Timer Overview

STM32F767 has 18 timers. TIM1, TIM8 = advanced-control; TIM2–TIM5 = general-purpose.

Properties of each timer:
- 16- or 32-bit counter
- 16-bit prescaler
- Interrupt on overflow
- Up to 4 channels: input capture, output compare, PWM, one-pulse mode

| Bus | Max Bus Freq (MHz) | Max Timer Freq (MHz) | Timers |
|-----|-------------------|----------------------|--------|
| APB1 | 54 | 108 | TIM2–TIM5, TIM12–TIM14 |
| APB2 | 108 | 216 | TIM1, TIM8–TIM11 |

---

## 2. Timer Configuration Formula

```
Time Interval = (Clock Division × Prescaler × Period) / Timer Clock Frequency
```

**Example — TIM1 for 1 ms (216 MHz timer clock):**
```
(1 × 216 × 1000) / 216 MHz = 1 ms
→ Prescaler = 216-1, Period = 1000-1
```

> Prescaler and Period values are -1 from calculation (0-indexed).

CubeMX: Timers → TIM1/TIM2 → Clock Source: Internal Clock → set PSC, ARR.

NVIC:
- TIM1: **TIM1 Update Interrupt** (advanced timer has multiple interrupt vectors)
- TIM2: **TIM2 Global Interrupt** (general-purpose = single vector)

---

## 3. Generated Code

**`MX_TIM1_Init()`** in `tim.c`:
```c
TIM_HandleTypeDef htim1;

htim1.Init.ClockDivision  = TIM_CLOCKDIVISION_DIV1;
htim1.Init.Prescaler      = 216-1;
htim1.Init.Period         = 1000-1;
htim1.Init.CounterMode    = TIM_COUNTERMODE_UP;
```

**Start timer in interrupt mode:**
```c
HAL_TIM_Base_Start_IT(&htim1);
HAL_TIM_Base_Start_IT(&htim2);
```

**ISRs** in `stm32f7xx_it.c`:
- `TIM1_UP_TIM10_IRQHandler` — TIM1 update
- `TIM2_IRQHandler` — TIM2

---

## Experiments

### Exp 1 — TIM1 ISR counter
- TIM1 counts 1 ms; ISR increments `uint32_t count`
- `extern uint32_t count;` in `stm32f7xx_it.c`
- `displayNumber(count)` + `HAL_Delay(400)` in main loop

### Exp 2 — MM:SS clock via TIM1 + TIM2
- TIM1 ISR increments seconds counter
- TIM2 triggers display every 400 ms (replace `HAL_Delay`)
- UART3 output ends with `'\r'` (overwrites same line)
- **Accuracy requirement:** ≤ 2 s error over ≥ 7 minutes
- Use ISR only — no callbacks

Record TIM2 config:

| Parameter | Value |
|-----------|-------|
| TIM2 time interval | 400 ms |
| Clock Division | 1 (No Division) |
| Prescaler | 107 |
| Period | 399999 |
| Calculation | (1 × 108 × 400,000) / 108,000,000 = 0.4 s |

> Output shows 2–3 prints per second — correct. 400 ms doesn't divide evenly into 1000 ms so each second value appears 2–3 times. Clock runs at real speed. ✓

---

## Checkpoints

- [ ] Exp 1
- [ ] Exp 2

## Submission Question

**Q1:** If LED toggle every 500 ms uses timer instead of `HAL_Delay`, how does MCU execution change?
> Timer-driven toggle is interrupt-based — CPU free to run other code in main loop. `HAL_Delay` blocks the CPU for 500 ms doing nothing useful.

---

---

## Solutions

### Exp 1 — TIM1 ISR counter

TIM1 config (from §2): PSC = 216-1, Period = 1000-1 → 1 ms interval.

**`stm32f7xx_it.c`:**
```c
extern uint32_t count;

void TIM1_UP_TIM10_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim1);
    count++;
}
```

**`main.c`:**
```c
uint32_t count = 0;

void displayNumber(uint32_t n) {
    char buf[20];
    sprintf(buf, "%lu\r\n", n);
    HAL_UART_Transmit(&huart3, (uint8_t*)buf, strlen(buf), 100);
}

// before while(1):
HAL_TIM_Base_Start_IT(&htim1);

// inside while(1):
while (1) {
    displayNumber(count);
    HAL_Delay(400);
}
```

---

### Exp 2 — MM:SS clock with TIM1 + TIM2

**TIM2 config for 400 ms** (APB1 → 108 MHz timer clock):
```
Time = (1 × PSC × Period) / 108 MHz = 0.4 s
→ PSC = 108-1, Period = 400000-1
```

| Parameter | Value |
|-----------|-------|
| Time interval | 400 ms |
| Clock Division | 1 (No Division) |
| Prescaler | 107 |
| Period | 399999 |
| Calculation | (1 × 108 × 400000) / 108,000,000 = 0.4 s |

**`stm32f7xx_it.c`:**
```c
extern uint32_t ms_count;
extern uint8_t  flag400;

void TIM1_UP_TIM10_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim1);
    ms_count++;
}

void TIM2_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim2);
    flag400 = 1;
}
```

**`main.c`:**
```c
uint32_t ms_count = 0;
uint8_t  flag400  = 0;

// before while(1):
HAL_TIM_Base_Start_IT(&htim1);
HAL_TIM_Base_Start_IT(&htim2);

// inside while(1):
while (1) {
    if (flag400) {
        flag400 = 0;
        uint32_t total_sec = ms_count / 1000;
        uint32_t mm = total_sec / 60;
        uint32_t ss = total_sec % 60;
        char buf[16];
        sprintf(buf, "%02lu:%02lu\r", mm, ss);
        HAL_UART_Transmit(&huart3, (uint8_t*)buf, strlen(buf), 100);
    }
}
```

**Submission Q1 answer:**
Using timer instead of `HAL_Delay` for LED toggle: CPU is free during the 500 ms wait — `HAL_Delay` busy-waits (SysTick polling), blocking the main loop. Timer-driven toggle fires an ISR, leaving the CPU free to execute other code between interrupts.

---

*See also: [[mcu-lab05-adc]] · [[mcu-lab07-pwm]] · [[mcu-stm32-project]]*
