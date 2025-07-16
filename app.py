import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import interpolate_distance, get_wind_adjustment

# Load chart data
chart_df = pd.read_csv("charts/landing_curve.csv")

st.set_page_config(page_title="RFDS B200 Landing Distance Estimator", layout="wide")
st.title("🛬 RFDS B200 Landing Distance Estimator")

# Sidebar inputs
st.sidebar.header("Flight Parameters")
weight = st.sidebar.slider("Landing Weight (lbs)", 10000, 12500, 11000, step=100)
altitude = st.sidebar.slider("Pressure Altitude (ft)", 0, 8000, 4000, step=500)
temperature = st.sidebar.slider("Outside Air Temperature (°C)", -10, 40, 20, step=1)
wind = st.sidebar.slider("Wind Component (knots)", -20, 20, 0, step=5)

# Interpolated result
raw_distance = interpolate_distance(chart_df, weight, altitude, temperature)
wind_adjust = get_wind_adjustment(wind, weight)
final_distance = raw_distance - wind_adjust

# Output metrics
st.metric("Distance over 50 ft Obstacle (Unadjusted)", f"{raw_distance:.0f} ft")
st.metric("Wind Correction", f"-{wind_adjust:.0f} ft" if wind > 0 else f"+{abs(wind_adjust):.0f} ft")
st.metric("Estimated Final Landing Distance", f"{final_distance:.0f} ft")

# Plot
fig, ax = plt.subplots()
ax.scatter(weight, final_distance, color='red', label='Your Scenario')
ax.plot(chart_df["Weight"], chart_df["Distance"], color='blue', label='OEM Curve')
ax.set_xlabel("Landing Weight (lbs)")
ax.set_ylabel("Distance over 50 ft Obstacle (ft)")
ax.legend()
st.pyplot(fig)

# Footer
st.caption("Data derived from April 2007 OEM charts. Wind adjustment is chart-faithful.")
