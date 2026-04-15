# Solar-Powered Multi-Effect VMD Simulator

A Python-based simulation tool with an interactive GUI for modeling solar-powered Vacuum Membrane Distillation (VMD) systems.

## Overview

This project simulates a **multi-effect vacuum membrane distillation system** powered by solar thermal energy. It includes:

- **Transient thermal modeling** of a solar thermal tank
- **Time-dependent solar input** with day/night cycles and optional cloud effects
- **Multi-stage VMD simulation** with heat recovery between effects
- **Real-time performance metrics** (GOR, specific energy consumption, water production)
- **Interactive Streamlit GUI** for parameter tuning and visualization

## Project Structure

```
VMD Project/
├── tank_model.py           # Solar thermal tank dynamics
├── solar_input.py          # Solar irradiance modeling
├── vmd_model.py            # Vacuum membrane distillation core model
├── multi_effect.py         # Multi-effect system and efficiency metrics
├── simulation.py           # Main transient simulation engine
├── app.py                  # Streamlit GUI application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## Installation

### 1. Create a Virtual Environment (Recommended)

```bash
cd "c:\Users\NANNU\Desktop\VMD Project"
python -m venv venv
venv\Scripts\activate  # On Windows
# Or on macOS/Linux:
# source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Simulation

### Launch the Interactive GUI

```bash
streamlit run app.py
```

This opens a web-based interface at `http://localhost:8501` where you can:
- Adjust all system parameters via sliders and inputs
- Run simulations with different configurations
- View real-time performance metrics
- Export results to CSV

## System Components

### 1. **Solar Thermal Tank** (`tank_model.py`)
- Models temperature dynamics using energy balance
- Accounts for solar input, heat losses, and VMD extraction
- Equation: `dT/dt = (Q_solar - Q_loss - Q_VMD) / (m * Cp)`

### 2. **Solar Input** (`solar_input.py`)
- Time-dependent solar irradiance (W/m²)
- Day/night cycle simulation
- Optional cloud fluctuations

### 3. **VMD Model** (`vmd_model.py`)
- Vapor pressure calculation (Antoine equation)
- Permeate flux computation: `J = C * (P_feed - P_vacuum)`
- Heat extraction modeling

### 4. **Multi-Effect System** (`multi_effect.py`)
- Simulates 1-5 VMD stages in series
- Configurable temperature drop between stages
- Total production and GOR calculations

### 5. **Simulation Engine** (`simulation.py`)
- Integrates all components
- Time-stepped numerical integration
- Computes performance metrics over simulation period

## Key Features

### Input Parameters (Via GUI)

**Tank Configuration:**
- Tank mass, initial temperature, ambient temperature
- Heat loss coefficient

**Solar Collector:**
- Solar intensity (W/m²)
- Collector area (m²)
- Cloud effect toggle

**VMD System:**
- Number of effects (1-5)
- Membrane area per effect
- Membrane coefficient
- Vacuum pressure
- Temperature drop per stage

**Simulation:**
- Simulation duration (1-72 hours)
- Time step (30-300 seconds)

### Output Metrics

- **Total water produced** (kg/h, liters)
- **Membrane flux** (kg/(m²·s))
- **Gain Output Ratio (GOR)** - efficiency metric
- **Specific Energy Consumption (SEC)** (kWh/m³)
- **Tank temperature profiles**
- **Solar irradiance patterns**
- **Cumulative and instantaneous production rates**

### Visualizations

- Tank temperature vs. time
- Solar irradiance vs. time
- Membrane flux vs. time
- Water production rate and cumulative production
- All plots are interactive (zoom, pan, hover data)

### Export

- Export all results and parameters to CSV
- Includes time series data and summary metrics

## Physics & Assumptions

### Key Equations

**Tank Energy Balance:**
```
dT/dt = (Q_solar - Q_loss - Q_VMD) / (m * Cp)
```

**VMD Flux:**
```
J = C * (P_feed - P_vacuum)
where P_feed = vapor_pressure(T_feed)
```

**Vapor Pressure (Antoine):**
```
log10(P) = A - B / (C + T)
(valid for 0-60°C)
```

**GOR (Gain Output Ratio):**
```
GOR = (distillate × latent_heat) / energy_input
```

### Assumptions

1. Water properties are constant (Cp = 4186 J/kg·K)
2. Latent heat of vaporization = 2.45 MJ/kg
3. Membrane surface remains constant
4. No fouling or degradation during simulation
5. Linear temperature drop across effects
6. Vapor pressure follows Antoine equation

## Example Usage

1. **Click "Run Simulation"** with default parameters to see typical 24-hour operation
2. **Increase solar intensity** to see effect on tank temperature and production
3. **Adjust membrane area** to explore scaling effects
4. **Vary number of effects** to see multi-stage benefits
5. **Enable cloud effects** to see realistic variations
6. **Export results** to CSV for external analysis

## Extending the Code

### Add New Features

**To add parameter sensitivity analysis:**
- Modify `app.py` to run multiple simulations
- Store results and create comparison plots

**To add more solar models:**
- Extend `SolarInput` class with alternative irradiance functions

**To improve VMD model accuracy:**
- Update Antoine coefficients for different temperature ranges
- Add temperature-dependent membrane coefficient
- Include fouling/degradation effects

**To add material balance:**
- Track feed salinity and reject concentration
- Model salt rejection during distillation

## Technical Specifications

- **Language:** Python 3.x
- **Numerical Integration:** Euler's method (simple, stable for small dt)
- **Plotting:** Plotly (interactive) + integration with Streamlit
- **Data Export:** CSV format

## Troubleshooting

**"ModuleNotFoundError" when running app.py:**
- Ensure all imports are available: `pip install -r requirements.txt`
- Check virtual environment is activated

**Slow performance:**
- Decrease simulation duration or increase time step
- Reduce number of historical points plotted

**Zero water production:**
- Increase solar intensity or tank mass
- Check that vacuum pressure is lower than feed vapor pressure
- Increase membrane coefficient or area

## Future Enhancements

- [ ] Implement RK4 integration for better accuracy
- [ ] Add economic analysis (cost per m³)
- [ ] Include fouling dynamics
- [ ] Multi-year simulations for seasonal analysis
- [ ] Comparison of different VMD configurations
- [ ] Salinity and desalination efficiency tracking
- [ ] 3D visualizations
- [ ] Optimization algorithms to maximize production/efficiency

## References

- Khayet, M. (2011). Membranes and desalination: Membrane distillation.
- Banat, F., Jwaied, N. (2008). Economic evaluation of desalination by solar-powered vacuum membrane distillation.

## License

This project is provided as-is for educational and research purposes.

## Contact & Support

For questions or improvements, feel free to modify and extend the code!

---

**Last Updated:** April 2026
