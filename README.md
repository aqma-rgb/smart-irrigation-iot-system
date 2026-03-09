# Smart Irrigation System (Solar-Powered IoT)

## Overview

This project presents a low-voltage **IoT-based smart irrigation system powered by solar energy**.  
The system is designed to support small-to-medium farms, especially in off-grid environments, by automating irrigation using real-time environmental monitoring.

The system monitors **soil moisture, temperature, and humidity**, and automatically activates irrigation when soil moisture levels fall below a defined threshold. A **Real-Time Clock (RTC)** module is also used to support scheduled irrigation.

Remote monitoring and manual control are implemented through a **Node-RED dashboard**, allowing users to observe system performance and manage irrigation activities remotely.

---

## Key Features

- Automated irrigation based on soil moisture levels  
- Real-time monitoring of environmental conditions  
- Solar-powered system suitable for off-grid farms  
- Time-based irrigation scheduling using RTC  
- Remote monitoring and control via Node-RED dashboard  

---

## Hardware Components

- ESP32 Microcontroller  
- Soil Moisture Sensor  
- DHT Sensor (Temperature & Humidity)  
- DS3231 Real-Time Clock (RTC)  
- Relay Module  
- Water Pump  
- Solar Panel  

---

## System Architecture

The system collects environmental data using sensors connected to an ESP32 microcontroller.  
Based on the soil moisture level and scheduling conditions, the controller activates the irrigation pump through a relay module.

Sensor data is transmitted to a Node-RED dashboard for monitoring and remote control.

---

## Project Poster

The full project design, methodology, circuit diagram, and results are presented in the poster below.

[View Project Poster](smart_irrigation_poster.pdf)

---

## Conclusion

This project demonstrates a **low-cost and energy-efficient smart irrigation system** using IoT technology and solar power. By automating irrigation based on soil conditions and enabling remote monitoring, the system improves water efficiency and reduces manual labor for small-scale farms.

---

## Author

Muhammad Aqma Farhan  
Bachelor in Information Technology (Internet of Things)  
