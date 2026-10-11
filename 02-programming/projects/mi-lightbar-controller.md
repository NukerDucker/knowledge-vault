---
title: Mi Lightbar Controller
tags: [hardware]
status: active
updated: 2026-10-01
---

# Mi Lightbar Controller

Control Xiaomi Mi Computer Monitor Light Bar (MJGJD01YL) from PC via Home Assistant.

## Architecture

```
Mi Lightbar ←RF→ nRF24L01 ←SPI→ ESP32-C3 ←WiFi/MQTT→ HA Mosquitto → HA UI / mobile
```

## Hardware

| Part | Model | Cost |
|---|---|---|
| MCU | ESP32-C3 SuperMini | ~80 ฿ |
| RF module | Mini nRF24L01 | 55 ฿ × 2 |
| Capacitor | 100µF electrolytic | ~2 ฿ |

## Wiring (nRF24 → ESP32-C3)

| nRF24 | ESP32-C3 |
|---|---|
| CE | GPIO 4 |
| CSN | GPIO 5 |
| SCK | GPIO 18 |
| MOSI | GPIO 23 |
| MISO | GPIO 19 |
| VCC | 3.3V |
| GND | GND |

Add 100µF cap across VCC/GND on nRF24 — fixes power instability.

## Firmware

Repo: https://github.com/ebinf/lightbar2mqtt  
Tested device: MJGJD01YL only

Setup:
1. Clone repo, copy config example
2. Install 5 libs via Arduino IDE
3. Flash → serial monitor → note remote serial number
4. Update config with serial → reflash

## HA Setup

1. Install Home Assistant (Docker or Pi)
2. Add-on: Mosquitto broker
3. Integration: MQTT
4. lightbar2mqtt sends auto-discovery → light entity appears automatically

## State tracking

- HA tracks last command sent (assumed state)
- Physical remote presses detected via sensor entity
- Power unplug = state drift (acceptable tradeoff)
- Hardware fix possible: LDR on analog pin, not worth it for desk use

## MQTT topics

`<ROOT_TOPIC>/l2m_<MAC>/0x<SERIAL>/command`

Payload JSON: `{"state": "ON", "brightness": 0-15, "color_temp": 153-370}`

## Status

- [ ] Order hardware (ESP32-C3 SuperMini + 2× Mini nRF24L01 + 100µF cap)
- [ ] Flash firmware + get remote serial number
- [ ] HA + Mosquitto setup
- [ ] Verify light entity appears in HA
- [ ] Test from mobile + PC
