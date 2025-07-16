import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import interpolate_distance, get_wind_adjustment

# Load OEM data
chart_df = pd.read_csv("charts/landing_curve.csv")

st.set_page_config(page_title="RFDS B200 Landing Distance Estimator", layout="wide")
st.title("🛬 RFDS B200 Landing Distance Estimator")

# Sidebar Inputs
st.sidebar.header("Flight Parameters")
weight = st.sidebar.slider("Landing Weight (lbs)", 10000, 12500, 11000, step=100)
altitude = st.sidebar.slider("Pressure Altitude (ft)", 0, 8000, 4000, step=500)
temperature = st.sidebar.slider("OAT (°C)", -10, 40, 20, step=10)
wind = st.sidebar.slider("Wind Component (knots)", -30, 30, 0, step=5)

# Run calculations
raw_distance, used_points = interpolate_distance(chart_df, weight, altitude, temperature)
wind_adjust = get_wind_adjustment(wind, weight)
final_distance = raw_distance - wind_adjust

# Output
st.metric("Unadjusted Landing Distance", f"{raw_distance:.0f} ft")
st.metric("Wind Correction", f"{'-' if wind > 0 else '+'}{abs(wind_adjust):.0f} ft")
st.metric("Estimated Final Distance", f"{final_distance:.0f} ft")

# Warning if fallback used
if len(used_points) < 2:
    st.warning("Interpolated from a single OEM datapoint. Results may be less precise.")

# Plot
fig, ax = plt.subplots()
ax.plot(chart_df["Weight"], chart_df["Distance"], label="OEM Curve", color="blue", alpha=0.5)
ax.scatter(weight, final_distance, color="red", label="Your Input")
ax.set_xlabel("Landing Weight (lbs)")
ax.set_ylabel("Distance (ft)")
ax.legend()
st.pyplot(fig)

# Footer
st.caption("Chart data based on April 2007 OEM performance. Wind adjustments are strictly chart-referenced.")
