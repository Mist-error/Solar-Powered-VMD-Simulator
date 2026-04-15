"""
Streamlit GUI for Solar-Powered Multi-Effect VMD Simulator
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from io import StringIO

from simulation import VMDSimulation


def create_layout():
    """Set page configuration and layout."""
    st.set_page_config(
        page_title="Solar-Powered VMD Simulator",
        page_icon="💧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("☀️ Solar-Powered Multi-Effect Vacuum Membrane Distillation (VMD) Simulator")
    st.markdown("---")


def create_sidebar_inputs() -> dict:
    """Create sidebar input controls and return all parameters."""
    
    st.sidebar.header("🔧 System Parameters")
    
    # Tank parameters
    st.sidebar.subheader("Tank Configuration")
    tank_mass = st.sidebar.slider(
        "Tank Mass (kg)",
        min_value=10.0,
        max_value=500.0,
        value=100.0,
        step=10.0,
        help="Mass of the solar thermal tank"
    )
    
    initial_temp = st.sidebar.slider(
        "Initial Temperature (°C)",
        min_value=15.0,
        max_value=80.0,
        value=25.0,
        step=1.0
    )
    
    ambient_temp = st.sidebar.slider(
        "Ambient Temperature (°C)",
        min_value=10.0,
        max_value=40.0,
        value=25.0,
        step=1.0
    )
    
    heat_loss_coeff = st.sidebar.slider(
        "Heat Loss Coefficient (W/K)",
        min_value=1.0,
        max_value=50.0,
        value=5.0,
        step=1.0,
        help="Heat loss rate per degree Celsius difference"
    )
    
    # Solar parameters
    st.sidebar.subheader("Solar Collector")
    solar_intensity = st.sidebar.slider(
        "Solar Intensity (W/m²)",
        min_value=100.0,
        max_value=1200.0,
        value=800.0,
        step=50.0,
        help="Peak solar irradiance"
    )
    
    solar_area = st.sidebar.slider(
        "Solar Collector Area (m²)",
        min_value=5.0,
        max_value=100.0,
        value=20.0,
        step=5.0
    )
    
    enable_clouds = st.sidebar.checkbox(
        "Enable Cloud Effects",
        value=False,
        help="Simulate random cloud fluctuations"
    )
    
    # VMD parameters
    st.sidebar.subheader("VMD System Configuration")
    num_effects = st.sidebar.slider(
        "Number of Effects",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        help="Number of VMD stages in series"
    )
    
    membrane_area = st.sidebar.slider(
        "Membrane Area per Effect (m²)",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=1.0
    )
    
    membrane_coeff = st.sidebar.number_input(
        "Membrane Coefficient (kg/(m²·s·Pa)) [×10⁻⁷]",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="Higher values = more permeable membrane"
    )
    membrane_coeff *= 1e-7  # Convert display value to actual
    
    vacuum_pressure = st.sidebar.slider(
        "Vacuum Pressure (Pa)",
        min_value=10.0,
        max_value=1000.0,
        value=100.0,
        step=50.0,
        help="Absolute pressure on permeate side"
    )
    
    temp_drop_per_stage = st.sidebar.slider(
        "Temperature Drop per Stage (°C)",
        min_value=1.0,
        max_value=15.0,
        value=5.0,
        step=0.5,
        help="Temperature decrease between effects"
    )
    
    # Simulation parameters
    st.sidebar.subheader("Simulation Settings")
    sim_hours = st.sidebar.slider(
        "Simulation Duration (hours)",
        min_value=1.0,
        max_value=72.0,
        value=24.0,
        step=1.0
    )
    
    time_step = st.sidebar.selectbox(
        "Time Step",
        options=[30.0, 60.0, 120.0, 300.0],
        index=1,
        format_func=lambda x: f"{int(x)} seconds"
    )
    
    return {
        'tank_mass': tank_mass,
        'initial_temperature': initial_temp,
        'ambient_temperature': ambient_temp,
        'heat_loss_coefficient': heat_loss_coeff,
        'solar_intensity': solar_intensity,
        'solar_area': solar_area,
        'enable_clouds': enable_clouds,
        'num_effects': num_effects,
        'membrane_area_per_effect': membrane_area,
        'membrane_coefficient': membrane_coeff,
        'vacuum_pressure': vacuum_pressure,
        'temperature_drop_per_stage': temp_drop_per_stage,
        'simulation_hours': sim_hours,
        'time_step_seconds': time_step
    }


def run_simulation_with_params(params: dict):
    """Run simulation with given parameters."""
    
    sim = VMDSimulation(
        tank_mass=params['tank_mass'],
        initial_temperature=params['initial_temperature'],
        ambient_temperature=params['ambient_temperature'],
        heat_loss_coefficient=params['heat_loss_coefficient'],
        solar_intensity=params['solar_intensity'],
        solar_area=params['solar_area'],
        enable_clouds=params['enable_clouds'],
        num_effects=params['num_effects'],
        membrane_area_per_effect=params['membrane_area_per_effect'],
        membrane_coefficient=params['membrane_coefficient'],
        vacuum_pressure=params['vacuum_pressure'],
        temperature_drop_per_stage=params['temperature_drop_per_stage']
    )
    
    results = sim.run_simulation(
        simulation_hours=params['simulation_hours'],
        time_step_seconds=params['time_step_seconds']
    )
    
    return results


def plot_temperature_vs_time(time_hours, tank_temps, ambient_temp):
    """Create temperature vs time plot."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_hours,
        y=tank_temps,
        mode='lines',
        name='Tank Temperature',
        line=dict(color='#FF6B6B', width=2)
    ))
    
    # Ambient temperature line
    fig.add_hline(
        y=ambient_temp,
        line_dash="dash",
        line_color="gray",
        annotation_text="Ambient Temperature",
        annotation_position="right"
    )
    
    fig.update_layout(
        title="Tank Temperature vs Time",
        xaxis_title="Time (hours)",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_flux_vs_time(time_hours, flux):
    """Create flux vs time plot."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_hours,
        y=flux,
        mode='lines',
        name='Membrane Flux',
        line=dict(color='#4ECDC4', width=2),
        fill='tozeroy',
        fillcolor='rgba(78, 205, 196, 0.2)'
    ))
    
    fig.update_layout(
        title="Membrane Flux vs Time",
        xaxis_title="Time (hours)",
        yaxis_title="Flux (kg/(m²·s))",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_production_vs_time(time_hours, cumulative_prod, distillate_rate):
    """Create production plots."""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Cumulative Production", "Distillate Rate")
    )
    
    # Cumulative production
    fig.add_trace(
        go.Scatter(
            x=time_hours,
            y=cumulative_prod,
            mode='lines',
            name='Cumulative Production',
            line=dict(color='#95E1D3', width=2),
            fill='tozeroy'
        ),
        row=1, col=1
    )
    
    # Distillate rate
    fig.add_trace(
        go.Scatter(
            x=time_hours,
            y=distillate_rate * 3600,  # Convert to kg/h
            mode='lines',
            name='Production Rate',
            line=dict(color='#F38181', width=2)
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Time (hours)", row=1, col=1)
    fig.update_xaxes(title_text="Time (hours)", row=1, col=2)
    fig.update_yaxes(title_text="Cumulative (kg)", row=1, col=1)
    fig.update_yaxes(title_text="Rate (kg/h)", row=1, col=2)
    
    fig.update_layout(
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def plot_solar_irradiance(time_hours, solar_irradiance):
    """Create solar irradiance plot."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_hours,
        y=solar_irradiance,
        mode='lines',
        name='Solar Irradiance',
        line=dict(color='#FFD93D', width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 217, 61, 0.3)'
    ))
    
    fig.update_layout(
        title="Solar Irradiance vs Time",
        xaxis_title="Time (hours)",
        yaxis_title="Irradiance (W/m²)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def display_metrics(metrics: dict):
    """Display key performance metrics."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Water Produced",
            f"{metrics['total_water_produced_kg']:.1f} kg",
            help="Total distillate production"
        )
    
    with col2:
        st.metric(
            "Production Rate",
            f"{metrics['total_water_produced_per_hour']:.2f} kg/h",
            help="Average production rate"
        )
    
    with col3:
        st.metric(
            "GOR (Gain Output Ratio)",
            f"{metrics['gor']:.2f}",
            help="Energy efficiency metric"
        )
    
    with col4:
        st.metric(
            "Specific Energy Consumption",
            f"{metrics['specific_energy_consumption_kWh_per_m3']:.1f} kWh/m³",
            help="Energy per unit volume of water"
        )
    
    # Additional metrics in second row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "Max Tank Temperature",
            f"{metrics['max_temperature']:.1f} °C"
        )
    
    with col6:
        st.metric(
            "Final Tank Temperature",
            f"{metrics['final_temperature']:.1f} °C"
        )
    
    with col7:
        st.metric(
            "Total Energy Input",
            f"{metrics['total_energy_input_kWh']:.1f} kWh"
        )
    
    with col8:
        st.metric(
            "Average Flux",
            f"{metrics['average_flux']:.2e} kg/(m²·s)"
        )


def export_results_csv(results: dict, params: dict):
    """Generate CSV export of simulation results."""
    
    # Main Results
    df = pd.DataFrame({
        'Time (hours)': results['time_hours'],
        'Tank Temperature (°C)': results['tank_temperature'],
        'Solar Irradiance (W/m²)': results['solar_irradiance'],
        'Membrane Flux (kg/(m²·s))': results['flux'],
        'Distillate Rate (kg/s)': results['distillate_rate'],
        'Cumulative Production (kg)': results['cumulative_production']
    })
    
    csv_buffer = StringIO()
    
    # Write parameters
    csv_buffer.write("# Simulation Parameters\n")
    for key, value in params.items():
        csv_buffer.write(f"# {key}: {value}\n")
    
    csv_buffer.write("\n# Simulation Results\n")
    csv_buffer.write(df.to_csv(index=False))
    
    # Write metrics
    csv_buffer.write("\n# Performance Metrics\n")
    metrics = results['metrics']
    for key, value in metrics.items():
        csv_buffer.write(f"# {key}: {value}\n")
    
    return csv_buffer.getvalue()


def main():
    """Main Streamlit application."""
    create_layout()
    
    # Sidebar parameters
    params = create_sidebar_inputs()
    
    # Run button and simulation
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        run_button = st.button("▶️ Run Simulation", key="run_sim")
    
    with col2:
        st.write("")  # Spacer
    
    if run_button or 'results' not in st.session_state:
        if run_button:
            with st.spinner("Running simulation..."):
                st.session_state.results = run_simulation_with_params(params)
                st.session_state.params = params
    
    # Display results if available
    if 'results' in st.session_state:
        results = st.session_state.results
        
        st.header("📊 Results & Analysis")
        
        # Performance Metrics
        st.subheader("Key Performance Metrics")
        display_metrics(results['metrics'])
        
        st.markdown("---")
        
        # Visualizations - Create two tabs
        tab1, tab2, tab3 = st.tabs(["Thermal & Solar", "Production & Flux", "Export"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    plot_temperature_vs_time(
                        results['time_hours'],
                        results['tank_temperature'],
                        params['ambient_temperature']
                    ),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    plot_solar_irradiance(
                        results['time_hours'],
                        results['solar_irradiance']
                    ),
                    use_container_width=True
                )
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    plot_flux_vs_time(
                        results['time_hours'],
                        results['flux']
                    ),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    plot_production_vs_time(
                        results['time_hours'],
                        results['cumulative_production'],
                        results['distillate_rate']
                    ),
                    use_container_width=True
                )
        
        with tab3:
            st.subheader("Export Results")
            
            csv_data = export_results_csv(results, params)
            
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv_data,
                file_name="vmd_simulation_results.csv",
                mime="text/csv"
            )
            
            st.text("CSV file contains:")
            st.text("- All simulation parameters")
            st.text("- Time series data (temperature, irradiance, flux, production)")
            st.text("- Performance metrics summary")
        
        st.markdown("---")
        st.markdown(
            "💡 **Tips:** Adjust parameters in the sidebar and click 'Run Simulation' "
            "to explore different system configurations."
        )


if __name__ == "__main__":
    main()
