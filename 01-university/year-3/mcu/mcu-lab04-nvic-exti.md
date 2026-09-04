---
title: Lab 04 — NVIC and EXTI
tags: [mcu, stm32, nvic, exti, interrupt, lab]
status: active
updated: 2026-08-26
subject: mcu
---

# Lab 04 — NVIC and EXTI

Course: MCU Interfacing (01276314)
Board: STM32F767 (Cortex M7)

---

## 1. Priority Interrupt

**Interrupt** = MCU temporarily halts current execution → handles incoming signal → resumes.

**NVIC** (Nested Vectored Interrupt Controller) = module that controls/responds to interrupt signals. Handles simultaneous interrupts or new interrupt arriving while handling previous one.

### Priority field

Cortex M7 uses 8-bit priority field. STM32F767 uses only **4 bits**, split into:

- `PreemptionPriority` — lower value = higher priority. Can preempt a currently-handled interrupt.
- `SubPriority` — tiebreaker when two interrupts share same `PreemptionPriority`; pending ones only (no preemption).

### Priority groups (Table 1.1)

| NVIC_PriorityGroup | PreemptionPriority bits | Possible values | SubPriority bits | Possible values |
|---|---|---|---|---|
| NVIC_PriorityGroup_0 | 0 | 0 | 4 | 0–15 |
| NVIC_PriorityGroup_1 | 1 | 0–1 | 3 | 0–7 |
| NVIC_PriorityGroup_2 | 2 | 0–3 | 2 | 0–3 |
| NVIC_PriorityGroup_3 | 3 | 0–7 | 1 | 0–1 |
| NVIC_PriorityGroup_4 | 4 | 0–15 | 0 | 0 |

---

## 2. CubeMX Configuration

### Step 1 — Configure PC13 as EXTI13

Pinout tab → PC13 → `GPIO_EXTI13`
(B1 button on PC13 → EXTI instead of GPIO input)

### Step 2 — Configure NVIC group

System Core → NVIC → Priority Group: **NVIC_PriorityGroup_1** (1-bit PreemptionPriority, 3-bit SubPriority)

Enable `EXTI line[15:10] interrupts`, set PreemptionPriority = 1, SubPriority = 0.

### Step 3 — Configure PC13 GPIO mode

GPIO → PC13 → NVIC tab:
- GPIO mode: **External Interrupt Mode with Rising edge trigger detection**
- GPIO Pull-up/Pull-down: **No pull-up and no pull-down** (floating input)

---

## 3. Generated Code

### `HAL_MspInit()` in `stm32f7xx_hal_msp.c`

Sets the priority group:

```c
void HAL_MspInit(void)
{
    __HAL_RCC_SYSCFG_CLK_ENABLE();
    __HAL_RCC_PWR_CLK_ENABLE();

    HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_1);  // ← priority group set here

    /* System interrupt init */
}
```

### `MX_GPIO_Init()` in `main.c`

```c
void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    /* GPIO Ports Clock Enable */
    __HAL_RCC_GPIOC_CLK_ENABLE();

    /* Configure GPIO pin: PC13 */
    GPIO_InitStruct.Pin  = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;   // EXTI, rising edge
    GPIO_InitStruct.Pull = GPIO_NOPULL;            // floating
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    /* EXTI interrupt init */
    HAL_NVIC_SetPriority(EXTI15_10_IRQn, 1, 0);
    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
}
```

**Notes on `MX_GPIO_Init`:**
- `__GPIOC_CLK_ENABLE()` — enables clock to GPIOC (B1 button on PC13)
- Rising edge = interrupt fires when B1 is pushed
- `HAL_NVIC_SetPriority(EXTI15_10_IRQn, 1, 0)` — PreemptionPriority=1, SubPriority=0
- `HAL_NVIC_EnableIRQ(EXTI15_10_IRQn)` — enables the interrupt

---

## 4. EXTI

**EXTI** (External Interrupt) = module that detects digital signal from GPIO pins → sends interrupt signal to NVIC when predefined condition met (rising edge / falling edge / both).

### GPIO → EXTI mapping

