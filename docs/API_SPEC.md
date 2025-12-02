# API Specification

## Base URL
```
Development: http://localhost:8000
Production: https://api.arcflash.studio
```

## Authentication

Currently no authentication (Phase 1).
Future: JWT tokens for user-specific projects.

## Endpoints

### POST /api/v1/calculate

Calculate arc flash incident energy for given equipment.

**Request Body:**
```json
{
  "equipment": {
    "name": "Main Switchboard",
    "voltage": 480,
    "bolted_fault_current": 40000,
    "working_distance": 24,
    "enclosure_type": "VCB",
    "electrode_gap": 32,
    "fault_clearing_time": 0.05,
    "grounding": "solidly_grounded"
  },
  "standard": "IEEE_1584_2018"
}
```

**Response (200 OK):**
```json
{
  "calculation_id": "calc_abc123",
  "equipment_name": "Main Switchboard",
  "results": {
    "incident_energy": 8.24,
    "incident_energy_unit": "cal/cm²",
    "arc_flash_boundary": 48.3,
    "boundary_unit": "inches",
    "ppe_category": 2,
    "arcing_current": 34000,
    "arcing_current_unit": "A"
  },
  "intermediate_values": {
    "arc_duration": 0.05,
    "correction_factor": 1.0,
    "enclosure_size_correction": 1.0
  },
  "warnings": [],
  "timestamp": "2024-12-02T10:30:00Z"
}
```

**Error Responses:**
```json
// 422 Validation Error
{
  "detail": [
    {
      "loc": ["body", "equipment", "voltage"],
      "msg": "Voltage must be between 208 and 15000 V",
      "type": "value_error"
    }
  ]
}

// 500 Calculation Error
{
  "detail": "Calculation did not converge. Check input parameters."
}
```

### GET /api/v1/equipment-library

Retrieve standard equipment configurations.

**Response (200 OK):**
```json
{
  "equipment": [
    {
      "id": "eq_001",
      "name": "480V Main Switchboard",
      "typical_voltage": 480,
      "typical_fault_range": [25000, 65000],
      "working_distance": 24,
      "enclosure_type": "VCB"
    }
  ]
}
```

### POST /api/v1/projects

Save a project with multiple equipment.

### GET /api/v1/projects

List all projects.

### GET /api/v1/projects/{project_id}

Get specific project details.

## Data Models

### Equipment

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Equipment identifier |
| voltage | number | Yes | System voltage (V) |
| bolted_fault_current | number | Yes | Available fault current (A) |
| working_distance | number | Yes | Distance from arc source (inches) |
| enclosure_type | enum | Yes | VCB, VCBB, HCB, VOA, HOA |
| electrode_gap | number | Yes | Conductor spacing (mm) |
| fault_clearing_time | number | Yes | Protection device time (seconds) |
| grounding | enum | No | solidly_grounded, ungrounded |

### Calculation Result

| Field | Type | Description |
|-------|------|-------------|
| incident_energy | number | Energy at working distance (cal/cm²) |
| arc_flash_boundary | number | Safe approach distance (inches) |
| ppe_category | integer | NFPA 70E category (0-4) |
| arcing_current | number | Calculated arc current (A) |

## Rate Limiting

- **Anonymous**: 100 requests/hour
- **Authenticated**: 1000 requests/hour

## Versioning

API versions are specified in the URL path (`/api/v1/`).
Breaking changes will increment the version number.

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid syntax |
| 422 | Unprocessable Entity - Validation failed |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Calculation failed |