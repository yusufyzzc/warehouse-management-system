# Warehouse Management System

A Python-centric, event-driven application modeling warehouse operations such as inventory tracking, order processing and alerts. Includes an AGV controller and RFID sensor simulation for item movement.

for more information: https://medium.com/@yusufyzc/building-a-python-based-warehouse-management-system-using-event-driven-programming-6e5779c9913e

## Features
- **Inventory Tracker** manages item quantities, raises low-stock alerts.
- **Order Processor** handles new orders, approves them if stock is available.
- **AGV Controller** simulates an automated guided vehicle for item transfer.
- **RFID Sensor** detects arrivals/departures of stock items.
- **Alert System** logs and displays critical events (e.g., low stock or AGV errors).

## Structures 
1. **`agents/`** – Contains the main logic units (e.g., inventory, orders, alerts).
2. **`events/`** – Defines all event names and related constants.
3. **`models/`** – Houses data structures (`Item`, `Order`) used by the system.
4. **`event_bus.py`** – Dispatches events to registered listeners.
5. **`app.py`** – Orchestrates agent instantiation and (optionally) a GUI or CLI.

## Usage
1. **Clone** this repository:
   ```bash
   git clone https://github.com/yusufyzzc/warehouse-management-system.git

2. **to run project**:  
   ```bash
   python -m src.app

