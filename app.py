import streamlit as st
import math

st.set_page_config(page_title="Simpler Solar Calculator", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
body, .stApp {background-color: #f5f5f5; color: #111; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
h1, h2, h3, h4 {font-family: 'Roboto', sans-serif; color: #111;}
.stMetricLabel, .stMetricValue {font-family: 'Courier New', monospace; font-weight: bold; color: #0077b6;}
.stContainer {background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Calculator", "Learn About Solar Panels", "Tips & FAQs"])

with tab1:
 st.title("Simpler Solar Power Calculator")
 st.write("Enter your information below and see your solar estimates.")

 with st.container():
  st.header("Energy Output Estimator")
  col1, col2, col3 = st.columns(3)
  with col1:
   Wattage = st.number_input("Panel Wattage (W)", value=400)
  with col2:
   sun_hours = st.number_input("Expected Sunlight Hours", value=10)
  with col3:
   Efficiency = st.slider("System Efficiency (%)", 50, 100, 80)
  daily_energy = (Wattage * (Efficiency/100) * sun_hours)/1000
  monthly_energy = daily_energy*30
  col1, col2 = st.columns(2)
  col1.metric("Daily Energy Output", f"{daily_energy:.2f} kWh/day")
  col2.metric("Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

 with st.container():
  st.header("Panels Needed")
  col1, col2 = st.columns(2)
  with col1:
   daily_need = st.number_input("Daily household energy usage (kWh)")
  if daily_energy > 0:
   number_panels = math.ceil(daily_need/daily_energy)
   col2.metric("Estimated Panels Needed", number_panels)

 with st.container():
  st.header("Roof Fit & Panel Size")
  col1, col2 = st.columns(2)
  with col1:
   panel_size = st.number_input("Approx. Panel Size (sq ft)", min_value=1.0)
  with col2:
   roof_size = st.number_input("Roof Size (sq ft)", min_value=1.0)
  if panel_size>0:
   panel_num = roof_size/panel_size
   st.write("Panels that can fit:", int(panel_num))

 with st.container():
  st.header("Cost Estimation")
  if panel_size>0 and roof_size>0:
   col1, col2 = st.columns(2)
   with col1:
    cost_per_watt = st.slider("Cost per Watt (USD/W)", 0.5,1.5,1.0)
    custom_install = st.checkbox("Know installation %")
    if custom_install:
     install_factor = st.slider("Installation & Equipment (%)",0,100,25)/100
    else:
     install_factor = 0.25
     st.write("Default installation cost: 25% of panel cost")
   total_system_watts = number_panels*Wattage
   panel_cost = total_system_watts*cost_per_watt
   installation_cost = panel_cost*install_factor
   total_cost = panel_cost+installation_cost
   col2.metric("System Power", f"{total_system_watts/1000:.2f} kW")
   col2.metric("Panel Cost", f"${panel_cost:,.0f}")
   col2.metric("Installation Cost", f"${installation_cost:,.0f}")
   col2.metric("Total System Cost", f"${total_cost:,.0f}")
  else:
   st.warning("Enter valid panel and roof sizes to calculate cost.")








