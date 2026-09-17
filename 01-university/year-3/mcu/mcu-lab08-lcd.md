---
title: Lab 08 — LCD and Touch Sensor
tags: [mcu, stm32, lcd, touch, rgb, am2320, lab]
status: submitted
updated: 2026-09-16
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
// HAL uses 8-bit address: 0x5C<<1 = 0xB8 (write); HAL sets bit0 for read internally
uint8_t cmd[3] = {0x03, 0x00, 0x04};  // func, start_reg, count
uint8_t buf[8] = {0};

// 1. Wake sensor (expect NACK — ignore error)
HAL_I2C_Master_Transmit(&hi2c1, 0x5C<<1, NULL, 0, 10);  // 0-byte payload = wake only
HAL_Delay(1);

// 2. Send read command
HAL_I2C_Master_Transmit(&hi2c1, 0x5C<<1, cmd, 3, 10);
HAL_Delay(2);

// 3. Read 8 bytes: [func, len, RH_H, RH_L, T_H, T_L, CRC_L, CRC_H]
// Simplified — no CRC check, no error check; see read_am2320() below for full version
HAL_I2C_Master_Receive(&hi2c1, 0x5C<<1, buf, 8, 10);

// Temperature sign bit: buf[4] bit7 = negative flag
uint16_t raw_t = ((buf[4] & 0x7F) << 8) | buf[5];
float temperature = (buf[4] & 0x80) ? -(raw_t / 10.0f) : (raw_t / 10.0f);
float humidity    = ((buf[2] << 8) | buf[3]) / 10.0f;
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
┌──────────────────────────────┐
│  27.1 C   ●(mixed)  55.6 %RH │
│ ●  ████░░░░░░  80 %          │  ← Red
│ ●  ████░░░░░░  40 %          │  ← Green
│ ●  ████░░░░░░  70 %          │  ← Blue
└──────────────────────────────┘
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
┌──────────────────────────────┐
│ [photo]  Group No.XX         │
│          First name          │
│          Last name           │
│          Student ID          │
└──────────────────────────────┘
```

**SP2.2 — Touch to switch screens**
- Screen 1 → touch mixed-colour circle → Screen 2 for 5 s → auto-return Screen 1
- Touch photo on Screen 2 within 5 s → immediate return to Screen 1
- Potentiometer adjusts LCD backlight: 20–100%

---

## Checkpoints

- [x] Exp 1 (Screen 1)
- [x] SP2 (Screen 2 + touch switching)

---

## Solutions (working — NUCLEO-F767ZI, ILI9341 driver, XPT2046 touch)

### Hardware

| Signal | Pin | Notes |
|--------|-----|-------|
| LCD SPI | SPI5: PF7/PF8/PF9 | SCK/MISO/MOSI |
| LCD CS | PG0 | CubeMX label "CS" |
| LCD DC | PG1 | |
| LCD RST | PD1 | CubeMX label "RES" |
| Touch IRQ | PE2 | T_IRQ |
| Touch CLK | PE3 | bit-bang |
| Touch MISO | PE4 | CubeMX label "T_DO" |
| Touch MOSI | PE5 | CubeMX label "T_DIN" |
| Touch CS | PE6 | T_CS |
| Backlight PWM | PB0 | TIM3 CH3 |
| Potentiometer | PC0 | ADC1 CH10 |
| AM2320 | I2C1 | 7-bit addr 0x5C |

**Pin alias gotcha:** driver expects `RST_Pin`, `T_MISO_Pin`, `T_MOSI_Pin` but CubeMX generates `RES_Pin`, `T_DO_Pin`, `T_DIN_Pin`. Add to `main.h` USER CODE Private defines:

```c
#define RST_Pin          RES_Pin
#define RST_GPIO_Port    RES_GPIO_Port
#define T_MISO_Pin       T_DO_Pin
#define T_MISO_GPIO_Port T_DO_GPIO_Port
#define T_MOSI_Pin       T_DIN_Pin
#define T_MOSI_GPIO_Port T_DIN_GPIO_Port
```

### TIM3 — backlight PWM

CubeMX: TIM3 CH3, PSC=99, ARR=999 (1 kHz). In loop:

```c
uint32_t adc = HAL_ADC_GetValue(&hadc1);
uint32_t duty = 200 + (adc * 800) / 4095;  // 200–999 = 20–100%
__HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_3, duty);
```

### Touch coordinate mapping

XPT2046 axes are **swapped** relative to screen (SCREEN_HORIZONTAL_1). Constants below are raw ADC readings from 4-corner calibration on this board — they will differ on other hardware:

```c
// pos[1] = raw X ADC: min≈25 (left) .. max≈320 (right)
// pos[0] = raw Y ADC: min≈25 (top)  .. max≈227 (bottom) — axis inverted
int32_t sx = ((int32_t)pos[1] - 25) * 320 / 295;
int32_t sy = (227 - (int32_t)pos[0]) * 240 / 202;
// clamp: ADC glitch can push values out of range
if (sx < 0) sx = 0; else if (sx > 319) sx = 319;
if (sy < 0) sy = 0; else if (sy > 239) sy = 239;
```

### AM2320 read

```c
static uint16_t CRC16_2(uint8_t *buf, uint8_t len); // forward decl

