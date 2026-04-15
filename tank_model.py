"""
Solar Thermal Tank Model

Models the dynamics of a solar thermal tank with heat input, losses, and extraction.
"""

import numpy as np
from typing import Tuple


class SolarThermalTank:
    """
    Simulates temperature dynamics in a solar thermal tank.
    
    dT/dt = (Q_solar - Q_loss - Q_VMD) / (m * Cp)
    """
    
    def __init__(
        self,
        mass: float,
        cp: float = 4186,  # Specific heat capacity of water (J/kg·K)
        initial_temperature: float = 25.0,
        ambient_temperature: float = 25.0,
        heat_loss_coefficient: float = 5.0  # W/K
    ):
        """
        Initialize the solar thermal tank.
        
        Args:
            mass: Tank mass (kg)
            cp: Specific heat capacity of water (J/kg·K)
            initial_temperature: Initial tank temperature (°C)
            ambient_temperature: Ambient temperature (°C)
            heat_loss_coefficient: Heat loss coefficient (W/K)
        """
        self.mass = mass
        self.cp = cp  # J/kg·K
        self.T = initial_temperature  # Current temperature (°C)
        self.T_ambient = ambient_temperature
        self.h_loss = heat_loss_coefficient  # W/K
        
    def compute_heat_loss(self) -> float:
        """
        Compute heat loss to environment: Q_loss = h_loss * (T - T_ambient)
        
        Returns:
            Heat loss (W)
        """
        return self.h_loss * (self.T - self.T_ambient)
    
    def update_temperature(
        self,
        Q_solar: float,
        Q_vmd: float,
        dt: float
    ) -> float:
        """
        Update tank temperature using Euler's method.
        
        dT/dt = (Q_solar - Q_loss - Q_vmd) / (m * Cp)
        
        Args:
            Q_solar: Solar heat input (W)
            Q_vmd: Heat extracted by VMD (W)
            dt: Time step (seconds)
            
        Returns:
            Updated temperature (°C)
        """
        Q_loss = self.compute_heat_loss()
        
        # Energy balance: dE = Q_solar - Q_loss - Q_vmd
        # dT = dE / (m * Cp)
        dT = (Q_solar - Q_loss - Q_vmd) / (self.mass * self.cp) * dt
        
        self.T = self.T + dT
        
        # Prevent temperature from going below ambient
        self.T = max(self.T, self.T_ambient)
        
        return self.T
    
    def reset(self, initial_temperature: float):
        """Reset tank to initial conditions."""
        self.T = initial_temperature
