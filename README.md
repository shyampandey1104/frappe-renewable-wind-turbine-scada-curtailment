# Frappe Renewable Wind Farm SCADA Telemetry & Curtailment Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CleanTech](https://img.shields.io/badge/CleanTech-Wind%20Farm%20SCADA-green.svg)](https://mnre.gov.in)

Utility-scale renewable wind energy SCADA telemetry receiver, aerodynamic power curve modeling, and State Load Despatch Centre (SLDC) grid curtailment revenue loss calculator.

## Features
- **Aerodynamic Power Curve:** Evaluates theoretical generation against cut-in (3 m/s), rated (11.5 m/s), and cut-out (25 m/s) wind speeds.
- **SLDC Curtailment Loss Accounting:** Computes lost deemed generation (kWh) and deemed tariff revenue under grid congestion instructions.
- **PPA Settlement Ledger:** Automated generation of Regional Energy Account (REA) billing credits.

## Tests
```bash
python3 -m unittest discover tests
```
