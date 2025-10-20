import streamlit as st
import math
st.set_page_config(page_title="Simpler Solar Calculator", layout="centered", initial_sidebar_state="expanded")
st.markdown("""<style>body, .stApp {background-color: #0d1b2a; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;} h1, h2, h3, h4 {font-family: 'Roboto', sans-serif; color: #e0e1dd;} .stMetricLabel, .stMetricValue {font-family: 'Courier New', monospace; font-weight: bold; color: #ffd166;} .css-1d391kg {background-color: #1b263b; border-radius: 10px; padding: 10px;} .stButton>button {background-color: #0077b6; color: white;}</style>""", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Calculator", "Learn About Solar Panels", "Tips & FAQs"])
with tab1:
 st.title("The Simpler Solar Power Calculator")
 st.write("Enter the information below and the system will calculate your solar needs.")
 with st.container():
  st.header("Energy Output Estimator")
  Wattage = st.number_input("Panel Wattage (W)", value=400)
  sun_hours = st.number_input("Expected Sunlight Hours", value=10)
  Efficiency = st.slider("System Efficiency (%)", 50, 100, 80)
  daily_energy = (Wattage * (Efficiency / 100) * sun_hours) / 1000
  monthly_energy = daily_energy * 30
  st.metric("Estimated Daily Energy Output", f"{daily_energy:.2f} kWh/day")
  st.metric("Estimated Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")
 with st.container():
  st.header("Number of Panels Needed")
  daily_need = st.number_input("Enter your daily household energy usage (kWh)")
  if daily_energy > 0:
   number_panels = math.ceil(daily_need / daily_energy)
   st.metric("Estimated Number of Panels Needed", number_panels)
 with st.container():
  st.header("Panels Fit on Your Roof")
  panel_size = st.number_input("Approximate panel size (sq ft)", min_value=1.0)
  roof_size = st.number_input("Estimated roof size (sq ft)", min_value=1.0)
  if panel_size > 0:
   panel_num = roof_size / panel_size
   st.write("Estimated number of panels that can fit:", int(panel_num))
 with st.container():
  st.header("Estimated Solar Panel Cost")
  if panel_size > 0 and roof_size > 0:
   cost_per_watt = st.slider("Estimated cost per watt (USD/W)", 0.5, 1.5, 1.0)
   custom_install = st.checkbox("I know my installation percentage")
   if custom_install:
    install_factor = st.slider("Installation & Equipment Cost (%)", 0, 100, 25)/100
   else:
    install_factor = 0.25
    st.write("Default installation cost: 25% of panel cost")
   total_system_watts = number_panels * Wattage
   panel_cost = total_system_watts * cost_per_watt
   installation_cost = panel_cost * install_factor
   total_cost_with_install = panel_cost + installation_cost
   st.metric("System Power", f"{total_system_watts/1000:.2f} kW")
   st.metric("Panel Cost", f"${panel_cost:,.0f}")
   st.metric("Installation Cost", f"${installation_cost:,.0f}")
   st.metric("Total System Cost", f"${total_cost_with_install:,.0f}")
  else:
   st.warning("Enter valid panel and roof sizes above to calculate cost.")
 with st.container():
  st.header("Angle Tilt")
  Latitude = st.number_input("Input the latitude of your area", value=90)
  Season = st.selectbox("Select season for max sunlight", ["Whole year", "Summer", "Winter"])
  if Season == "Whole year":
   tilt = Latitude
   st.write("Tilt equals your latitude")
  elif Season == "Summer":
   tilt = Latitude - 15
   st.write("Tilt equals latitude minus 15 degrees")
  else:
   tilt = Latitude + 15
   st.write("Tilt equals latitude plus 15 degrees")
  st.metric("Recommended tilt angle", f"{tilt:.1f}°")
 with st.container():
  st.header("Panel Degradation")
  years = st.number_input("Enter number of years to estimate efficiency", min_value=0, step=1)
  degradation_rate = 0.005
  efficiency = 100 * (1 - degradation_rate * years)
  st.metric("Estimated panel efficiency (%)", f"{efficiency:.2f}")
 with st.container():
  st.header("Battery Storage Estimation")
  days_backup = st.slider("How many days of backup energy do you need?", 1, 5, 2)
  battery_type = st.selectbox("Battery type", ["Lithium-ion", "Lead-acid"])
  if battery_type == "Lithium-ion":
   depth_of_discharge = 0.9
   system_efficiency = 0.9
   cost_per_kWh = 400
  else:
   depth_of_discharge = 0.5
   system_efficiency = 0.85
   cost_per_kWh = 250
  battery_capacity = (daily_energy * days_backup) / (depth_of_discharge * system_efficiency)
  total_cost = battery_capacity * cost_per_kWh
  st.metric("Recommended Battery Capacity", f"{battery_capacity:.2f} kWh")
  st.metric("Estimated Battery Cost", f"${total_cost:,.0f} USD")
  st.info(f"This estimate accounts for efficiency losses and safe discharge limits for {battery_type.lower()} batteries.")







