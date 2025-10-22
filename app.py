import streamlit as st
import matplotlib.pyplot as plt
import math 
import pandas as pd
import numpy as np

st.set_page_config(page_title="The Simpler Solar Calculator", layout="centered")

st.markdown(
    """
    <style>
    /* Global font for headers, text, and metrics */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    h1, h2, h3, h4 {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stMetricLabel, .stMetricValue {
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs (["Calculator", "Tips & Reccomendations"])

with tab1:
    st.title("The Simpler Solar Power Calculator")
    st.write("Enter the information you know and allow the system to calculate for you")

    st.header("Energy Output Estimator")
    Wattage = st.number_input("Panel Wattage (the maximum power the panel can generate, think about what you're using the panel for to estimate this)", value=400)
    sun_hours = st.number_input("How many sunlight hours do you expect (Base this on your area, month etc.)?", value=10)
    Efficiency = st.slider("Choose system efficiency you want in your panels (%)", 50, 100, 80)
    st.write("Lower values mean your panels will be cheaper but less efficient")

    daily_energy = (Wattage * (Efficiency / 100) * sun_hours) / 1000  # kWh/day
    monthly_energy = daily_energy * 30

    st.metric("Estimated Daily Energy Output", f"{daily_energy:.2f} kWh/day")
    st.metric("Estimated Monthly Energy Output", f"{monthly_energy:.2f} kWh/month")

    st.header("Number of panels needed")
    daily_need = st.number_input("Enter your daily household energy usage (kWh) you can use the figure calculated above")
    number_panels = math.ceil(daily_need / daily_energy)
    st.metric("Estimated number of panels needed", number_panels)

    st.header("Estimated number of panels that can fit")
    st.write("The average size of a solar panel is 65 inches long by 39 inches wide, (17.6 square feet.) but this varies. If you have an idea of the panel size you will be using, enter it below.")
    st.write("If you want to calculate the size of a solar panel in square feet, divide each inch by 12 and multiply them by each other.")

    panel_size = st.number_input("Enter approximate panel size (sq ft)", min_value=1.0)
    roof_size = st.number_input("If you have an estimate of your roof size, enter it (sq ft)", min_value=1.0)

    if panel_size > 0:
        panel_num = roof_size / panel_size
        st.write("Estimated number of panels that can fit:", int(panel_num))

    st.header("Estimated solar panel cost")
    st.write("You can estimate how much your solar panels and installation will cost based on the size of your system.")

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

        total_system_watts = number_panels * Wattage
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
        st.warning("Please enter a valid panel and roof size above to calculate cost.")

    st.header("Graph Representation")
    panel_counts = np.arange(1, 51)
    daily_output_per_panel = Wattage * (Efficiency / 100) * sun_hours / 1000  # kWh
    outputs = panel_counts * daily_output_per_panel
    df = pd.DataFrame({"Number of Panels": panel_counts, "Daily Output (kWh)": outputs})

    st.subheader("Daily Output vs Number of Panels")
    st.line_chart(df.set_index("Number of Panels"))
    st.subheader("Compare Different Panel Wattages & Efficiency")
    comparison_type = st.radio("Compare by:", ["Panel Wattage", "Efficiency"])

    if comparison_type == "Panel Wattage":
        wattages = [200, 300, 400, 500]
        comp_data = {
            f"{w}W": panel_counts * (w * (Efficiency / 100) * sun_hours / 1000)
            for w in wattages
        }
    else:
        efficiencies = [60, 70, 80, 90, 100]
        comp_data = {
            f"{e}%": panel_counts * (Wattage * (e / 100) * sun_hours / 1000)
            for e in efficiencies
        }

    comp_df = pd.DataFrame(comp_data, index=panel_counts)
    st.line_chart(comp_df)

    st.header("Angle tilt")
    Latitude = st.number_input("Input the latitude of your geographical area (google it and then enter it if needed)", value=90)
    Season = st.selectbox("What times are you trying to get maximum sunlight absorption for?", ["The whole year", "Summer", "Winter"])
    if Season == "The whole year":
        tilt = Latitude
        st.write("Tilt is simply equal to your latitude")
    elif Season == "Summer":
        tilt = Latitude - 15
        st.write("Tilt is equal to your latitude - 15 degrees")
    else:
        tilt = Latitude + 15
        st.write("Tilt is equal to your latitude - 15 degrees")
    st.success(f"Recommended tilt angle: {tilt:.1f}°")

    st.header("Panel degradation")
    years = st.number_input("Enter a specific number of years to figure out the efficiency of your panel after this period.", min_value=0, step=1)
    degradation_rate = 0.005  # 0.5% per year
    efficiency = 100 * (1 - degradation_rate * years)
    st.metric("Estimated panel efficiency (%)", f"{efficiency:.2f}")

    st.header("Battery storage estimation")
    st.write("This refers to the amount of energy you need to store in your panel")
    days_backup = st.slider("How many days of backup energy do you need?", 1, 5, 2)
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

    st.header("The Total")
    if panel_size > 0 and roof_size > 0:
        final_total_cost = total_cost_with_install + total_cost 
        st.metric("Final Total Cost (Panels + Installation + Battery)", f"${final_total_cost:,.0f} USD")

with tab2: 
    st.title("Tips & Reccomendations")
    st.write("Just some advice to help you out")

    st.header("Energy Usage & Selection of your panels")
    st.write("Know your daily energy needs before buying panels, you can do this by checking your electric bill. Overestimating wastes money and underestimating will leave you short.")
    st.write("Choose panels with higher efficiency if you have limited roof space as they produce more energy per panel. Also compare different wattages, sometimes more smaller panels are better than fewer large panels depending on roof shape.")
    
    st.header("Placement & Installation")
    st.write("- Panels should face south (in Northern Hemisphere) and face north (in southern hemisphere) for maximum sunlight.")
    st.write("- Try avoid shading from trees, chimneys, or other buildings.")
    st.write("- Ensure your panel is placed at the correct tilt angle for optimal performance and sunlight absorption.")

    st.header("Battery Storage")
    st.write("- Use batteries if you want backup for cloudy days or night usage.")
    st.write("- Match battery capacity to backup days and household needs.")
    st.write("- Lithium-ion batteries let you use most of their stored energy, while lead-acid batteries can only use about half safely.")

    st.header("Cost & Financial Tips")
    st.write("- Make sure to plan for installation & equipment costs (they could add 20–30% of panel cost).")
    st.write("- Check for government incentives or tax credits to reduce costs.")
    st.write("- Invest in high-quality panels for long-term savings.")

    st.header("Maintenance")
    st.write("- Clean panels periodically to maintain output, dirty panels can reduce output by 10–25%.")
    st.write("- Monitor panel efficiency over time; average degradation ~0.5%/year.")
    st.write("- Regularly check connections and inverter performance (A device that converts the DC electricity from solar panels into AC electricity that can be used by household appliances.) to ensure consistent energy production.")

    st.header("Safety + Regulations")
    st.write("- Hire certified installers; improper installation can damage your roof or void warranties.")
    st.write("- Follow local electrical codes, ensure proper wiring, grounding, mounting, and inverter connections, obtain any required permits or inspections, and use safety measures like circuit breakers to keep your solar system safe, legal, and reliable.")
    st.write("- Consider trying to get insurance to protect your panels, inverters and batteries from damage due to storms, theft, or accidents, reducing potential repair or replacement costs.")
    






