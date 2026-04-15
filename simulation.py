"""
Transient Simulation Engine

Orchestrates the full VMD system simulation over time.
"""

import numpy as np
from typing import Dict, List, Tuple
from tank_model import SolarThermalTank
from solar_input import SolarInput
from multi_effect import MultiEffectVMD


class VMDSimulation:
    """
    Main simulation engine for solar-powered multi-effect VMD system.
    
    Simulates thermal and mass transfer dynamics over time.
    """
    
    def __init__(
        self,
        # Tank parameters
        tank_mass: float = 100.0,
        initial_temperature: float = 25.0,
        ambient_temperature: float = 25.0,
        heat_loss_coefficient: float = 5.0,
        
        # Solar parameters
        solar_intensity: float = 800.0,
        solar_area: float = 20.0,
        enable_clouds: bool = False,
        
        # VMD parameters
        num_effects: int = 3,
        membrane_area_per_effect: float = 10.0,
        membrane_coefficient: float = 1e-7,
        vacuum_pressure: float = 100.0,
        temperature_drop_per_stage: float = 5.0,
    ):
        """
        Initialize VMD simulation system.
        
        Args:
            tank_mass: Solar tank mass (kg)
            initial_temperature: Initial tank temperature (°C)
            ambient_temperature: Ambient temperature (°C)
            heat_loss_coefficient: Heat loss coefficient (W/K)
            solar_intensity: Peak solar intensity (W/m²)
            solar_area: Solar collector area (m²)
            enable_clouds: Enable cloud fluctuations
            num_effects: Number of VMD effects
            membrane_area_per_effect: Membrane area per effect (m²)
            membrane_coefficient: Membrane coefficient
            vacuum_pressure: Vacuum pressure (Pa)
            temperature_drop_per_stage: Temperature drop per stage (°C)
        """
        # Tank
        self.tank = SolarThermalTank(
            mass=tank_mass,
            initial_temperature=initial_temperature,
            ambient_temperature=ambient_temperature,
            heat_loss_coefficient=heat_loss_coefficient
        )
        
        # Solar input
        self.solar_input = SolarInput(
            solar_intensity=solar_intensity,
            enable_clouds=enable_clouds
        )
        self.solar_collector_area = solar_area
        
        # Multi-effect VMD
        self.vmd = MultiEffectVMD(
            num_effects=num_effects,
            membrane_area_per_effect=membrane_area_per_effect,
            membrane_coefficient=membrane_coefficient,
            vacuum_pressure=vacuum_pressure,
            temperature_drop_per_stage=temperature_drop_per_stage
        )
        
    def run_simulation(
        self,
        simulation_hours: float = 24.0,
        time_step_seconds: float = 60.0
    ) -> Dict:
        """
        Run transient simulation of the VMD system.
        
        Args:
            simulation_hours: Total simulation time (hours)
            time_step_seconds: Time step for numerical integration (seconds)
            
        Returns:
            Dictionary containing simulation results:
            {
                'time_hours': array of time points,
                'tank_temperature': array of tank temperatures,
                'solar_irradiance': array of solar inputs,
                'flux': array of fluxes,
                'distillate_rate': array of production rates,
                'cumulative_production': array of cumulative distillate,
                'temperatures_by_stage': list of temperature arrays per stage,
                'fluxes_by_stage': list of flux arrays per stage,
                'metrics': performance metrics
            }
        """
        # Initialize time arrays
        total_seconds = simulation_hours * 3600
        num_steps = int(total_seconds / time_step_seconds)
        
        time_hours = np.zeros(num_steps)
        tank_temps = np.zeros(num_steps)
        solar_irradiances = np.zeros(num_steps)
        fluxes = np.zeros(num_steps)
        distillate_rates = np.zeros(num_steps)
        cumulative_prod = np.zeros(num_steps)
        
        # Store per-stage data
        temps_by_stage = [np.zeros(num_steps) for _ in range(self.vmd.num_effects)]
        fluxes_by_stage = [np.zeros(num_steps) for _ in range(self.vmd.num_effects)]
        
        # Running totals
        total_energy_input = 0.0
        total_distillate = 0.0
        dt = time_step_seconds
        
        # Simulation loop
        for step in range(num_steps):
            t_hours = step * time_step_seconds / 3600.0
            time_hours[step] = t_hours
            
            # Current tank temperature
            tank_temps[step] = self.tank.T
            
            # Solar irradiance
            irradiance = self.solar_input.get_irradiance(t_hours)
            solar_irradiances[step] = irradiance
            
            # Heat from solar collector
            Q_solar = irradiance * self.solar_collector_area  # W
            total_energy_input += Q_solar * dt  # Integrate over time step
            
            # VMD production
            stg_temps, stg_fluxes, distillate_rate = self.vmd.compute_multi_effect_production(
                self.tank.T
            )
            
            # Heat extraction by VMD
            Q_vmd = self.vmd.compute_total_heat_extraction(self.tank.T)
            
            # Update tank temperature
            self.tank.update_temperature(Q_solar, Q_vmd, dt)
            
            # Store results
            fluxes[step] = np.mean(stg_fluxes) if stg_fluxes else 0.0
            distillate_rates[step] = distillate_rate
            total_distillate += distillate_rate * dt
            cumulative_prod[step] = total_distillate
            
            # Store per-stage data
            for i in range(self.vmd.num_effects):
                if i < len(stg_temps):
                    temps_by_stage[i][step] = stg_temps[i]
                if i < len(stg_fluxes):
                    fluxes_by_stage[i][step] = stg_fluxes[i]
        
        # Compute performance metrics
        metrics = {
            'total_water_produced_kg': total_distillate,
            'total_water_produced_liters': total_distillate,  # 1 kg ≈ 1 L for fresh water
            'total_water_produced_per_hour': total_distillate / simulation_hours,
            'average_flux': np.mean(fluxes[fluxes > 0]) if np.any(fluxes > 0) else 0.0,
            'peak_flux': np.max(fluxes) if np.any(fluxes > 0) else 0.0,
            'total_energy_input_J': total_energy_input,
            'total_energy_input_kWh': total_energy_input / 3.6e6,
            'final_temperature': self.tank.T,
            'max_temperature': np.max(tank_temps)
        }
        
        # GOR and SEC
        gor, sec = self.vmd.compute_gpp_gor(total_energy_input, total_distillate)
        metrics['gor'] = gor
        metrics['specific_energy_consumption_kWh_per_m3'] = sec
        
        # If water was produced, compute average energy per unit
        if total_distillate > 0:
            metrics['energy_per_kg_kWh'] = metrics['total_energy_input_kWh'] / total_distillate
        else:
            metrics['energy_per_kg_kWh'] = 0.0
        
        return {
            'time_hours': time_hours,
            'tank_temperature': tank_temps,
            'solar_irradiance': solar_irradiances,
            'flux': fluxes,
            'distillate_rate': distillate_rates,
            'cumulative_production': cumulative_prod,
            'temperatures_by_stage': temps_by_stage,
            'fluxes_by_stage': fluxes_by_stage,
            'metrics': metrics
        }
    
    def reset(self, initial_temperature: float):
        """Reset simulation to initial conditions."""
        self.tank.reset(initial_temperature)