GPIO pins with **same pin number** share the same EXTI signal regardless of port:
- PA0, PB0, PC0 … PG0 → all share EXTI0
- PA13, PB13, PC13 … PG13 → all share EXTI13
- Configured via `AFIOx_EXTICRx` register bits (4 bits per line select which port)

---

## 5. Interrupt Service Routine (ISR)

When NVIC sends interrupt signal to processor core:
1. Processor halts current execution
2. Calls ISR from **vector table** (location stored there)
3. ISR runs
4. Processor resumes halted execution

### Example flow (B1 button)

PC13 push → EXTI13 signal → NVIC → processor halts → calls `EXTI15_10_IRQHandler()`

### ISR location

`EXTI15_10_IRQHandler()` is in `stm32f7xx_it.c`
- Handles EXTI10–EXTI15 (shared IRQ line)
- Vector table declared in `startup_stm32f767zitx.s`

### ISR names by EXTI line

| EXTI lines | IRQ name | ISR function |
|---|---|---|
| EXTI0 | EXTI0_IRQn | `EXTI0_IRQHandler()` |
| EXTI1 | EXTI1_IRQn | `EXTI1_IRQHandler()` |
| EXTI2 | EXTI2_IRQn | `EXTI2_IRQHandler()` |
| EXTI3 | EXTI3_IRQn | `EXTI3_IRQHandler()` |
| EXTI4 | EXTI4_IRQn | `EXTI4_IRQHandler()` |
| EXTI5–9 | EXTI9_5_IRQn | `EXTI9_5_IRQHandler()` |
| EXTI10–15 | EXTI15_10_IRQn | `EXTI15_10_IRQHandler()` |

### ISR implementation example

```c
void EXTI15_10_IRQHandler(void)
{
    /* USER CODE BEGIN EXTI15_10_IRQn 0 */
    /* USER CODE END EXTI15_10_IRQn 0 */
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);
    /* USER CODE BEGIN EXTI15_10_IRQn 1 */
    HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_0);  // toggle LD1 on PB0
    /* USER CODE END EXTI15_10_IRQn 1 */
}
```

`HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13)` — inspects interrupt, clears pending bit, calls callback.

```c
void HAL_GPIO_EXTI_IRQHandler(uint16_t GPIO_Pin)
{
    if (__HAL_GPIO_EXTI_GET_IT(GPIO_Pin) != RESET)
    {
        __HAL_GPIO_EXTI_CLEAR_IT(GPIO_Pin);
        HAL_GPIO_EXTI_Callback(GPIO_Pin);
    }
}
```

---

## 6. Callback Function

**Callback** = function invoked inside ISR for sophisticated handling (separate success/error paths).

- EXTI: 1 callback → `HAL_GPIO_EXTI_Callback()`
- UART receive: 2 callbacks → `HAL_UART_RxCpltCallback()` (success), `HAL_UART_ErrorCallback()` (error)

### HAL flow (EXTI)

```
init NVIC → init GPIO → [edge detected] → EXTI IRQHandler → HAL EXTI interrupt handler
→ HAL clears flags → HAL_GPIO_EXTI_Callback()
```

### `__weak` pattern

CubeMX generates callback as `__weak` in `stm32f7xx_hal_gpio.c` — **do not modify**. Reimplement in `main.c`:

```c
/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_13)
    {
        HAL_UART_Transmit(&huart3, (uint8_t *) "---", 3, 100);
        HAL_Delay(200);
        for (int i=0; i<20; i++)
        {
            HAL_UART_Transmit(&huart3, (uint8_t *) "B", 1, 100);
            HAL_Delay(200);
        }
    }
}
/* USER CODE END 4 */
```

Argument `GPIO_Pin` = EXTI number that caused interrupt. Check it to distinguish multiple EXTI sources.

### ⚠️ ISR Pitfall — No HAL_Delay inside callback

`HAL_Delay` spins waiting for `uwTick` to increment (driven by SysTick IRQ). STM32 HAL sets SysTick to priority **15** (lowest). EXTI interrupt at priority 1 is higher — SysTick cannot preempt the running EXTI ISR → `uwTick` never increments → `HAL_Delay` loops forever → MCU freezes, requires reset. Symptom: first UART output (`---`) prints, then MCU stops responding.

