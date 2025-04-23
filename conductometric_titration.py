import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Conductometric Titration Simulator", layout="wide")

# Title
st.title("🔬 Conductometric Titration Simulator")

with st.expander("🎯 Aim"):
    st.markdown("""
    To find out the strength of hydrochloric acid and acetic acid in a given mixture 
    by titrating it against sodium hydroxide solution, conductometrically.
    """)

with st.expander("⚙️ Apparatus"):
    st.markdown("""
    Conductivity meter, burette, pipette, beakers, volumetric flask, etc.
    """)

with st.expander("📚 Principle"):
    st.markdown("""
    Conductometric titration is based on measuring the change in conductivity of a solution
    as an acid is neutralized by a base. The change depends on the mobility of ions like H⁺, OH⁻, and Na⁺.
    """)

with st.expander("🧪 Procedure Summary"):
    st.markdown("""
    1. Standardize NaOH using oxalic acid.
    2. Titrate 10 ml of diluted acid mixture with 0.1N NaOH.
    3. Measure conductance every 0.2 ml of NaOH addition until 8 ml.
    4. Plot conductance vs. volume added and calculate the strength.
    """)

# Input Section
st.header("📥 Input Experimental Data")

col1, col2 = st.columns(2)
with col1:
    V1 = st.number_input("Volume of oxalic acid (ml)", value=25.0)
    x = st.number_input("Concentration of oxalic acid (N)", value=0.1)
    Vx = st.number_input("Volume of NaOH used for titration (ml)", value=12.5)

with col2:
    V_HCl = st.number_input("Volume of NaOH for HCl from graph (ml)", value=4.0)
    V_total = st.number_input("Volume for HCl + CH₃COOH from graph (ml)", value=8.0)
    sample_volume = 10.0

# Calculations
Ni = round((25 * x) / Vx, 4)
N_HCl = round((V_HCl * Ni) / sample_volume, 4)
N_CH3COOH = round(((V_total - V_HCl) * Ni) / sample_volume, 4)

mass_HCl = round((N_HCl * 36.5 * 100) / 1000, 4)
mass_CH3COOH = round((N_CH3COOH * 60 * 100) / 1000, 4)

# Display Calculations
st.header("🧮 Results")

st.write(f"**Concentration of NaOH (N):** {Ni}")
st.write(f"**Concentration of HCl (N):** {N_HCl}")
st.write(f"**Concentration of CH₃COOH (N):** {N_CH3COOH}")
st.success(f"**Mass of HCl in mixture:** {mass_HCl} g")
st.success(f"**Mass of CH₃COOH in mixture:** {mass_CH3COOH} g")

# Graphical Simulation
st.header("📈 Simulated Graph")

acid_type = st.selectbox("Choose acid system to simulate:", ["HCl only", "CH₃COOH only", "Mixture (HCl + CH₃COOH)"])
volume_added = st.slider("Max Volume of NaOH added (mL)", 5.0, 30.0, 15.0, 0.5)
volumes = np.arange(0, volume_added, 0.5)
conductance = []

if acid_type == "HCl only":
    for v in volumes:
        c = 10 - v if v < 7 else 2 + (v - 7) * 0.8
        conductance.append(c)
elif acid_type == "CH₃COOH only":
    for v in volumes:
        c = 4 + v * 0.5 if v < 8 else 8 + (v - 8) * 1.2
        conductance.append(c)
else:
    for v in volumes:
        if v < 5:
            c = 10 - v * 1.2
        elif v < 12:
            c = 5 + (v - 5) * 0.5
        else:
            c = 8 + (v - 12) * 1.5
        conductance.append(c)

fig, ax = plt.subplots()
ax.plot(volumes, conductance, marker='o', color='blue')
ax.set_title("Conductance vs Volume of NaOH Added")
ax.set_xlabel("Volume of NaOH (mL)")
ax.set_ylabel("Conductance (mS)")
ax.grid(True)
st.pyplot(fig)

# Theory Box
with st.expander("📘 Show Theory Behind Graph"):
    st.markdown("""
    - **HCl**: Sharp drop in conductance due to replacement of fast-moving H⁺ by slower Na⁺.
    - **CH₃COOH**: Gradual increase since CH₃COONa adds ions slowly.
    - **After endpoint**: Conductance rises due to excess OH⁻ ions.
    """)

# Report download
report = f"""
Conductometric Titration Report

Concentration of NaOH: {Ni} N
Volume for HCl (from graph): {V_HCl} mL
Volume for HCl + CH₃COOH: {V_total} mL

Concentration of HCl: {N_HCl} N
Concentration of CH₃COOH: {N_CH3COOH} N

Amount of HCl in 100 ml: {mass_HCl} g
Amount of CH₃COOH in 100 ml: {mass_CH3COOH} g
"""

st.download_button("📄 Download Report", report, "titration_report.txt")

st.success("🧪 Simulation and calculations complete! Feel free to modify inputs and recheck.")
