import streamlit as st
import matplotlib.pyplot as plt
import math 
st.set_page_config(page_title=" The Simpler Solar Calculator", layout="centered")

tab1, tab2, tab3 = st.tabs (["Calculator", "Learn About Solar Panels", "Tips & FAQs"])

with tab1:
    st. title ("The Simpler Solar Power Calculator")
    st. write ("Enter the information you know and allow the system to calculate for you")

st. header ("Estimated Output")

st.header("Energy Output Estimator")

Wattage = st.number_input( "Panel Wattage (the maximum power the panel can generate, think about what you're using the panel for to estimate this)",value=400)

sun_hours = st.number_input("How many sunlight hours do you expect (Base this on your area, month etc.)?", value=10)

Efficiency = st.slider("Choose system efficiency you want in your panels (%)", 50, 100, 80)
st.write("Lower values mean your panels will be cheaper but less efficient")

daily_energy = (Wattage * (Efficiency / 100) * sun_hours) / 1000  # kWh/day
monthly_energy = daily_energy * 30

st.metric("Estimated Daily Energy Output", f"{daily_energy:.2f} kWh/day")
st.metric("Estimated Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

st. header ("Number of panels needed")

daily_need = st. number_input ("Enter your daily household energy usage (kWh) you can use the figure calculated above")
number_panels = math.ceil (daily_need / daily_energy)
st. metric ("Estimated number of panels needed", number_panels)

st. header ("Estimated solar panel cost")
st. write ("You can estimate how much your solar panels and installation will cost based on the size of your system.")

if panel_size > 0 and roof_size > 0:
    
    cost_per_watt = st.slider(
        "Estimated cost per watt (USD/W)",
        0.5, 1.5, 1.0,
        help="Most solar panels cost between $0.80–$1.20 per watt."
    )

    custom_install = st.checkbox("I know my installation percentage")

    if custom_install:
        install_factor = st.slider(
            "Enter installation and equipment cost (%)",
            0, 100, 25,
            help="Includes inverter, wiring, mounting, and labor costs."
        ) / 100
    else:
        install_factor = 0.25  # default 25%
        st.write("Estimated installation cost: **25% of panel cost** (typical average).")

    total_system_watts = panel_num * Wattage
    panel_cost = total_system_watts * cost_per_watt
    installation_cost = panel_cost * install_factor
    total_cost_with_install = panel_cost + installation_cost

    st.metric("Estimated System Power", f"{total_system_watts/1000:.2f} kW")
    st.metric("Estimated Panel Cost", f"${panel_cost:,.0f}")
    st.metric("Estimated Installation & Equipment Cost", f"${installation_cost:,.0f}")
    st.metric("Estimated Total System Cost", f"${total_cost_with_install:,.0f}")

    st.info(
        "This estimate uses average solar prices. Installation includes inverter, wiring, and labor. "
        "Actual prices depend on your region and installer."
    )
else:
    st.warning("Please

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

st.header("Panel degradation")

years = st.number_input("Enter a specific number of years to figure out the efficiency of your panel after this period.", min_value=0, step=1)
degradation_rate = 0.005  # 0.5% per year
efficiency = 100 * (1 - degradation_rate * years)

st.metric("Estimated panel efficiency (%)", f"{efficiency:.2f}")

st.header("Estimated number of panels that can fit")

st.write("The average size of a solar panel is 65 inches long by 39 inches wide, (17.6 square feet.) but this varies. If you have an idea of the panel size you will be using, enter it below.")
st. write ("If you want to calculate the size of a solar panel in square feet, divide each inch by 12 and multiply them by each other.")

panel_size = st.number_input("Enter approximate panel size (sq ft)", min_value=1.0)
roof_size = st.number_input("If you have an estimate of your roof size, enter it (sq ft)", min_value=1.0)

if panel_size > 0:
    panel_num = roof_size / panel_size
    st.write("Estimated number of panels that can fit:", int(panel_num))
    
st. header ("Battery storage estimation")

st. write ("This refers to the amount of energy you need to store in your panel")

days_backup = st. slider ("How many days of backup energy do you need?", 1, 5, 2)
battery_type = st.selectbox("What type of battery will you use?", ["Lithium-ion", "Lead-acid"])

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




