
"""
Equipment data models for arc flash calculations.
Uses Pydantic for validation and serialization.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class EnclosureType(str, Enum):
    """IEEE 1584-2018 Enclosure Types"""
    VCB = "VCB"    # Vertical Circuit Breaker
    VCBB = "VCBB"  # VCB with Barriers
    HCB = "HCB"    # Horizontal Circuit Breaker
    VOA = "VOA"    # Vertical Open Air
    HOA = "HOA"    # Horizontal Open Air


class GroundingType(str, Enum):
    """System grounding configuration"""
    SOLIDLY_GROUNDED = "solidly_grounded"
    UNGROUNDED = "ungrounded"
    IMPEDANCE_GROUNDED = "impedance_grounded"


class EquipmentInput(BaseModel):
    """Input data for arc flash calculation"""
    
    name: str = Field(
        ..., 
        description="Equipment identifier",
        min_length=1,
        max_length=100
    )
    
    voltage: float = Field(
        ...,
        description="System voltage in Volts",
        gt=0,
        le=15000
    )
    
    bolted_fault_current: float = Field(
        ...,
        description="Three-phase bolted fault current in Amperes",
        gt=0,
        le=106000
    )
    
    working_distance: float = Field(
        ...,
        description="Working distance from arc source in inches",
        gt=0,
        le=120
    )
    
    enclosure_type: EnclosureType = Field(
        ...,
        description="Equipment enclosure configuration"
    )
    
    electrode_gap: float = Field(
        ...,
        description="Gap between electrodes in millimeters",
        gt=0,
        le=200
    )
    
    fault_clearing_time: float = Field(
        ...,
        description="Protective device clearing time in seconds",
        gt=0,
        le=2.0
    )
    
    grounding: GroundingType = Field(
        default=GroundingType.SOLIDLY_GROUNDED,
        description="System grounding type"
    )
    
    @field_validator('voltage')
    @classmethod
    def validate_voltage_range(cls, v: float) -> float:
        """Ensure voltage is in IEEE 1584-2018 valid range"""
        if v < 208:
            raise ValueError("Voltage must be at least 208V for IEEE 1584-2018")
        return v
    
    @field_validator('electrode_gap')
    @classmethod
    def validate_gap_for_voltage(cls, v: float, info) -> float:
        """Validate gap is appropriate for voltage level"""
        # This will be called after voltage validation
        # Additional cross-field validation can be added here
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Main Switchboard",
                    "voltage": 480,
                    "bolted_fault_current": 40000,
                    "working_distance": 24,
                    "enclosure_type": "VCB",
                    "electrode_gap": 32,
                    "fault_clearing_time": 0.05,
                    "grounding": "solidly_grounded"
                }
            ]
        }
    }


class CalculationResult(BaseModel):
    """Arc flash calculation results"""
    
    equipment_name: str
    incident_energy: float = Field(
        ...,
        description="Incident energy at working distance in cal/cm²"
    )
    arc_flash_boundary: float = Field(
        ...,
        description="Arc flash protection boundary in inches"
    )
    ppe_category: int = Field(
        ...,
        description="NFPA 70E PPE Category (0-4)",
        ge=0,
        le=4
    )
    arcing_current: float = Field(
        ...,
        description="Calculated arcing current in Amperes"
    )
    
    # Intermediate calculation values
    arc_duration: float = Field(
        ...,
        description="Arc duration (equals fault clearing time) in seconds"
    )
    correction_factor: float = Field(
        ...,
        description="Enclosure size correction factor"
    )
    
    # Warnings for user
    warnings: list[str] = Field(
        default_factory=list,
        description="Calculation warnings or notes"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "equipment_name": "Main Switchboard",
                    "incident_energy": 8.24,
                    "arc_flash_boundary": 48.3,
                    "ppe_category": 2,
                    "arcing_current": 34000,
                    "arc_duration": 0.05,
                    "correction_factor": 1.0,
                    "warnings": []
                }
            ]
        }
    }
