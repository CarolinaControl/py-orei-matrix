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
* **Native UI:** Uses Home Assistant `select` entities for a clean dropdown interface.

## Prerequisites

1.  **OREI HDS-808 Matrix** connected to your network via Ethernet.
2.  **Home Assistant** instance.
3.  **[Pyscript](https://github.com/custom-components/pyscript)** installed (available via HACS).

## Installation

### Step 1: Install Pyscript
If you haven't already, install **Pyscript** from HACS:
1.  Go to HACS > Integrations > Explore > Search for "Pyscript".
2.  Install and restart Home Assistant.

### Step 2: Add
1.  Navigate to your Home Assistant config folder (using File Editor or VS Code).
2.  Upload `orei_matrix.py` inside the `pyscript/` folder.
