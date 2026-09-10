---
title: Lab 08 — LCD and Touch Sensor
tags: [mcu, stm32, lcd, touch, rgb, am2320, lab]
status: active
updated: 2026-09-09
subject: mcu
---

# Lab 08 — LCD and Touch Sensor

Course: MCU Interfacing (01276314)
Board: STM32F767 (Cortex M7)
PDF: `~/Documents/University/Year-3/Microcon/2026-Lab-08-LCD.pdf`

---

## CubeMX Setup

### 1. Create project
- Board Selector → NUCLEO-F767ZI → 216 MHz clock.
- Keep USART3. Add ADC1 (potentiometer on PC0 → CH10, see [[mcu-lab05-adc]]).

### 2. LCD — SPI + BSP
The lab uses the **Adafruit 2.8" TFT LCD shield** (ILI9341) or the **STM32 LCD expansion board** connected via SPI.  
Use STM32 BSP drivers if available in the project BSP folder; otherwise use a bare SPI + ILI9341 HAL driver.

**SPI1 config (typical for LCD shield):**
- Connectivity → SPI1 → Mode: Full-Duplex Master
- Data Size: 8 bits, Prescaler: to achieve ~20 MHz (APB2/8 = 13.5 MHz is fine)
- CPOL: Low, CPHA: 1 Edge
- NSS: Software

**GPIO for LCD control pins:**
| Signal | Pin | Mode |
|--------|-----|------|
| LCD_CS | PA4 or custom | Output PP, No pull, High |
| LCD_DC | PB0 or custom | Output PP, No pull |
| LCD_RST | PB1 or custom | Output PP, No pull, High |
| LCD_BL | PE5 or custom | Output PP (or TIM PWM for dimming) |

**LCD backlight via PWM (SP2.2):**
- Pick any timer channel on the backlight pin → configure same as Lab 07 PWM.
- Map ADC value (0–4095) → duty 20–100%: `duty = 0.20f + (adc/4095.0f)*0.80f`

### 3. Touch sensor (XPT2046 or FT6206)
Board-specific. For resistive touch (XPT2046) via SPI2:
- Connectivity → SPI2 → Full-Duplex Master, 8-bit, ~1 MHz
- GPIO: T_CS (PB12), T_IRQ (PB11 → EXTI input with pull-up)

For capacitive touch (FT6206) via I2C:
- Connectivity → I2C1 → Standard Mode (100 kHz)
- GPIO: INT pin → EXTI with pull-up

### 4. AM2320 — I2C temperature + humidity
- Connectivity → I2C1 (or I2C2) → Standard Mode, 100 kHz
- No CubeMX peripheral needed beyond I2C; driver is user code.

**AM2320 read sequence:**
```c
// 1. Wake sensor (expect NACK, ignore error)
HAL_I2C_Master_Transmit(&hi2c1, 0xB8, NULL, 0, 10);
HAL_Delay(1);

// 2. Send read command: func=0x03, start reg=0x00, count=4
uint8_t cmd[3] = {0x03, 0x00, 0x04};
HAL_I2C_Master_Transmit(&hi2c1, 0xB8, cmd, 3, 10);
HAL_Delay(2);

// 3. Read 8 bytes: [func, len, RH_H, RH_L, T_H, T_L, CRC_H, CRC_L]
uint8_t buf[8];
HAL_I2C_Master_Receive(&hi2c1, 0xB9, buf, 8, 10);

float humidity    = ((buf[2] << 8) | buf[3]) / 10.0f;
float temperature = ((buf[4] << 8) | buf[5]) / 10.0f;
```

### 5. ILI9341 driver (if no BSP)
Add ILI9341 open-source driver to project (e.g. `ili9341.c/.h`). Key init:
```c
ILI9341_Init();              // sends init command sequence over SPI
ILI9341_FillScreen(WHITE);
ILI9341_WriteString(x, y, "27.1 C", Font_16x26, BLACK, WHITE);
ILI9341_FillRect(x, y, w, h, RED);    // progress bar
ILI9341_FillCircle(cx, cy, r, color); // colour dot
```

### 6. Generate code + add drivers
- Copy `ili9341.c/.h` and `xpt2046.c/.h` (or FT6206 driver) into `Core/Src/` and `Core/Inc/`.
- Add includes in `main.c`.
- Call `ILI9341_Init()` and `TS_Init()` in `/* USER CODE BEGIN 2 */`.

---

## 1. Objectives

- Display graphics on LCD
- Use touch sensor for interaction

---

## Experiments

### Exp 1 — Screen 1: RGB colour mixer on LCD

White background, black text. Layout (Fig 1.1):

