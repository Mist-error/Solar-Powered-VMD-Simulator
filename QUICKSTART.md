# Quick Start Guide - VMD Simulator

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd "c:\Users\NANNU\Desktop\VMD Project"
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web GUI framework
- `numpy`, `scipy` - Numerical computing
- `plotly` - Interactive visualizations
- `pandas` - Data handling
- `matplotlib` - Additional plotting

### Step 2: Run the Application
```bash
streamlit run app.py
```

The GUI will open at `http://localhost:8501`

### Step 3: Explore!
- Adjust sliders in the sidebar to change system parameters
- Click **"▶️ Run Simulation"** to execute
- View results in real-time
- Export data to CSV

---

## 📊 Understanding the Results

### Key Metrics Explained

| Metric | Unit | Meaning |
|--------|------|---------|
| **Total Water Produced** | kg | Total fresh water generated in the simulation |
| **Production Rate** | kg/h | Average water production per hour |
| **GOR** | – | Gain Output Ratio: higher is better (typical 2-5) |
| **SEC** | kWh/m³ | Energy needed to produce 1 cubic meter of water |
| **Max Temperature** | °C | Highest temperature reached in the tank |
| **Average Flux** | kg/(m²·s) | Membrane permeability in action |

**Good Performance:**
- GOR > 3 (ideally 4-6)
- SEC < 200 kWh/m³
- Smooth temperature rise during daytime

---

## 🎮 Parameter Tuning Tips

### To Increase Water Production:
1. ✅ **Increase solar intensity** - Use a sunnier location
2. ✅ **Increase collector area** - More solar panels
3. ✅ **Increase membrane area** - More distillation surface
4. ✅ **Improve membrane** - Higher membrane coefficient

### To Improve Efficiency (GOR):
1. ✅ **Increase tank mass** - Better thermal storage
2. ✅ **Reduce heat loss** - Better insulation
3. ✅ **Add more effects** - Multi-effect improves efficiency
4. ✅ **Lower vacuum pressure** - Increases driving force

### To Reduce Energy Consumption (SEC):
1. ✅ **Larger tank** - Smoother temperature
2. ✅ **More solar area** - Harness more free energy
3. ✅ **Better insulation** - Reduce parasitic losses
4. ✅ **Multi-effect** - Heat recovery between stages

---

## 🧪 Example Scenarios

### Scenario 1: Desert Location
```
Solar Intensity: 1000 W/m²
Ambient: 45°C
Heat Loss: 3 W/K (good insulation)
Tank: 200 kg
Result: ~50+ kg/h production
```

### Scenario 2: Temperate Climate
```
Solar Intensity: 700 W/m²
Ambient: 25°C
Heat Loss: 8 W/K
Tank: 100 kg
Result: ~25-30 kg/h production
```

### Scenario 3: Research/Efficiency Focus
```
Number of Effects: 5 (max)
Membrane Area/Effect: 30 m²
Tank Mass: 300 kg
Enable Clouds: OFF (ideal conditions)
Result: High GOR (4-5), low SEC
```

---

## 📈 Interpreting Graphs

### Tank Temperature vs Time
- **Flat line**: System in thermal equilibrium
- **Rising curve**: Heating up (sunny hours)
- **Falling curve**: Cooling at night
- **Target**: Should reach 40-60°C in good conditions

### Solar Irradiance vs Time
- **Cosine-like shape**: Natural day/night cycle (5 AM - 6 PM)
- **Jagged line**: Cloud effects enabled
- **Zero during night**: Realistic behavior

### Flux vs Time
- **Follows irradiance**: More sun = more flux
- **Peaks at midday**: When tank is hottest
- **Zero at night**: No evaporation without heat

### Cumulative Production
- **Steep rise during day**: Active production
- **Flat at night**: Paused production
- **Final value**: Total water at simulation end

---

## 🔧 Advanced Usage

### Export and Analysis
1. Run simulation
2. Download CSV in "Export" tab
3. Analyze in Excel, Python, or your favorite tool

### Compare Designs
1. Run simulation with Design A
2. Note the results
3. Adjust parameters for Design B
4. Compare metrics side-by-side

### Cloud Effects
- Enable **"Enable Cloud Effects"** in sidebar
- Simulates realistic weather variability
- Reduces peak production but shows robustness

---

## ❓ Troubleshooting

**Q: Temperature not increasing?**
- A: Check if it's during daytime hours (6 AM - 6 PM in the model)
- A: Increase solar area or intensity
- A: Reduce heat loss coefficient

**Q: Zero water production?**
- A: Temperature needs to be > ambient
- A: Vacuum pressure must be < vapor pressure at feed temp
- A: Increase membrane coefficient

**Q: Simulation takes too long?**
- A: Increase time step (e.g., 300s instead of 60s)
- A: Reduce simulation hours
- A: Reduce number of data points

**Q: GOR is too low?**
- A: Increase tank mass for better thermal storage
- A: Add more VMD effects (up to 5)
- A: Increase solar area relative to membrane area

---

## 📚 Further Reading

Check the main `README.md` for:
- Full physics equations
- Code architecture details
- Component descriptions
- Future enhancement ideas

---

## 💡 Example Commands

### Quick test run:
```bash
python test_simulation.py
```
This runs a preset 24-hour simulation to verify everything works.

### Full interactive GUI:
```bash
streamlit run app.py
```

---

**Ready to simulate?** Run the app and start exploring! 🎯
