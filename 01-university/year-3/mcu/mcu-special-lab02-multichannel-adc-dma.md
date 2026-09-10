---
title: Special Lab 02 — Multichannel ADC with DMA
tags: [mcu, adc, dma, uart, stm32]
status: active
updated: 2026-09-08
subject: mcu
---

# Special Lab 02 — Multichannel ADC with DMA

## Task

- 2 potentiometers, each wired to 4 ADC1 channels (8 total)
- DMA transfers all 8 values into `adc_buf[8]`
- Half-transfer complete → LD2 ON
- Full-transfer complete → LD2 OFF
- Print values over UART3 (115200 baud)

## Channel mapping

| Rank | Channel | Pin | Pot  |     |
| ---- | ------- | --- | ---- | --- |
| 1    | CH0     | PA0 | POT1 |     |
| 2    | CH3     | PA3 | POT1 |     |
| 3    | CH6     | PA6 | POT1 |     |
| 4    | CH8     | PB0 | POT1 |     |
| 5    | CH9     | PB1 | POT2 |     |
| 6    | CH10    | PC0 | POT2 |     |
| 7    | CH12    | PC2 | POT2 |     |
| 8    | CH13    | PC3 | POT2 |     |

## Key config (ioc)

- ADC1: Scan mode, Continuous, 8 conversions, DMA Continuous Requests ON
- DMA2 Stream0: ADC1, circular, word width
- USART3: Async 115200 — maps to STLink VCP (PD8/PD9) for serial output
- Resolution: 12-bit → values 0–4095

## Final code pattern

```c
/* USER CODE BEGIN 2 */
HAL_UART_Transmit(&huart3, (uint8_t*)"START\r\n", 7, 100); // test
HAL_ADC_Start_DMA(&hadc1, adc_buf, 8);
/* USER CODE END 2 */
```

```c
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc)
{
  if (hadc->Instance == ADC1)
    HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
  if (hadc->Instance == ADC1) {
    HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);
    char buf[128];
    int len = sprintf(buf,
        "POT1: %4lu %4lu %4lu %4lu | POT2: %4lu %4lu %4lu %4lu\r\n",
        adc_buf[0], adc_buf[1], adc_buf[2], adc_buf[3],
        adc_buf[4], adc_buf[5], adc_buf[6], adc_buf[7]);
    HAL_UART_Transmit(&huart3, (uint8_t*)buf, len, 200);
  }
}
```

## Verification

- Serial terminal (115200) on STLink VCP → values print every DMA cycle
- Turn POT1 → `adc_buf[0..3]` change, `[4..7]` stable
- Turn POT2 → `adc_buf[4..7]` change, `[0..3]` stable
- Live Expressions in CubeIDE debugger also works if no serial app available
- LD2 toggles at ADC speed — too fast for naked eye; correct in hardware

## Related

- [[mcu-lab05-adc]] — single-channel ADC baseline
- [[mcu-stm32-log]]