static uint8_t read_am2320(void) {
    uint8_t cmd[3] = {0x03, 0x00, 0x04}, buf[8] = {0};
    HAL_I2C_Master_Transmit(&hi2c1, 0x5C<<1, NULL, 0, 200); // wake (expect NACK)
    HAL_Delay(1);
    if (HAL_I2C_Master_Transmit(&hi2c1, 0x5C<<1, cmd, 3, 200) != HAL_OK) return 0;
    HAL_Delay(2);
    if (HAL_I2C_Master_Receive(&hi2c1, 0x5C<<1, buf, 8, 200) != HAL_OK) return 0;
    uint16_t rcrc = (buf[7]<<8) | buf[6];
    if (rcrc != CRC16_2(buf, 6)) return 0;
    uint16_t raw_t = ((buf[4]&0x7F)<<8) | buf[5];
    temp_c = (buf[4]&0x80) ? -(raw_t/10.0f) : (raw_t/10.0f);
    hum_rh = ((buf[2]<<8)|buf[3]) / 10.0f;
    return 1;
}
```

CRC16-IBM (polynomial 0xA001). Call `read_am2320()` every 2 s in main loop.

```c
static uint16_t CRC16_2(uint8_t *buf, uint8_t len) {
    uint16_t crc = 0xFFFF;
    for (uint8_t i = 0; i < len; i++) {
        crc ^= buf[i];
        for (uint8_t b = 0; b < 8; b++)
            crc = (crc & 1) ? (crc >> 1) ^ 0xA001 : (crc >> 1);
    }
    return crc;
}
```

### Float formatting

`--specs=nano.specs` disables float in `snprintf`. Use integer math:

```c
// Scale to tenths first, then split — handles negatives correctly
int32_t t10 = (int32_t)roundf(temp_c * 10);  // roundf from <math.h>
int32_t h10 = (int32_t)roundf(hum_rh * 10);
snprintf(buf, sizeof(buf), "%d.%dC",    t10 / 10, (t10 < 0 ? -t10 : t10) % 10);
snprintf(buf, sizeof(buf), "%d.%d%%RH", h10 / 10, h10 % 10);
```

> **Note:** The simpler form `(int)(temp_c*10+0.5f)%10` is wrong for values like 27.96 (rounds decimal independently of integer part → shows 27.0 instead of 28.0) and breaks for negatives.

### Photo on Screen 2

Convert image to 100×120 RGB565 C array → `photo.h`. Draw:

```c
static void draw_region(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, const uint16_t *data) {
    ILI9341_Set_Address(x0, y0, x1, y1);
    ILI9341_Write_Command(0x2C);
    uint32_t n = (uint32_t)(x1-x0+1) * (y1-y0+1);
    for (uint32_t i = 0; i < n; i++) {
        ILI9341_Write_Data(data[i] >> 8);
        ILI9341_Write_Data(data[i] & 0xFF);
    }
}
// usage: draw_region(5, 10, 104, 129, photo_data);
```

---

*See also: [[mcu-lab07-pwm]] · [[mcu-lab05-adc]] · [[mcu-stm32-project]]*
