import streamlit as st
import matplotlib.pyplot as plt
import math 
st.set_page_config(page_title=" The Simpler Solar Calculator", layout="centered")

tab1, tab2, tab3 = st.tabs (["Calculator", "Learn About Solar Panels", "Tips & FAQs"])

with tab1:
    st. title ("The Simpler Solar Power Calculator")
    st. write ("Enter the information you know and allow the system to calculate for you")

st. header ("Estimated Output")

Wattage = st.number_input ("Panel Wattage (the maximum power the panel can generate, think about what you're using the panel for to estimate this)", value = 400)

sun_hours = st. number_input ("How many sunlight hours do you expect (Base this on your area, month etc.)?", value = 10)
Efficiency = st. slider ("Choose system efficiency you want in your panels) (%)", 50, 100, 80) 
st. write ("Lower values mean your panels will be cheaper but less efficient")

daily_energy = (Wattage * (Efficiency / 100)) * sun_hours / 1000
monthly_energy = (daily_energy * 30)

st.metric("Estimated Daily Energy Output", f"{daily_energy:.2f} kWh/day")
st.metric("Estimated Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

st. header ("Number of panels needed")

daily_need = st. number_input ("Enter your daily household energy usage (kWh) you can use the figure calculated above")
number_panels = math.ceil (daily_need / daily_energy)
st. metric ("Estimated number of panels needed", number_panels)

st. header ("Angle tilt")

Latitude = st.number_input ("Input the latitude of your geographical area (google it and then enter it if needed)", value = 90)
Season = st.selectbox ("What times are you trying to get maximum sunlight absorption for?", ["The whole year", "Summer", "Winter"])
if Season == "The whole year":
    tilt = Latitude 
    st. write ("Tilt is simply equal to your latitude")
elif Season == "Summer":
    tilt = Latitude - 15
    st. write ("Tilt is equal to your latitude - 15 degrees")
else:
    tilt = Latitude + 15
    st. write ("Tilt is equal to your latitude - 15 degrees")
st.success(f"Recommended tilt angle: {tilt:.1f}°")

st. header ("Panel degradation") 
Degradation = st. number_input ("Enter a specific year to figure out the efficiency of your panel after this period.")
Degradation_calculation = (Degradation
st. metric = ("Estimated panel efficiency", f

