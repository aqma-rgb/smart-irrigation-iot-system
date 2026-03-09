# Smart Irrigation System (Solar-Powered IoT)

## Overview

This project is an IoT-based smart irrigation system designed to automate agricultural watering.  
The system monitors soil moisture levels and automatically activates water pumps when soil moisture drops below a threshold.

The system also uses a Real-Time Clock (RTC) module to enable scheduled irrigation.

---

## Features

- Automated irrigation based on soil moisture levels
- RTC-based irrigation scheduling
- Real-time monitoring of environmental conditions
- Energy-efficient solar-powered design
- IoT-based system architecture

---

## Hardware Components

- ESP32 Microcontroller
- Soil Moisture Sensor
- DS3231 RTC Module
- Relay Module
- Water Pump
- Solar Panel

---

## Software

- MicroPython / Python
- IoT communication protocols
- Sensor monitoring logic

---

## System Architecture

```mermaid
flowchart LR

SoilSensor --> ESP32
RTC --> ESP32
ESP32 --> Relay
Relay --> WaterPump
ESP32 --> IoT_Dashboard
SolarPanel --> Power_System
Power_System --> ESP32
