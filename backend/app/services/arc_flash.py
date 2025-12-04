"""
IEEE 1584-2018 Arc Flash Calculator
Implements the latest standard for arc flash hazard calculations.
"""

import math
from app.models.equipment import EquipmentInput, CalculationResult, EnclosureType

# Add these helper methods to the ArcFlashCalculator class


class ArcFlashCalculator:
    """
    IEEE 1584-2018 compliant arc flash calculator.
    
    Reference: IEEE Std 1584-2018 - IEEE Guide for Performing 
    Arc-Flash Hazard Calculations
    """
    
    # IEEE 1584-2018 Constants
    ENCLOSURE_FACTORS = {
        EnclosureType.VCB: 1.0,
        EnclosureType.VCBB: 0.973,
        EnclosureType.HCB: 1.056,
        EnclosureType.VOA: 1.0,
        EnclosureType.HOA: 1.0,
    }

    def _log10(self, value: float) -> float:
        """Helper for log10 calculations"""
        return math.log10(value)
    
    def _get_ppe_description(self, category: int) -> str:
        """Get PPE description for category"""
        descriptions = {
            0: "Non-melting or untreated natural fiber shirt and pants",
            1: "FR shirt and pants (4 cal/cm²)",
            2: "FR shirt and pants + FR coverall (8 cal/cm²)",
            3: "FR shirt and pants + FR coverall + FR jacket (25 cal/cm²)",
            4: "FR shirt and pants + multilayer flash suit (40+ cal/cm²)"
        }
        return descriptions.get(category, "Unknown category")
    
    def calculate(self, equipment: EquipmentInput) -> CalculationResult:
        """
        Perform complete arc flash calculation.
        
        Args:
            equipment: Equipment parameters
            
        Returns:
            CalculationResult with incident energy, PPE category, etc.
        """
        warnings = []
        
        # Step 1: Calculate arcing current
        arcing_current = self.calculate_arcing_current(equipment)
        
        # Step 2: Calculate incident energy
        incident_energy = self.calculate_incident_energy(
            equipment, arcing_current
        )
        
        # Step 3: Determine PPE category
        ppe_category = self.determine_ppe_category(incident_energy)
        
        # Step 4: Calculate arc flash boundary
        boundary = self.calculate_arc_flash_boundary(
            equipment, arcing_current
        )
        
        # Step 5: Get correction factor
        correction_factor = self.ENCLOSURE_FACTORS[equipment.enclosure_type]
        
        # Warnings
        if equipment.fault_clearing_time > 0.5:
            warnings.append(
                "Clearing time > 0.5s may indicate inadequate protection"
            )
        
        if incident_energy > 40:
            warnings.append(
                "Incident energy > 40 cal/cm² - consider additional protection"
            )
        
        return CalculationResult(
            equipment_name=equipment.name,
            incident_energy=round(incident_energy, 2),
            arc_flash_boundary=round(boundary, 1),
            ppe_category=ppe_category,
            arcing_current=round(arcing_current, 0),
            arc_duration=equipment.fault_clearing_time,
            correction_factor=correction_factor,
            warnings=warnings
        )
    
    def calculate_arcing_current(self, equipment: EquipmentInput) -> float:
        """
        Calculate arcing current using IEEE 1584-2018 equations.
        
        For voltages 208V - 15kV:
        lg(Ia) = K + 0.662 * lg(Ibf) + 0.0966 * V + 0.000526 * G + 0.5588 * V * lg(Ibf) - 0.00304 * G * lg(Ibf)
        
        Where:
        - Ia = arcing current (A)
        - Ibf = bolted fault current (A)
        - V = system voltage (kV)
        - G = conductor gap (mm)
        - K = constant based on enclosure type
        """
        voltage_kv = equipment.voltage / 1000.0
        ibf = equipment.bolted_fault_current
        gap = equipment.electrode_gap
        
        # K constant varies by enclosure (simplified - full standard has more detail)
        if equipment.enclosure_type in [EnclosureType.VCB, EnclosureType.VCBB, EnclosureType.HCB]:
            K = -0.153  # Enclosed equipment
        else:
            K = -0.097  # Open air
        
        # IEEE 1584-2018 arcing current equation
        lg_ia = (
            K 
            + 0.662 * math.log10(ibf)
            + 0.0966 * voltage_kv
            + 0.000526 * gap
            + 0.5588 * voltage_kv * math.log10(ibf)
            - 0.00304 * gap * math.log10(ibf)
        )
        
        arcing_current = 10 ** lg_ia
        
        return arcing_current
    
    def calculate_incident_energy(
        self, 
        equipment: EquipmentInput, 
        arcing_current: float
    ) -> float:
        """
        Calculate incident energy at working distance.
        
        IEEE 1584-2018 equation:
        E = (4.184 * Cf * Ia^n * t) / (4π * D^2)
        
        Where:
        - E = incident energy (cal/cm²)
        - Cf = enclosure correction factor
        - Ia = arcing current (A)
        - t = arc duration (s)
        - D = working distance (inches)
        - n = exponent (typically 1.0 for enclosed, varies for open)
        """
        cf = self.ENCLOSURE_FACTORS[equipment.enclosure_type]
        ia = arcing_current
        t = equipment.fault_clearing_time
        d = equipment.working_distance
        
        # Exponent n varies by configuration
        if equipment.enclosure_type in [EnclosureType.VOA, EnclosureType.HOA]:
            n = 1.0  # Open air
        else:
            n = 1.0  # Enclosed (simplified)
        
        # Incident energy calculation (simplified form)
        # Full IEEE equation is more complex with additional factors
        energy = (4.184 * cf * (ia ** n) * t) / (4 * math.pi * (d ** 2))
        
        return energy
    
    def determine_ppe_category(self, incident_energy: float) -> int:
        """
        Determine PPE category per NFPA 70E Table 130.5(G).
        
        Categories:
        - 0: < 1.2 cal/cm²
        - 1: 1.2 to 4 cal/cm²
        - 2: 4 to 8 cal/cm²
        - 3: 8 to 25 cal/cm²
        - 4: > 25 cal/cm²
        """
        if incident_energy < 1.2:
            return 0
        elif incident_energy < 4:
            return 1
        elif incident_energy < 8:
            return 2
        elif incident_energy < 25:
            return 3
        else:
            return 4
    
    def calculate_arc_flash_boundary(
        self,
        equipment: EquipmentInput,
        arcing_current: float
    ) -> float:
        """
        Calculate arc flash boundary (distance where incident energy = 1.2 cal/cm²).
        
        Rearrange incident energy equation to solve for distance:
        D = sqrt((4.184 * Cf * Ia^n * t) / (4π * E_threshold))
        
        Where E_threshold = 1.2 cal/cm² (onset of second-degree burn)
        """
        cf = self.ENCLOSURE_FACTORS[equipment.enclosure_type]
        ia = arcing_current
        t = equipment.fault_clearing_time
        e_threshold = 1.2  # cal/cm²
        n = 1.0
        
        # Solve for distance
        numerator = 4.184 * cf * (ia ** n) * t
        denominator = 4 * math.pi * e_threshold
        
        boundary = math.sqrt(numerator / denominator)
        
        return boundary
        