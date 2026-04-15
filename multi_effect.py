"""
Multi-Effect VMD System

Simulates multiple VMD stages in series, with heat recovery between stages.
"""

import numpy as np
from typing import List, Tuple
from vmd_model import VMDModel


class MultiEffectVMD:
    """
    Simulates a multi-effect VMD system.
    
    Each stage receives reduced temperature and reuses latent heat from
    the previous stage for improved efficiency.
    """
    
    def __init__(
        self,
        num_effects: int = 3,
        membrane_area_per_effect: float = 10.0,
        membrane_coefficient: float = 1e-7,
        vacuum_pressure: float = 100.0,
        temperature_drop_per_stage: float = 5.0  # °C
    ):
        """
        Initialize multi-effect VMD system.
        
        Args:
            num_effects: Number of VMD effects (1-5)
            membrane_area_per_effect: Membrane area per stage (m²)
            membrane_coefficient: Membrane coefficient (kg/(m²·s·Pa))
            vacuum_pressure: Vacuum pressure (Pa)
            temperature_drop_per_stage: Temperature decrease per stage (°C)
        """
        self.num_effects = max(1, min(num_effects, 5))
        self.dT_stage = temperature_drop_per_stage
        
        # Create VMD models for each effect
        self.stages: List[VMDModel] = []
        for i in range(self.num_effects):
            vmd = VMDModel(
                membrane_area=membrane_area_per_effect,
                membrane_coefficient=membrane_coefficient,
                vacuum_pressure=vacuum_pressure
            )
            self.stages.append(vmd)
        
    def compute_multi_effect_production(
        self,
        T_feed: float
    ) -> Tuple[List[float], List[float], float]:
        """
        Compute distillate production across all effects.
        
        Each stage operates at reduced temperature relative to previous stage.
        
        Args:
            T_feed: Feed temperature to first stage (°C)
            
        Returns:
            tuple: (temperatures, fluxes, total_production_rate)
                - temperatures: List of temperatures in each stage (°C)
                - fluxes: List of fluxes in each stage (kg/(m²·s))
                - total_production_rate: Total distillate rate (kg/s)
        """
        temperatures = [T_feed]
        fluxes = []
        total_production = 0.0
        
        for i, stage in enumerate(self.stages):
            T_stage = T_feed - i * self.dT_stage
            
            # Ensure temperature is reasonable
            T_stage = max(T_stage, 5.0)  # Don't go below 5°C
            
            temperatures.append(T_stage)
            
            # Compute flux at this stage
            flux = stage.compute_flux(T_stage)
            fluxes.append(flux)
            
            # Production rate at this stage
            production = stage.compute_distillate_rate(T_stage)
            total_production += production
        
        return temperatures[:-1], fluxes, total_production
    
    def compute_total_heat_extraction(
        self,
        T_feed: float
    ) -> float:
        """
        Compute total heat extracted across all effects.
        
        Args:
            T_feed: Feed temperature to first stage (°C)
            
        Returns:
            Total heat extraction (W)
        """
        _, _, total_production = self.compute_multi_effect_production(T_feed)
        
        # Heat extraction (latent heat only)
        latent_heat = 2.45e6  # J/kg
        Q_total = total_production * latent_heat
        
        return Q_total
    
    def compute_gpp_gor(
        self,
        energy_input: float,
        distillate_produced: float
    ) -> Tuple[float, float]:
        """
        Compute Gain Output Ratio (GOR) and energy metrics.
        
        GOR = (total distillate produced × latent heat) / energy input
        
        Args:
            energy_input: Total energy input to system (J)
            distillate_produced: Total distillate produced (kg)
            
        Returns:
            tuple: (gor, specific_energy_consumption)
                - gor: Gain Output Ratio (unitless)
                - sec: Specific energy consumption (kWh/m³)
        """
        latent_heat = 2.45e6  # J/kg
        
        # GOR: ratio of heat used for evaporation to total energy input
        if energy_input > 0:
            heat_used = distillate_produced * latent_heat
            gor = heat_used / energy_input if energy_input > 0 else 0
        else:
            gor = 0
        
        # Specific energy consumption (kWh/m³)
        if distillate_produced > 0:
            volume_m3 = distillate_produced / 1000  # kg to m³ for fresh water
            energy_kWh = energy_input / 3.6e6  # J to kWh
            sec = energy_kWh / volume_m3 if volume_m3 > 0 else 0
        else:
            sec = 0
        
        return gor, sec
