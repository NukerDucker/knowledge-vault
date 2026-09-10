---
title: Lab 07 — PWM
tags: [mcu, stm32, pwm, timer, rgb, lab]
status: active
updated: 2026-09-09
subject: mcu
---

# Lab 07 — PWM

Course: MCU Interfacing (01276314)
Board: STM32F767 (Cortex M7)
PDF: `~/Documents/University/Year-3/Microcon/2026-Lab-07-PWM.pdf`

---

## CubeMX Setup

### 1. Create project
- Reuse Lab 06 project **or** create new from Board Selector (NUCLEO-F767ZI), 216 MHz clock.
- Keep USART3 configured.

### 2. TIM2 — PWM on CH3 (Exp 1 & 2)
- Timers → TIM2 → Clock Source: **Internal Clock**
- Channel 3: **PWM Generation CH3**
- Parameter Settings:
  - Prescaler: `108-1` (= 107) — APB1 timer clock 108 MHz
  - Counter Mode: Up
  - Counter Period (ARR): `10000-1` (= 9999) → 10 ms period
  - Internal Clock Division: No Division
  - auto-reload preload: Disable
- PWM Generation Channel 3:
  - Mode: **PWM mode 1**
  - Pulse (CCR3): `10000/4 - 1` (= 2499) → 25% duty cycle
  - Output compare preload: Enable
  - Fast Mode: Disable
- **No NVIC needed for PWM** (no interrupt)
- Pin mapping: CubeMX auto-assigns **PB10** as TIM2_CH3 (PA2 conflicts with UART2)
  - If not auto-assigned: Pinout view → PB10 → TIM2_CH3

### 3. Verify PB10 GPIO config (auto-generated)
- GPIO mode: Alternate Function Push Pull
- Pull-up/Pull-down: No pull
- Maximum output speed: Very High
- Alternate Function: AF1 TIM2

### 4. TIM3 — RGB LED (Exp 3, 3 PWM channels)
- Timers → TIM3 → Clock Source: Internal Clock
- Channel 1: PWM Generation CH1 → **PB4**
- Channel 2: PWM Generation CH2 → **PB5**
- Channel 3: PWM Generation CH3 → **PB0**
- Same parameters: PSC=107, ARR=9999, Mode=PWM1, Pulse=0
- No NVIC

### 5. ADC1 (for STM32CubeMonitor variable monitoring)
- No extra config needed — CubeMonitor reads variables directly via SWD debug interface.

### 6. Generate code
- Add `#include <string.h>` and `#include <stdio.h>` in `main.c` if needed.
- Declare `uint8_t pwm;` and `float dutyCycle;` in `/* USER CODE BEGIN 0 */`.

### 7. Start PWM before while(1)
```c
/* USER CODE BEGIN 2 */
HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
/* USER CODE END 2 */
```
For Exp 3 also start htim3 channels 1, 2, 3.

---

## 1. PWM Overview

Timers generate PWM by comparing counter register vs `TIMx_CCRx`:

| Mode | Count direction | PWM HIGH when |
|------|----------------|---------------|
| Mode 1 | Up | counter < CCRx |
| Mode 2 | Down | counter > CCRx |

- **Frequency** controlled by `TIMx_ARR` (Period register)
- **Duty cycle** controlled by `TIMx_CCRx` (Pulse register)

---

## 2. CubeMX Config — TIM2_CH3 PWM

- TIM2 → Channel 3 → PWM Generation CH3
- Clock Source: Internal Clock
- Pin: **PB10** (use instead of PA2 if PA2 taken by UART2)
  - PB10 → GPIO mode: Alternate Function Push Pull, speed: Very High

**10 ms period, 25% duty cycle** (TIM2 on APB1 → 108 MHz timer clock):
```
Prescaler = 108-1
Period    = 10000-1
Pulse     = 10000/4 - 1   (25%)
```

---

## 3. Generated Code

**`MX_TIM2_Init()`:**
```c
TIM_HandleTypeDef htim2;

htim2.Init.Prescaler    = 108-1;
htim2.Init.CounterMode  = TIM_COUNTERMODE_UP;
htim2.Init.Period       = 10000-1;
htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

sConfigOC.OCMode   = TIM_OCMODE_PWM1;
sConfigOC.Pulse    = 10000/4 - 1;
HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_3);
```

**`HAL_TIM_MspPostInit()`** (stm32f7xx_hal_msp.c) — configures PB10 as TIM2_CH3 alternate function.

**Start/stop PWM:**
```c
HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
HAL_TIM_PWM_Stop(&htim2, TIM_CHANNEL_3);
```

**Change duty cycle at runtime:**
```c
htim2.Instance->CCR3 = (10000-1) * dutyCycle;
```

---

## 4. RGB LED

4-pin LED: R, G, B + common (cathode or anode). 3 current-limiting resistors required.
Drive each channel with a separate PWM channel.

---

## Experiments

### Exp 1 — PWM on TIM2_CH3 (PB10)
- 10 ms period, 25% duty cycle
- LED at PB10; compare brightness vs logic HIGH
- Read pin state: `pwm = (GPIOB->IDR & GPIO_PIN_10) >> 10;`
- Verify with STM32CubeMonitor

