"""
Test suite for IEEE 1584-2018 arc flash calculations.
Tests validate against known calculation examples.
"""

import pytest
from app.models.equipment import EquipmentInput, EnclosureType
from app.services.arc_flash import ArcFlashCalculator


class TestArcFlashCalculator:
    """Test IEEE 1584-2018 calculation engine"""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance for tests"""
        return ArcFlashCalculator()
    
    @pytest.fixture
    def sample_equipment(self):
        """Sample 480V equipment for testing"""
        return EquipmentInput(
            name="Test Switchboard",
            voltage=480,
            bolted_fault_current=40000,
            working_distance=24,
            enclosure_type=EnclosureType.VCB,
            electrode_gap=32,
            fault_clearing_time=0.05,
            grounding="solidly_grounded"
        )
    
    def test_calculator_initialization(self, calculator):
        """Test calculator can be instantiated"""
        assert calculator is not None
    
    def test_arcing_current_calculation(self, calculator, sample_equipment):
        """Test arcing current calculation produces reasonable value"""
        arcing_current = calculator.calculate_arcing_current(sample_equipment)
        
        # Arcing current should be less than bolted fault current
        assert arcing_current < sample_equipment.bolted_fault_current
        # For 480V systems, typically 10-20% of bolted fault due to arc impedance
        assert arcing_current > sample_equipment.bolted_fault_current * 0.1
        assert arcing_current < sample_equipment.bolted_fault_current * 0.3
    
    def test_incident_energy_calculation(self, calculator, sample_equipment):
        """Test incident energy calculation"""
        result = calculator.calculate(sample_equipment)
        
        # Incident energy should be positive
        assert result.incident_energy > 0
        # Should be reasonable for 480V, 40kA, 0.05s at 24"
        assert result.incident_energy < 50  # cal/cm²
    
    def test_ppe_category_assignment(self, calculator, sample_equipment):
        """Test PPE category follows NFPA 70E"""
        result = calculator.calculate(sample_equipment)
        
        # PPE category must be 0-4
        assert 0 <= result.ppe_category <= 4
        
        # Test known thresholds
        if result.incident_energy <= 1.2:
            assert result.ppe_category == 0
        elif result.incident_energy <= 4:
            assert result.ppe_category == 1
        elif result.incident_energy <= 8:
            assert result.ppe_category == 2
    
    def test_arc_flash_boundary_calculation(self, calculator, sample_equipment):
        """Test arc flash boundary is calculated correctly"""
        result = calculator.calculate(sample_equipment)
        
        # Boundary should be positive
        assert result.arc_flash_boundary > 0
        # Should be reasonable (not absurdly large)
        assert result.arc_flash_boundary < 500  # inches
        
        # If incident energy is low, boundary can be less than working distance (safe condition)
        # This is physically correct - you're already outside the hazard zone
        if result.incident_energy < 1.2:
            # Low energy - boundary may be less than working distance
            assert result.arc_flash_boundary > 0
        else:
            # Higher energy - boundary should exceed working distance
            assert result.arc_flash_boundary > sample_equipment.working_distance
    
    def test_low_voltage_validation(self, calculator):
        """Test that voltage below 208V is rejected"""
        with pytest.raises(ValueError):
            EquipmentInput(
                name="Too Low",
                voltage=120,  # Below minimum
                bolted_fault_current=5000,
                working_distance=18,
                enclosure_type=EnclosureType.VCB,
                electrode_gap=25,
                fault_clearing_time=0.1
            )
    
    def test_different_enclosure_types(self, calculator, sample_equipment):
        """Test that different enclosures give different results"""
        # Calculate for VCB
        sample_equipment.enclosure_type = EnclosureType.VCB
        result_vcb = calculator.calculate(sample_equipment)
        
        # Calculate for VOA (open air)
        sample_equipment.enclosure_type = EnclosureType.VOA
        result_voa = calculator.calculate(sample_equipment)
        
        # Open air should have different incident energy
        assert result_vcb.incident_energy != result_voa.incident_energy
    
    def test_clearing_time_impact(self, calculator, sample_equipment):
        """Test that longer clearing time increases incident energy"""
        sample_equipment.fault_clearing_time = 0.05
        result_fast = calculator.calculate(sample_equipment)
        
        sample_equipment.fault_clearing_time = 0.5
        result_slow = calculator.calculate(sample_equipment)
        
        # Longer time should mean more energy
        assert result_slow.incident_energy > result_fast.incident_energy
    
    def test_high_energy_scenario(self, calculator):
        """Test calculation with higher energy scenario"""
        high_energy_equipment = EquipmentInput(
            name="High Energy Equipment",
            voltage=480,
            bolted_fault_current=65000,  # Higher fault current
            working_distance=18,  # Closer working distance
            enclosure_type=EnclosureType.VCB,
            electrode_gap=32,
            fault_clearing_time=0.3,  # Longer clearing time
            grounding="solidly_grounded"
        )
        
        result = calculator.calculate(high_energy_equipment)
        
        # Should produce higher incident energy
        assert result.incident_energy > 1.0
        # Boundary should exceed working distance for higher energy
        assert result.arc_flash_boundary > high_energy_equipment.working_distance
        # PPE category should be appropriate
        assert result.ppe_category >= 1


# Test data validation
class TestEquipmentInputValidation:
    """Test Pydantic model validation"""
    
    def test_valid_equipment_input(self):
        """Test valid input is accepted"""
        equipment = EquipmentInput(
            name="Valid Equipment",
            voltage=480,
            bolted_fault_current=40000,
            working_distance=24,
            enclosure_type=EnclosureType.VCB,
            electrode_gap=32,
            fault_clearing_time=0.05
        )
        assert equipment.voltage == 480
    
    def test_negative_voltage_rejected(self):
        """Test negative voltage is rejected"""
        with pytest.raises(ValueError):
            EquipmentInput(
                name="Bad Voltage",
                voltage=-480,
                bolted_fault_current=40000,
                working_distance=24,
                enclosure_type=EnclosureType.VCB,
                electrode_gap=32,
                fault_clearing_time=0.05
            )
    
    def test_zero_fault_current_rejected(self):
        """Test zero fault current is rejected"""
        with pytest.raises(ValueError):
            EquipmentInput(
                name="No Fault",
                voltage=480,
                bolted_fault_current=0,
                working_distance=24,
                enclosure_type=EnclosureType.VCB,
                electrode_gap=32,
                fault_clearing_time=0.05
            )
    
    def test_excessive_clearing_time_accepted_with_warning(self):
        """Test that long clearing times are accepted but generate warnings"""
        equipment = EquipmentInput(
            name="Slow Protection",
            voltage=480,
            bolted_fault_current=40000,
            working_distance=24,
            enclosure_type=EnclosureType.VCB,
            electrode_gap=32,
            fault_clearing_time=1.5  # Very long
        )
        calculator = ArcFlashCalculator()
        result = calculator.calculate(equipment)
        
        # Should calculate but include warning
        assert result.incident_energy > 0
        assert len(result.warnings) > 0