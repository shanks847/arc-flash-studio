---
sidebar_position: 1
---

# Introduction

Welcome to **Arc Flash Studio** - a modern, open-source arc flash calculator built for electrical engineers.

## What is Arc Flash?

An arc flash is an explosive release of energy caused by an electric arc. The incident energy can cause severe burns and injuries. OSHA and NFPA 70E require arc flash analysis for electrical systems.

## Why Arc Flash Studio?

### 🎯 IEEE 1584-2018 Compliant
Full implementation of the latest IEEE standard for arc flash calculations, including all correction factors and equipment configurations.

### 🌐 Web-Based & Modern
No software installation required. Works on any device with a web browser. Clean, intuitive interface.

### 🔓 Open Source & Transparent
- See exactly how calculations are performed
- Validate against your own test cases
- Contribute improvements
- No vendor lock-in

### ⚡ Fast & Accurate
- Real-time validation
- Instant calculations
- Results you can trust

## Key Features

- **Equipment Library**: Pre-configured common equipment
- **Multi-Equipment Systems**: Analyze entire facilities
- **Report Generation**: Professional PDF reports and arc flash labels
- **Project Management**: Save and organize your work
- **API Access**: Integrate with other tools

## Who Should Use This?

- Electrical engineers performing arc flash studies
- Facility managers ensuring workplace safety
- Students learning power systems analysis
- Researchers validating calculation methods

## Standards Compliance

Arc Flash Studio implements:
- **IEEE 1584-2018**: Guide for Performing Arc-Flash Hazard Calculations
- **NFPA 70E**: Standard for Electrical Safety in the Workplace
- **NEC Article 110.16**: Flash Protection requirements

## Quick Example
```json
// Simple API request
POST /api/v1/calculate
{
  "equipment": {
    "voltage": 480,
    "bolted_fault_current": 40000,
    "working_distance": 24,
    "enclosure_type": "VCB"
  }
}

// Response
{
  "incident_energy": 8.24,  // cal/cm²
  "ppe_category": 2,
  "arc_flash_boundary": 48  // inches
}
```

## Architecture

Arc Flash Studio uses a modern three-tier architecture:

![System Architecture](/img/system-architecture.svg)

- **Frontend**: React-based web interface
- **Backend**: FastAPI with PandaPower integration
- **Calculation Engine**: Pure Python implementation of IEEE 1584-2018

## Getting Started

Ready to dive in? Check out our [Quick Start Guide](./getting-started/installation.md).

## Open Source

This project is MIT licensed and welcomes contributions. See our [Contributing Guide](./contributing/overview.md).

:::warning Safety Disclaimer
Arc Flash Studio is for educational and reference purposes. Always consult with qualified electrical engineers for safety-critical calculations. The authors assume no liability for use of this software.
:::