```
┌────────────────────────────┐
│  27.1 C   ●(mixed)  55.6 %RH │
│ ●  ████░░░░░░  80 %          │   ← Red
│ ●  ████░░░░░░  40 %          │   ← Green
│ ●  ████░░░░░░  70 %          │   ← Blue
└────────────────────────────┘
```

Requirements:
- Temperature + humidity from **AM2320** sensor
- Horizontal scrollbar per colour (0–100%)
- Mixed-colour preview circle (top)
- Touch red/green/blue circles → brightness +10%
- Select appropriate font sizes

### Special Problem 2

**SP2.1 — Screen 2: Student info card**

White background, text colour = mixed colour from Screen 1:
```
┌────────────────────────────┐
│ [photo]  Group No.XX        │
│          First name         │
│          Last name          │
│          Student ID         │
└────────────────────────────┘
```

**SP2.2 — Touch to switch screens**
- Screen 1 → touch mixed-colour circle → Screen 2 for 5 s → auto-return Screen 1
- Touch photo on Screen 2 within 5 s → immediate return to Screen 1
- Potentiometer adjusts LCD backlight: 20–100%

---

## Checkpoints

- [ ] Exp 1 (Screen 1)
- [ ] SP2 (Screen 2 + touch switching)

---

---

## Solutions

### Exp 1 — Screen 1 approach

Board has built-in LCD (ILI9341 or similar) + BSP drivers. Use `BSP_LCD_*` HAL from STM32 BSP.

**Key functions:**
```c
BSP_LCD_Init();
BSP_LCD_LayerDefaultInit(0, LCD_FB_START_ADDRESS);
BSP_LCD_SetLayerVisible(0, ENABLE);
BSP_LCD_SelectLayer(0);

BSP_LCD_Clear(LCD_COLOR_WHITE);
BSP_LCD_SetTextColor(LCD_COLOR_BLACK);
BSP_LCD_SetBackColor(LCD_COLOR_WHITE);
BSP_LCD_SetFont(&Font24);

// Draw text
BSP_LCD_DisplayStringAt(x, y, (uint8_t*)"27.1 C", LEFT_MODE);

// Draw filled rectangle (scroll bar fill)
BSP_LCD_SetTextColor(LCD_COLOR_RED);
BSP_LCD_FillRect(x, y, width * r_pct / 100, height);

// Draw circle (colour button)
BSP_LCD_FillCircle(cx, cy, radius);
```

**AM2320 (I2C temp/humidity):** read via `HAL_I2C_Master_Transmit` / `HAL_I2C_Master_Receive`.
Wake sequence: send address, expect NACK, then read 8 bytes (function code, length, RH_H, RH_L, T_H, T_L, CRC_H, CRC_L).

**Touch detection:**
```c
TS_StateTypeDef ts;
BSP_TS_Init(BSP_LCD_GetXSize(), BSP_LCD_GetYSize());

// in loop:
BSP_TS_GetState(&ts);
if (ts.touchDetected) {
    uint16_t tx = ts.touchX[0];
    uint16_t ty = ts.touchY[0];
    // check if (tx, ty) inside red circle bounding box → r += 0.1f; etc.
    if (r > 1.0f) r = 0.0f;
}
```

**PWM for brightness:** connect LED backlight pin to a timer PWM channel; `__HAL_TIM_SET_COMPARE` to adjust from potentiometer ADC value mapped 20–100%.

---

### SP2 — Screen switching

```c
typedef enum { SCREEN_1, SCREEN_2 } Screen;
Screen current = SCREEN_1;
uint32_t screen2_enter_tick = 0;

// in loop:
BSP_TS_GetState(&ts);
if (current == SCREEN_1 && ts.touchDetected) {
    if (/* touch on mixed-colour circle */) {
        current = SCREEN_2;
        screen2_enter_tick = HAL_GetTick();
        draw_screen2();
    }
}
if (current == SCREEN_2) {
    if (ts.touchDetected && /* touch on photo area */) {
        current = SCREEN_1;
        draw_screen1();
    } else if (HAL_GetTick() - screen2_enter_tick >= 5000) {
        current = SCREEN_1;
        draw_screen1();
    }
}
```

**Backlight (potentiometer 20–100%):**
```c
// ADC value 0–4095 → duty 20–100%
float duty = 0.20f + (adc_val / 4095.0f) * 0.80f;
__HAL_TIM_SET_COMPARE(&htimX, TIM_CHANNEL_Y, (uint32_t)((period) * duty));
```

---

*See also: [[mcu-lab07-pwm]] · [[mcu-lab05-adc]] · [[mcu-stm32-project]]*
