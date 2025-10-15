import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(page_title=" The Simpler Solar Calculator", layout="centered")

tab1, tab2, tab3 = st.tabs (["Calculator", "Learn About Solar Panels", "Tips & FAQs"])



with tab1:
    st. title ("The Simpler Solar Power Calculator")
    st. write ("Enter the information you know and allow the system to calculate for you")

Wattage = st.number_input ("Panel Wattage (W)", value = 400)
Latitude = st.number_input ("Input the latitude of your geographical area (google it and then enter it)", value = 90)
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
    
