import streamlit as st
import math

st.set_page_config(
    page_title="The Simpler Solar Calculator",
    layout="centered"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]  {
    font-family: 'Roboto', sans-serif;
    background-color: #f7f9fc;
    color: #1a1a1a;
}
.stAlert {
    border-radius: 10px;
    padding: 10px;
}
.stMetricValue, .stMetricLabel {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Calculator", "Learn About Solar Panels", "Tips & FAQs"])

with tab1:
    st.title("The Simpler Solar Power Calculator")
    st.write("Enter the information you know and allow the system to calculate for you.")

    with st.expander("Energy Output Estimator", expanded=True):
        col1, col2 = st.columns(2)
        Wattage = col1.number_input("Panel Wattage (W)", value=400)
        sun_hours = col2.number_input("Sunlight hours/day", value=10)
        Efficiency = st.slider("System efficiency (%)", 50, 100, 80)

        daily_energy = (Wattage * (Efficiency / 100) * sun_hours) / 1000
        monthly_energy = daily_energy * 30

        col1.metric("Daily Energy Output", f"{daily_energy:.2f} kWh/day")
        col2.metric("Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

    with st.expander("Panels Needed", expanded=True):
        daily_need = st.number_input("Daily household energy usage (kWh)", value=daily_energy)
        number_panels = math.ceil(daily_need / daily_energy)
        st.metric("Estimated Number of Panels", number_panels)

        st.write("Roof Fit Estimation")
        panel_size = st.number_input("Panel size (sq ft)", value=17.6, min_value=1.0)
        roof_size = st.number_input("Roof size (sq ft)", value=200, min_value=1.0)
        if panel_size > 0 and roof_size > 0:
            panel_num_fit = roof_size / panel_size
            st.write(f"Estimated panels that fit on roof: {int(panel_num_fit)}")

    with st.expander("Estimated System Cost", expanded=True):
        cost_per_watt = st.slider("Cost per watt (USD/W)", 0.5, 1.5, 1.0)
        custom_install = st.checkbox("I know my installation %")
        if custom_install:
            install_factor = st.slider("Installation & equipment (%)", 0, 100, 25) / 100
        else:
            install_factor = 0.25
            st.write("Installation cost: 25% of panel cost (typical).")

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

        st.info("Estimate includes panel cost, installation, inverter, wiring, and labor.")

    with st.expander("Panel Tilt", expanded=False):
        Latitude = st.number_input("Latitude", value=0)
        Season = st.selectbox("Season for maximum sunlight", ["Whole year", "Summer", "Winter"])
        if Season == "Whole year":
            tilt = Latitude
        elif Season == "Summer":
            tilt = Latitude - 15
        else:
            tilt = Latitude + 15
        st.success(f"Recommended tilt angle: {tilt:.1f}°")

    with st.expander("Panel Degradation", expanded=False):
        years = st.number_input("Number of years", min_value=0, step=1)
        degradation_rate = 0.005
        efficiency_after_years = 100 * (1 - degradation_rate * years)
        st.metric("Estimated Panel Efficiency (%)", f"{efficiency_after_years:.2f}")

    with st.expander("Battery Storage Estimation", expanded=False):
        days_backup = st.slider("Days of backup energy", 1, 5, 2)
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
        battery_cost = battery_capacity * cost_per_kWh

        col1, col2 = st.columns(2)
        col1.metric("Recommended Battery Capacity", f"{battery_capacity:.2f} kWh")
        col2.metric("Estimated Battery Cost", f"${battery_cost:,.0f} USD")

        st.info(f"This estimate accounts for efficiency losses and safe discharge limits for {battery_type.lower()} batteries.")





