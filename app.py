import streamlit as st
import math

st.set_page_config(page_title="The Simpler Solar Calculator", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]  {
    font-family: 'Roboto', sans-serif;
    background-color: #f7f9fc;
    color: #1a1a1a;
}
.stMetricValue, .stMetricLabel {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Calculator", "Learn About Solar Panels", "Tips & FAQs"])

st.title("The Simpler Solar Power Calculator")
st.write("Enter the information you know and allow the system to calculate for you.")

st.header("Energy Output Estimator")
Wattage = st.number_input("Panel Wattage (W)", value=400)
sun_hours = st.number_input("Sunlight hours/day", value=10)
Efficiency = st.slider("System efficiency (%)", 50, 100, 80)

daily_energy = (Wattage * (Efficiency / 100) * sun_hours) / 1000
monthly_energy = daily_energy * 30

col1, col2 = st.columns(2)
col1.metric("Daily Energy Output", f"{daily_energy:.2f} kWh/day")
col2.metric("Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

st.header("Panels Needed")
daily_need = st.number_input("Daily household energy usage (kWh)", value=daily_energy)
number_panels = math.ceil(daily_need / daily_energy)
st.metric("Estimated Number of Panels", number_panels)

st.header("Roof Fit Estimation")
panel_size = st.number_input("Panel size (sq ft)", value=17.6, min_value=1.0)
roof_size = st.number_input("Roof size (sq ft)", value=200, min_value=1.0)
panel_num_fit = roof_size / panel_size if panel_size > 0 else 0
st.write(f"Estimated panels that fit on roof: {int(panel_num_fit)}")

st.header("Estimated System Cost")
cost_per_watt = st.slider("Cost per watt (USD/W)", 0.5, 1.5, 1.0)
custom_install = st.checkbox("I know my installation %")
if custom_install:
    install_factor = st.slider("Installation & equipment (%)", 0, 100, 25) / 100
else:
    install_factor = 0.25

total_system_watts = number_panels * Wattage
panel_cost = total_system_watts * cost_per_watt
installation_cost = panel_cost * install_factor
total_cost_with_install = panel_cost + installation_cost

col1, col2 = st.columns(2)
col1.metric("System Power", f"{total_system_watts/1000:.2f} kW")
col2.metric("Panel Cost", f"${panel_cost:,.0f}")
col3, col4 = st.columns(2)
col3.metric("Installation Cost", f"${installation_cost:,.0f}")
col4.metric("Total System Cost", f"${total_cost_with_install:,.0f}")

st.header("Panel Tilt")
Latitude = st.number_input("Latitude", value=0)
Season = st.selectbox("Season for max sunlight", ["Whole year", "Summer", "Winter"])
tilt = Latitude if Season=="Whole year" else Latitude -15 if Season=="Summer" else Latitude +15
st.success(f"Recommended tilt angle: {tilt:.1f}°")

st.header("Panel Degradation")
years = st.number_input("Number of years", min_value=0, step=1)
degradation_rate = 0.005
efficiency_after_years = 100 * (1 - degradation_rate * years)
st.metric("Estimated Panel Efficiency (%)", f"{efficiency_after_years:.2f}")

st.header("Battery Storage Estimation")
days_backup = st.slider("Days of backup energy", 1, 5, 2)
battery_type = st.selectbox("Battery type", ["Lithium-ion", "Lead-acid"])
depth_of_discharge = 0.9 if battery_type=="Lithium-ion" else 0.5
system_efficiency = 0.9 if battery_type=="Lithium-ion" else 0.85
cost_per_kWh = 400 if battery_type=="Lithium-ion" else 250

battery_capacity = (daily_energy * days_backup) / (depth_of_discharge * system_efficiency)
battery_cost = battery_capacity * cost_per_kWh

col1, col2 = st.columns(2)
col1.metric("Recommended Battery Capacity", f"{battery_capacity:.2f} kWh")
col2.metric("Estimated Battery Cost", f"${battery_cost:,.0f} USD")

st.info(f"This estimate accounts for efficiency losses and safe discharge limits for {battery_type.lower()} batteries.")






