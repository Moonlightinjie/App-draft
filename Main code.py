import streamlit as st
import matplotlib.pyplot -m as plt

# ---- Page Config ----
st.set_page_config(
    page_title="Solar Energy Simulator 🌞",
    page_icon="☀️",
    layout="wide"
)

# ---- Title & Description ----
st.title("🌞 Solar Energy Simulator")
st.markdown("""
This interactive simulator lets you **estimate daily solar energy output** and **optimize your solar panel setup**.  
Use the sliders to adjust the number of panels, sunlight hours, panel efficiency, and tilt angle.  
Graphs and tips update dynamically to help you understand your results.
""")

# ---- Sidebar Inputs ----
st.sidebar.header("🔧 System Settings")

num_panels = st.sidebar.slider("Number of Solar Panels", 1, 20, 5)
sun_hours = st.sidebar.slider("Sunlight Hours per Day", 1, 12, 6)
panel_efficiency = st.sidebar.slider("Panel Efficiency (%)", 5, 25, 15)
panel_angle = st.sidebar.slider("Panel Tilt Angle (degrees)", 0, 90, 30)

# ---- Calculations ----
angle_factor = max(0, 1 - abs(45 - panel_angle)/45)  # peak efficiency at 45°
energy_output = num_panels * sun_hours * panel_efficiency * 50 * angle_factor  # Wh

# ---- Display Main Results ----
st.subheader("⚡ Estimated Daily Energy Output")
st.markdown(f"<h2 style='color:green'>{energy_output:.0f} Wh</h2>", unsafe_allow_html=True)

# ---- Explanations ----
st.subheader("💡 Tips & Explanations")
if angle_factor < 0.9:
    st.write(f"- Your panel tilt angle ({panel_angle}°) is not optimal. Adjusting closer to 45° increases efficiency.")
else:
    st.write("- Your panel tilt angle is near optimal! Great setup.")

if sun_hours < 4:
    st.write("- Low sunlight hours reduce energy output. Consider panel location or supplemental energy sources.")
else:
    st.write("- Sunlight hours are sufficient for good energy output.")

# ---- Graph: Energy vs Number of Panels ----
st.subheader("📈 Energy Output vs Number of Panels")

panel_range = list(range(1, 21))
energy_range = [p * sun_hours * panel_efficiency * 50 * angle_factor for p in panel_range]

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(panel_range, energy_range, marker='o', color='#FFA500')
ax.set_xlabel("Number of Panels")
ax.set_ylabel("Daily Energy Output (Wh)")
ax.set_title("Energy Output vs Number of Panels")
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# ---- Challenge Mode ----
st.subheader("🎯 Challenge Mode")
target_energy = st.number_input("Set a target energy output (Wh)", min_value=100, max_value=20000, value=1000)
min_panels_needed = max(1, int(target_energy / (sun_hours * panel_efficiency * 50 * angle_factor)))
st.markdown(f"- Minimum number of panels needed to meet this target: **{min_panels_needed} panels**")

# ---- Footer ----
st.markdown("""
---
Developed for **Eurekathon 2025** 🌟  
Interactive learning meets real-world renewable energy!
""")
