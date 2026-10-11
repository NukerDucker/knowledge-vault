---
title: Lab Exam — Cheat Sheet
tags: [stm32, lab]
status: active
updated: 2026-09-28
subject: mcu
course: 01276314
---

# MCU Lab Exam — Cheat Sheet

Course: MCU Interfacing (01276314)
Exam: 7 Oct 2026 · 17:30–18:45 · ECC-704
Student: Napaul Intharasing · 67011178 · Lab 19 · Exam Group 1
Artifact: https://claude.ai/artifact/TzMmwbU68edHBcNwgJNCjh
HTML: `01-university/year-3/mcu/mcu-lab-exam-cheatsheet.html`

---

## Exam Rules

- Workspace: `D:\67011178_exam` — delete with **Shift+Delete** after
- Max **2 submissions per question**
- 1 handwritten A4 sheet allowed
- Can start from `767_SPI_ILI9341 v2.zip` for LCD questions

---

## Exam Start Ritual

1. File → Switch Workspace → `D:\67011178_exam`
2. New Project → Board Selector → NUCLEO-F767ZI → Init all: **No**
3. Clock Config → HCLK = **216 MHz**
4. USART3 → Async · 115200
5. Project Mgr → STM32CubeIDE → Generate
6. `#include <stdio.h>` + `#include <string.h>` in main.c

---

## Numbers to Memorize

| Value | Meaning |
|-------|---------|
| 216 MHz | APB2 timer clock (TIM1) |
| 108 MHz | APB1 timer clock (TIM2–5) |
| 4095 | ADC max (12-bit) |
| 9999 | PWM ARR (PSC=107, 10ms period) |
| PC13 | B1 button → EXTI15_10_IRQn |
| 0x5C | AM2320 I2C address (shift left 1 in HAL) |

---

## Recipe Index

| Recipe | Key peripheral | Pin/timer |
|--------|---------------|-----------|
| 1 — Timer interrupt | TIM1 (1ms) + TIM2 (slow) | APB2/APB1 |
| 2 — EXTI button | PC13 → GPIO_EXTI13 | EXTI15_10_IRQn |
| 3 — ADC → UART | ADC1 CH10 | PC0 |
| 4 — ADC → PWM | TIM2 CH3 | **PB10** (not PA2!) |
| 5 — ADC → LCD | ILI9341 SPI | start from v2.zip |
| 6 — AM2320 → LCD | I2C1 + ILI9341 | 0x5C addr |

---

## Callback Names (exact)

```c
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc)
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
```

---

## Common Mistakes

- PWM on PA2 → conflict with UART2 → use **PB10**
- Timer: used `Start` not `Start_IT` → no callback
- ADC: missing `PollForConversion` before `GetValue`
- LCD ghost digits: erase with white FillRect before redrawing
- AM2320 NACK on wake → **normal**, ignore error and continue
- sprintf crash: missing `#include <stdio.h>`
- Code disappeared after regen: was outside USER CODE blocks