**Rule:** ISR must finish in microseconds. No delays, no blocking, no long loops.

**Fix — flag pattern:**

```c
/* Private variables (top of main.c) */
volatile uint8_t btn_flag = 0;  // volatile: prevents compiler register-caching across ISR/main

/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_13) btn_flag = 1;  // ISR exits immediately
}
/* USER CODE END 4 */

/* Infinite loop */
/* USER CODE BEGIN WHILE */
while (1)
{
    HAL_UART_Transmit(&huart3, (uint8_t *)".", 1, 100);
    HAL_Delay(400);
    /* USER CODE BEGIN 3 */
    if (btn_flag)
    {
        btn_flag = 0;
        HAL_UART_Transmit(&huart3, (uint8_t *)"---", 3, 100);
        HAL_Delay(200);
        for (int i = 0; i < 20; i++)
        {
            HAL_UART_Transmit(&huart3, (uint8_t *)"B", 1, 100);
            HAL_Delay(200);
        }
    }
}
/* USER CODE END 3 */
```

---

## 7. Experiments

### Exp 1 — Basic EXTI (B1 button)

**Pin config:**
- PC13 → `GPIO_EXTI13` (B1, rising edge, no pull)
- PB0, PB7, PB14 → `GPIO_Output` (3 LEDs)
- PD8, PD9 → UART3

**ISR:** `EXTI15_10_IRQHandler` → `HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13)`

**Callback:** on GPIO_PIN_13 → send `"---"` then 20× `"B"` via UART3, 200ms delay each

**main loop:** send `"."` every 400ms indefinitely

Observe in TeraTerm: `.` stream interrupted by `---BBBB…` when B1 pushed.

---

### Exp 2 — Two external buttons (PA0, PA5)

**Add:** external buttons on PA0, PA5 → falling edge EXTI, toggle LD2 (PB7) and LD3 (PB14)

**Callback additions:**
- `GPIO_PIN_0` → send `"---"` + 20× `"E"`
- `GPIO_PIN_5` → send `"---"` + 20× `"5"`

**Checkpoint:** Exp 2 + Exp 3.2

---

### Exp 3 — Priority interrupt (NVIC_PriorityGroup_2)

Push B1 while 'B' chars printing → does PA0 preempt? Push PA0 while 'E' printing → does B1 preempt?

**Table 7.1 — Priority config:**

| Exp | Button | PreemptionPriority | SubPriority |
|---|---|---|---|
| 3.1 | B1 | 2 | 2 |
| 3.1 | External PA0 | 2 | 0 |
| 3.2 | B1 | 3 | 1 |
| 3.2 | External PA0 | 2 | 3 |

**Exp 3.1:** Same PreemptionPriority → SubPriority decides pending order only (no preemption mid-ISR).

**Exp 3.2:** PA0 PreemptionPriority=2 < B1 PreemptionPriority=3 → PA0 can preempt B1's ISR.

**Checkpoint:** Exp 3.2

---

### Exp 4 — SubPriority (NVIC_PriorityGroup_2)

**Table 7.2:**

| Button | PreemptionPriority | SubPriority |
|---|---|---|
| B1 | 3 | 1 |
| External PA0 | 2 | 3 |
| External PA5 | 3 | 3 |

Push PA0 → while 'E' printing, push B1 then PA5. Observe order.
Push PA0 → while 'E' printing, push PA5 then B1. Observe order.

PA0 (Preemption=2) preempts all. B1 vs PA5 same Preemption=3, B1 SubPriority=1 < PA5 SubPriority=3 → B1 handled first when both pending.

**Checkpoint:** Exp 4

---

## 8. Code

### `main.c` — main loop (all experiments)

```c
/* USER CODE BEGIN WHILE */
while (1)
{
    HAL_UART_Transmit(&huart3, (uint8_t *)".", 1, 100);
    HAL_Delay(400);
}
```

### `main.c` — callback (Exp 1: PC13 only)

