"""
Vacuum Membrane Distillation (VMD) Model

Models permeate flux and distillate production based on vapor pressure difference.
"""

import numpy as np


class VMDModel:
    """
    Simulates Vacuum Membrane Distillation.
    
    Computes permeate flux: J = C * (P_feed - P_vacuum)
    where P_feed is vapor pressure at feed temperature.
    """
    
    def __init__(
        self,
        membrane_area: float,
        membrane_coefficient: float = 1e-7,  # kg/(m²·s·Pa)
        vacuum_pressure: float = 100.0  # Pa
    ):
        """
        Initialize VMD model.
        
        Args:
            membrane_area: Membrane surface area (m²)
            membrane_coefficient: Membrane permeability coefficient (kg/(m²·s·Pa))
            vacuum_pressure: Vacuum pressure on permeate side (Pa)
        """
        self.A = membrane_area
        self.C = membrane_coefficient
        self.P_vac = vacuum_pressure
        
    def vapor_pressure_water(self, T: float) -> float:
        """
        Compute vapor pressure of water using Antoine equation.
        
        Valid for 0-60°C
        
        Args:
            T: Temperature (°C)
            
        Returns:
            Vapor pressure (Pa)
        """
        # Antoine equation: log10(P) = A - B / (C + T)
        # Coefficients for water (0-60°C)
        A = 8.07131
        B = 1730.63
        C = 233.426
        
        log_P = A - B / (C + T)
        P_Pa = 10 ** log_P * 133.322  # Convert mmHg to Pa
        
        return max(0.1, P_Pa)  # Avoid zero pressure
    
    def compute_flux(self, T_feed: float) -> float:
        """
        Compute permeate flux.
        
        J = C * (P_feed - P_vacuum)
        
        Args:
            T_feed: Feed temperature (°C)
            
        Returns:
            Membrane flux (kg/(m²·s))
        """
        P_feed = self.vapor_pressure_water(T_feed)
        
        # Pressure difference (only positive difference produces flux)
        dP = max(0, P_feed - self.P_vac)
        
        # Flux = coefficient × pressure difference
        flux = self.C * dP
        
        return flux
    
    def compute_distillate_rate(self, T_feed: float) -> float:
        """
        Compute distillate production rate per unit time.
        
        Production rate = flux × area
        
        Args:
            T_feed: Feed temperature (°C)
            
        Returns:
            Distillate production rate (kg/s)
        """
        flux = self.compute_flux(T_feed)
        production_rate = flux * self.A
        
        return production_rate
    
    def compute_vmd_heat_extraction(self, T_feed: float, distillate_rate: float) -> float:
        """
        Compute heat extracted by VMD process.
        
        This includes both sensible heat and latent heat of vaporization.
        Latent heat of vaporization for water ≈ 2.45 MJ/kg
        
        Args:
            T_feed: Feed temperature (°C)
            distillate_rate: Distillate production rate (kg/s)
            
        Returns:
            Heat extracted (W)
        """
        latent_heat = 2.45e6  # J/kg (latent heat of vaporization)
        
        # Heat extraction = production rate × latent heat
        # (Simplified: only latent heat, sensible heat is smaller)
        Q_extraction = distillate_rate * latent_heat
        
        return Q_extraction
