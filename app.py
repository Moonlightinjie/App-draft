import streamlit as st
import math

st.set_page_config(page_title="Simpler Solar Calculator", layout="centered")

st.markdown("""
<style>
body, .stApp {background-color: #f0f2f6; color: #111; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
h1, h2, h3, h4 {font-family: 'Roboto', sans-serif; color: #111;}
.stMetricLabel, .stMetricValue {font-family: 'Courier New', monospace; font-weight: bold; color: #0077b6;}
.stContainer {background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Calculator", "Learn About Solar Panels", "Tips & FAQs"])

with tab1:
 st.title("The Simpler Solar Power Calculator")
 st.write("Enter the information you know and the system will calculate for you.")

 with st.container():
  st.header("Energy Output Estimator")
  st.write("Enter your panel specifications and expected sunlight hours to estimate energy output.")
  Wattage = st.number_input("Panel Wattage (the maximum power the panel can generate)", value=400)
  sun_hours = st.number_input("Expected sunlight hours (based on area/month)", value=10)
  Efficiency = st.slider("System efficiency (%)", 50, 100, 80)
  st.write("Lower efficiency values mean cheaper panels but less energy output.")
  daily_energy = (Wattage * (Efficiency/100) * sun_hours)/1000
  monthly_energy = daily_energy*30
  st.metric("Estimated Daily Energy Output", f"{daily_energy:.2f} kWh/day")
  st.metric("Estimated Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

 with st.container():
  st.header("Number of Panels Needed")
  st.write("Enter your daily household energy usage to estimate how many panels you'll need.")
  daily_need = st.number_input("Daily household energy usage (kWh)")
  if daily_energy>0:
   number_panels = math.ceil(daily_need/daily_energy)
   st.metric("Estimated number of panels needed", number_panels)

 with st.container():
  st.header("Panels Fit on Your Roof")
  st.write("Estimate how many panels can fit on your roof based on panel and roof size.")
  panel_size = st.number_input("Approximate panel size (sq ft)", min_value=1.0)
  roof_size = st.number_input("Estimated roof size (sq ft)", min_value=1.0)
  if panel_size>0:
   panel_num = roof_size/panel_size
   st.write("Estimated number of panels that can fit:", int(panel_num))

 with st.container():
  st.header("Estimated Solar Panel Cost")
  st.write("Estimate panel and installation costs for your system.")
  if panel_size>0 and roof_size>0:
   cost_per_watt = st.slider("Estimated cost per watt (USD/W)", 0.5,1.5,1.0)
   custom_install = st.checkbox("I know my installation percentage")
   if custom_install:
    install_factor = st.slider("Installation & Equipment Cost (%)",0,100,25)/100
   else:
    install_factor = 0.25
    st.write("Default installation cost: 25% of panel cost")
   total_system_watts = number_panels*Wattage
   panel_cost = total_system_watts*cost_per_watt
   installation_cost = panel_cost*install_factor
   total_cost = panel_cost+installation_cost
   st.metric("Estimated System Power", f"{total_system_watts/1000:.2f} kW")
   st.metric("Estimated Panel Cost", f"${panel_cost:,.0f}")
   st.metric("Estimated Installation Cost", f"${installation_cost:,.0f}")
   st.metric("Estimated Total System Cost", f"${total_cost:,.0f}")
  else:
   st.warning("Enter valid panel and roof sizes to calculate cost.")