```c
/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_13)
    {
        HAL_UART_Transmit(&huart3, (uint8_t *)"---", 3, 100);
        HAL_Delay(200);
        for (int i = 0; i < 20; i++)
        {
            HAL_UART_Transmit(&huart3, (uint8_t *)"B", 1, 100);
            HAL_Delay(200);
        }
    }
}
/* USER CODE END 4 */
```

### `main.c` — callback (Exp 2+: PC13 + PA0 + PA5)

```c
/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    char ch;
    if      (GPIO_Pin == GPIO_PIN_13) { ch = 'B'; HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_0);  }
    else if (GPIO_Pin == GPIO_PIN_0)  { ch = 'E'; HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_7);  }
    else if (GPIO_Pin == GPIO_PIN_5)  { ch = '5'; HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_14); }
    else return;

    HAL_UART_Transmit(&huart3, (uint8_t *)"---", 3, 100);
    HAL_Delay(200);
    for (int i = 0; i < 20; i++)
    {
        HAL_UART_Transmit(&huart3, (uint8_t *)&ch, 1, 100);
        HAL_Delay(200);
    }
}
/* USER CODE END 4 */
```

### `main.c` — PA0 + PA5 init (add inside `MX_GPIO_Init`, Exp 2+)

```c
/* Exp 2: external buttons on PA0, PA5 — falling edge */
__HAL_RCC_GPIOA_CLK_ENABLE();

GPIO_InitStruct.Pin  = GPIO_PIN_0 | GPIO_PIN_5;
GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
GPIO_InitStruct.Pull = GPIO_PULLUP;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

HAL_NVIC_SetPriority(EXTI0_IRQn,   1, 0);  // PA0 — change per Exp 3/4
HAL_NVIC_EnableIRQ(EXTI0_IRQn);
HAL_NVIC_SetPriority(EXTI9_5_IRQn, 1, 0);  // PA5 — change per Exp 3/4
HAL_NVIC_EnableIRQ(EXTI9_5_IRQn);
```

### `stm32f7xx_it.c` — ISRs for PA0 + PA5 (Exp 2+)

```c
void EXTI0_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

void EXTI9_5_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_5);
}
```

`EXTI15_10_IRQHandler` for PC13 is already generated by CubeMX — just add the `HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_0)` in USER CODE section if needed, or let callback handle it.

### Priority values to swap per experiment

Change these 3 `HAL_NVIC_SetPriority` calls in `MX_GPIO_Init()` in `main.c`:

```c
// Exp 3.1 (PriorityGroup_2):
HAL_NVIC_SetPriority(EXTI15_10_IRQn, 2, 2);  // B1
HAL_NVIC_SetPriority(EXTI0_IRQn,     2, 0);  // PA0

// Exp 3.2 (PriorityGroup_2):
HAL_NVIC_SetPriority(EXTI15_10_IRQn, 3, 1);  // B1
HAL_NVIC_SetPriority(EXTI0_IRQn,     2, 3);  // PA0

// Exp 4 (PriorityGroup_2):
HAL_NVIC_SetPriority(EXTI15_10_IRQn, 3, 1);  // B1
HAL_NVIC_SetPriority(EXTI0_IRQn,     2, 3);  // PA0
HAL_NVIC_SetPriority(EXTI9_5_IRQn,   3, 3);  // PA5
```

Also update `HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_2)` in `HAL_MspInit` for Exp 3+.

---

## Submission

**Checkpoints (in lab):** Exp 2+3.2, Exp 4

**Question (written):**
> From Exp 3, if priority changed to `NVIC_PriorityGroup_1`, can B1 and external button interrupt each other? If yes, specify scenario. If no, give reason. (Note: PreemptionPriority=0 reserved for pre-configured interrupts like timer.)
>
> **Answer:** No. `NVIC_PriorityGroup_1` reserves only 1 bit for PreemptionPriority (values 0–1), and value 0 is reserved for other system modules — that leaves B1 and PA0 both at PreemptionPriority=1. Same preemption value → they cannot interrupt each other. If both schedule an interrupt while pending, execution order is decided by SubPriority instead. (cream bun)
