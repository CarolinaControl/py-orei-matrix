# py-orei-matrix
A custom pyscript solution for the OREI matrix (OREI HDS-808) for Home Assistant.  This script uses the device's TCP/IP control protocol on Port 8000 (default) to send ASCII commands. It exposes services to Home Assistant that you can use in dashboards and automations.

# OREI HDS-808 HDMI Matrix Control for Home Assistant

A custom **[Pyscript](https://github.com/custom-components/pyscript)** integration to control the **OREI HDS-808 8x8 HDMI Matrix** via TCP/IP.

This integration allows you to switch inputs/outputs, control power, and sync status directly from your Home Assistant dashboard without needing IR blasters or complex RS232 adapters.

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom-blue) ![Pyscript](https://img.shields.io/badge/Made%20for-Pyscript-yellow)

## Features

* **Matrix Routing:** Route any of the 8 HDMI inputs to any of the 8 HDMI outputs.
* **Power Control:** Turn the matrix ON or OFF remotely.
* **Two-Way Feedback:** Reads the current status of the matrix to keep Home Assistant UI in sync (e.g., if someone uses the physical remote).

## Prerequisites

1.  **OREI HDS-808 Matrix** connected to your network via Ethernet.
2.  **Home Assistant** instance.
3.  **[Pyscript](https://github.com/custom-components/pyscript)** installed (available via HACS).

## Installation

### Step 1: Install Pyscript
If you haven't already, install **Pyscript** from HACS:
1.  Go to HACS > Integrations > Explore > Search for "Pyscript".
2.  Install and restart Home Assistant.

### Step 2: Add the Script
1.  Navigate to your Home Assistant config folder (using File Editor or VS Code).
2.  Upload `orei_matrix.py` inside the `pyscript/` folder.

## Usage

### Services
The integration exposes the following services you can use in automations:\

* service `pyscript.orei_set_route`: Switch inputs.
    * `input_id`: 1-8
    * `output_id`: 1-8 (or 0 for All)
* service `pyscript.orei_power`: Turn matrix on/off.
    * `power_state`: "on" or "off"
* service `pyscript.orei_refresh_status`: Force a status update from the matrix.

### Dashboard Configuration

To control the matrix from your Home Assistant dashboard, you can use a **Vertical Stack** containing **Grid Cards**. This creates a clean, remote-like interface for each output.

```yaml
type: vertical-stack
title: HDMI Matrix Control
cards:
  # --- CONTROLS FOR TV 1 (OUTPUT 1) ---
  - type: custom:text-divider-row # Optional, or just use markdown
    text: "TV 1 - Living Room"
  - type: grid
    columns: 4
    square: false
    cards:
      - type: button
        name: Apple TV (In 1)
        icon: mdi:apple
        tap_action:
          action: call-service
          service: pyscript.orei_set_route
          service_data:
            input_id: 1
            output_id: 1
      - type: button
        name: PS5 (In 2)
        icon: mdi:controller
        tap_action:
          action: call-service
          service: pyscript.orei_set_route
          service_data:
            input_id: 2
            output_id: 1
      - type: button
        name: Cable (In 3)
        icon: mdi:television-box
        tap_action:
          action: call-service
          service: pyscript.orei_set_route
          service_data:
            input_id: 3
            output_id: 1
      - type: button
        name: PC (In 4)
        icon: mdi:laptop
        tap_action:
          action: call-service
          service: pyscript.orei_set_route
          service_data:
            input_id: 4
            output_id: [1, 2] # Direct routing array grouping      # ... Repeat buttons for Inputs 5-8 if needed ...

  # --- REPEAT THE GRID ABOVE FOR TV 2, TV 3, ETC. ---
```
### Troubleshooting
* Status says "Unknown":
   * The matrix hasn't been polled yet. Click the "Refresh Status" service or wait for the startup trigger.
* Connection Refused:
   * Ensure the Matrix IP is static and correct. Try changing PORT = 8000 to PORT = 23 in orei_matrix.py if 8000 fails.

### Disclaimer
This is a community project and is not affiliated with OREI. Use at your own risk.