### Exp 2 — Adjustable duty cycle
```c
float dutyCycle = 0.5;
htim2.Instance->CCR3 = (10000-1) * dutyCycle;
```

Record from STM32CubeMonitor for dutyCycle = 0.5, 0.25, 0.75, 1.0, 2.0:

| dutyCycle | t1 (s) | t2 (s) | t3 (s) | Calculated duty cycle |
| --------- | ------ | ------ | ------ | --------------------- |
| 0.25      | 1.45   | 1.80   | 2.45   | 32/110 = 0.291        |
| 0.5       | 0.4    | 0.9    | 1.4    | 55/110 = 0.500        |
| 0.75      | 1.40   | 2.09   | 2.40   | 76/110 = 0.691        |
| 1.0       | 0.0    | 1.0    | 1.0    | 1.000                 |
| 2.0       | 0.0    | 1.0    | 1.0    | 1.000                 |

### Exp 3 — RGB LED colour mixing
- 3 PWM channels (any free pins)
- UART3 input: `r`/`g`/`b` keys cycle brightness 0→20→40→60→80→100→0%
- Show duty cycles in STM32CubeMonitor

| Colour | Timer | Channel | GPIO pin |
|--------|-------|---------|----------|
| Red | | | |
| Green | | | |
| Blue | | | |

---

## Checkpoints

- [ ] Exp 2
- [ ] Exp 3

## Submission Question

**Q1:** Changing `TIM_OCMODE_PWM1` → `TIM_OCMODE_PWM2` in Exp 1 — what happens?
> PWM polarity inverts. Mode 1: HIGH when counter < CCR, LOW otherwise. Mode 2: LOW when counter < CCR, HIGH otherwise. Same duty cycle %, opposite signal — LED behaviour unchanged for symmetric PWM but waveform flips.

---

---

## Solutions

### Exp 1 — PWM on TIM2_CH3

```c
uint8_t pwm;

// inside while(1):
while (1) {
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
    HAL_Delay(100);
    HAL_TIM_PWM_Stop(&htim2, TIM_CHANNEL_3);
    pwm = (GPIOB->IDR & GPIO_PIN_10) >> 10;
}
```

---

### Exp 2 — Adjustable duty cycle

```c
float dutyCycle = 0.5;

// inside while(1):
while (1) {
    htim2.Instance->CCR3 = (uint32_t)((10000 - 1) * dutyCycle);
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
    HAL_Delay(100);
    HAL_TIM_PWM_Stop(&htim2, TIM_CHANNEL_3);
    pwm = (GPIOB->IDR & GPIO_PIN_10) >> 10;
}
```

Expected Table 5.1 results (10 ms period):

| dutyCycle | t1 (s) | t2 (s) | t3 (s) | Duty cycle |
|-----------|--------|--------|--------|------------|
| 0.5 | — | ~0.005 | ~0.010 | 0.500 |
| 0.25 | — | ~0.0025 | ~0.010 | 0.250 |
| 0.75 | — | ~0.0075 | ~0.010 | 0.750 |
| 1.0 | — | ~0.010 | ~0.010 | 1.000 (always HIGH) |
| 2.0 | — | ~0.010 | ~0.010 | 1.000 (CCR > ARR → clamped) |

> dutyCycle = 2.0 → CCR3 = 19999 > ARR = 9999 → output stays HIGH, effective duty = 100%.

---

### Exp 3 — RGB LED colour mixing

Use TIM3_CH1 (PB4), TIM3_CH2 (PB5), TIM3_CH3 (PB0) or any 3 free PWM-capable pins.
Period = 10000-1, PSC = 108-1 (same 10 ms period, 108 MHz APB1).

```c
// global
float r = 0.0f, g = 0.0f, b = 0.0f;

void setRGB(void) {
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, (uint32_t)((10000-1) * r));
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, (uint32_t)((10000-1) * g));
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_3, (uint32_t)((10000-1) * b));
}

// before while(1):
HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);
HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);

// inside while(1):
while (1) {
    uint8_t ch;
    if (HAL_UART_Receive(&huart3, &ch, 1, 10) == HAL_OK) {
        float *target = NULL;
        if (ch == 'r') target = &r;
        else if (ch == 'g') target = &g;
        else if (ch == 'b') target = &b;
        if (target) {
            *target += 0.2f;
            if (*target > 1.0f + 0.01f) *target = 0.0f;
            setRGB();
        }
    }
}
```

**Submission Q1 answer:**
`TIM_OCMODE_PWM2` inverts the signal vs `PWM1`. PWM1: output HIGH while counter < CCR (active-high). PWM2: output LOW while counter < CCR (active-low). Same duty cycle percentage, opposite polarity — LED driven with common cathode would behave identically in duty cycle but signal phase flips; with common anode, brightness inverts.

---

*See also: [[mcu-lab06-timer]] · [[mcu-lab08-lcd]] · [[mcu-stm32-project]]*
