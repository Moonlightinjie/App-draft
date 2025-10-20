import streamlit as st
import matplotlib.pyplot as plt
import math 

st.set_page_config(page_title="The Simpler Solar Calculator", layout="centered")

st.markdown("""
<style>
/* Global font and colors */
body, .stApp {background-color: #f5f5f5; color: #111; font-family: 'Inter', sans-serif;}
h1, h2, h3, h4 {font-family: 'Roboto', sans-serif; color: #111;}
.stMetricLabel, .stMetricValue {font-family: 'Courier New', monospace; font-weight: bold; color: #0077b6;}
.stContainer {background-color: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Calculator", "Learn About Solar Panels", "Tips & FAQs"])

with tab1:
    st.title("The Simpler Solar Power Calculator")
    st.write("Enter the information you know and allow the system to calculate for you")

    with st.container():
        st.header("Energy Output Estimator")
        st.write("Enter your panel specifications and expected sunlight hours to estimate energy output.")
        Wattage = st.number_input("Panel Wattage (maximum power your panel can generate)", value=400)
        sun_hours = st.number_input("Expected sunlight hours (based on area/month)", value=10)
        Efficiency = st.slider("System efficiency (%)", 50, 100, 80)
        st.write("Lower values mean cheaper panels but less energy output.")
        daily_energy = (Wattage * (Efficiency / 100) * sun_hours) / 1000
        monthly_energy = daily_energy * 30
        st.metric("Estimated Daily Energy Output", f"{daily_energy:.2f} kWh/day")
        st.metric("Estimated Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

    with st.container():
        st.header("Number of Panels Needed")
        st.write("Enter your daily household energy usage to estimate how many panels you'll need.")
        daily_need = st.number_input("Daily household energy usage (kWh)")
        number_panels = math.ceil(daily_need / daily_energy)
        st.metric("Estimated number of panels needed", number_panels)

    with st.container():
        st.header("Estimated Number of Panels That Can Fit")
        st.write("Enter panel and roof sizes to estimate how many panels fit.")
        st.write("Average panel size ~17.6 sq ft. If calculating manually, divide inches by 12 and multiply.")
        panel_size = st.number_input("Approximate panel size (sq ft)", min_value=1.0)
        roof_size = st.number_input("Estimated roof size (sq ft)", min_value=1.0)
        if panel_size > 0:
            panel_num = roof_size / panel_size
            st.write("Estimated number of panels that can fit:", int(panel_num))

    with st.container():
        st.header("Estimated Solar Panel Cost")
        st.write("Estimate total system cost including panels and installation.")
        if panel_size > 0 and roof_size > 0:
            cost_per_watt = st.slider("Estimated cost per watt (USD/W)", 0.5, 1.5, 1.0, help="Most panels cost $0.80–$1.20 per watt.")
            custom_install = st.checkbox("I know my installation percentage")
            if custom_install:
                install_factor = st.slider("Installation & Equipment Cost (%)", 0, 100, 25, help="Includes inverter, wiring, mounting, and labor.") / 100
            else:
                install_factor = 0.25
                st.write("Default installation cost: 25% of panel cost.")
            total_system_watts = number_panels * Wattage
            panel_cost = total_system_watts * cost_per_watt
            installation_cost = panel_cost * install_factor
            total_cost_with_install = panel_cost + installation_cost
            st.metric("Estimated System Power", f"{total_system_watts/1000:.2f} kW")
            st.metric("Estimated Panel Cost", f"${panel_cost:,.0f}")
            st.metric("Estimated Installation & Equipment Cost", f"${installation_cost:,.0f}")
            st.metric("Estimated Total System Cost", f"${total_cost_with_install:,.0f}")
            st.info("This estimate uses average solar prices. Actual costs depend on your region and installer.")
        else:
            st.warning("Enter valid panel and roof sizes above to calculate cost.")

    with st.container():
        st.header("Angle Tilt")
        Latitude = st.number_input("Input the latitude of your area", value=90)
        Season = st.selectbox("Select season for max sunlight", ["The whole year", "Summer", "Winter"])
        if Season == "The whole year":
            tilt = Latitude
            st.write("Tilt is equal to your latitude.")
        elif Season == "Summer":
            tilt = Latitude - 15
            st.write("Tilt equals latitude minus 15 degrees.")
        else:
            tilt = Latitude + 15
            st.write("Tilt equals latitude plus 15 degrees.")
        st.success(f"Recommended tilt angle: {tilt:.1f}°")

    with st.container():
        st.header("Panel Degradation")
        years = st.number_input("Enter number of years to estimate panel efficiency", min_value=0, step=1)
        degradation_rate = 0.005
        efficiency = 100 * (1 - degradation_rate * years)
        st.metric("Estimated panel efficiency (%)", f"{efficiency:.2f}")

    with st.container():
        st.header("Battery Storage Estimation")
        st.write("Estimate the battery capacity and cost for backup storage.")
        days_backup = st.slider("Days of backup energy needed", 1, 5, 2)
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




