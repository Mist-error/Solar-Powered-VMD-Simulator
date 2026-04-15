"""
Quick test of the VMD simulation
"""

from simulation import VMDSimulation
import numpy as np

# Test simulation for a full 24-hour day (will see day/night cycle)
print("Running 24-hour test simulation...")
print("Note: Solar input is zero before 6 AM and after 6 PM\n")

sim = VMDSimulation(
    tank_mass=150.0,           # Larger tank holds heat better
    initial_temperature=20.0,  # Start cool
    ambient_temperature=20.0,
    heat_loss_coefficient=8.0,
    solar_intensity=900.0,     # Realistic peak
    solar_area=30.0,           # Decent collector size
    num_effects=3,
    membrane_area_per_effect=15.0,
    membrane_coefficient=1.5e-7,  # Slightly improved membrane
    vacuum_pressure=80.0       # Lower vacuum pressure
)

# Run for 24 hours with 10-minute time steps
results = sim.run_simulation(simulation_hours=24.0, time_step_seconds=600.0)

print("✓ Simulation completed successfully!")
print(f"\nResults Summary:")
print(f"  Total water produced: {results['metrics']['total_water_produced_kg']:.1f} kg")
print(f"  Average production rate: {results['metrics']['total_water_produced_per_hour']:.2f} kg/h")
print(f"  Max tank temperature: {results['metrics']['max_temperature']:.1f}°C")
print(f"  Final tank temperature: {results['metrics']['final_temperature']:.1f}°C")
print(f"  Peak membrane flux: {results['metrics']['peak_flux']:.2e} kg/(m²·s)")
print(f"  Average flux (when producing): {results['metrics']['average_flux']:.2e} kg/(m²·s)")
print(f"  Total energy input: {results['metrics']['total_energy_input_kWh']:.2f} kWh")
print(f"  GOR (Gain Output Ratio): {results['metrics']['gor']:.3f}")
print(f"  SEC (Specific Energy Consumption): {results['metrics']['specific_energy_consumption_kWh_per_m3']:.1f} kWh/m³")
print(f"\n✓ All systems operational!")
