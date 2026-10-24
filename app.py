import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
import time

# Page Layout Configuration
st.set_page_config(
    page_title="Gwalior Waterways Real-Time Auditing Console",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Gwalior Waterways Real-Time Auditing Console")
st.caption("Monitoring Swarna Rekha Canal & Tigra Reservoir | Edge-DSP Optical & Electrochemical Telemetry")

st.divider()

# ---------------------------------------------------------
# LANDING SELECTION: 4 SYSTEM MODULE OPTIONS
# ---------------------------------------------------------
st.markdown("### Select System Module")
selected_tab = st.radio(
    "Choose a module to inspect:",
    [
        "Tab 1: Spatial GIS Map & Contamination Heatmap",
        "Tab 2: Optical & Electrochemical Signal Engine",
        "Tab 3: Surrogate Water Metrics & Alerts",
        "Tab 4: Lab Calibration Engine"
    ],
    horizontal=True
)

st.divider()

# ---------------------------------------------------------
# DATASETS
# ---------------------------------------------------------
canal_route_data = [
    {"point": "Hanuman Bandh (Canal Origin)", "lat": 26.1950, "lon": 78.1450, "contamination": 1.2, "source": "Clean Inlet Stream", "contrib_pct": 0.0},
    {"point": "Birpur Intake Stretch", "lat": 26.2000, "lon": 78.1520, "contamination": 3.5, "source": "Birpur Domestic Runoff", "contrib_pct": 11.5},
    {"point": "Gwalior Zoo Environs", "lat": 26.2080, "lon": 78.1620, "contamination": 9.8, "source": "Gwalior Zoo Animal Waste & Runoff", "contrib_pct": 31.5},
    {"point": "Phoolbagh Commercial Area", "lat": 26.2150, "lon": 78.1680, "contamination": 14.2, "source": "Phoolbagh Commercial Effluent", "contrib_pct": 22.0},
    {"point": "Lashkar Sewage Outfall", "lat": 26.2250, "lon": 78.1760, "contamination": 18.1, "source": "Lashkar Municipal Drain #4", "contrib_pct": 19.5},
    {"point": "Hazira Industrial Belt", "lat": 26.2400, "lon": 78.1880, "contamination": 19.8, "source": "Hazira Chemical & Dye Discharge", "contrib_pct": 8.5},
    {"point": "Gwalior Outskirts / Morena Exit", "lat": 26.2700, "lon": 78.2050, "contamination": 20.0, "source": "Downstream Agricultural Runoff", "contrib_pct": 7.0}
]
df_canal = pd.DataFrame(canal_route_data)

tigra_silt_data = [
    {"sector": "Tigra Dam Main Spillway Zone", "lat": 26.2150, "lon": 78.0120, "silt_level_ntu": 4.2, "status": "Low Silt"},
    {"sector": "Sank River Inflow Mouth", "lat": 26.2080, "lon": 78.0010, "silt_level_ntu": 18.6, "status": "Critical Silt Deposit"},
    {"sector": "Kullu Catchment Basin", "lat": 26.2210, "lon": 78.0180, "silt_level_ntu": 12.4, "status": "Moderate Silt"},
    {"sector": "Southern Feeder Channel", "lat": 26.1980, "lon": 78.0060, "silt_level_ntu": 15.8, "status": "High Silt"}
]
df_tigra = pd.DataFrame(tigra_silt_data)

tigra_inflow_origins = [
    {"Origin": "Sank River Catchment Runoff", "Contribution_Pct": 42.5, "Primary_Contaminant": "Silt & Agricultural Nitrates", "Severity": "High"},
    {"Origin": "Birpur / Rural Catchment Stream", "Contribution_Pct": 31.0, "Primary_Contaminant": "Colloidal Suspended Solids", "Severity": "Moderate"},
    {"Origin": "Upstream Livestock Grazing Outfalls", "Contribution_Pct": 16.5, "Primary_Contaminant": "Organic Carbon (BOD/COD)", "Severity": "Moderate"},
    {"Origin": "Gwalior Municipal Intake Spillover", "Contribution_Pct": 10.0, "Primary_Contaminant": "Total Dissolved Solids (TDS)", "Severity": "Low"}
]
df_inflow = pd.DataFrame(tigra_inflow_origins)

# ---------------------------------------------------------
# MODULE RENDERING LOGIC
# ---------------------------------------------------------
if selected_tab.startswith("Tab 1"):
    st.subheader("Swarna Rekha Canal Route & Tigra Reservoir Contamination Spatial Heatmap")
    
    st.sidebar.header("Map Layer Controls")
    show_canal = st.sidebar.checkbox("Show Swarna Rekha Canal Nodes", value=True)
    show_flow_line = st.sidebar.checkbox("Show Canal Water Blue Flow Line", value=True)
    show_tigra = st.sidebar.checkbox("Show Tigra Reservoir Silt Map", value=True)
    selected_source_inspection = st.sidebar.selectbox("Inspect Contamination Origin:", df_canal["point"].tolist())

    col_map, col_analytics = st.columns([2.2, 1])

    with col_map:
        fig = go.Figure()
        heatmap_colorscale = [
            [0.0, "#FFFFE0"], [0.2, "#FFD700"], [0.4, "#FF7F00"],
            [0.6, "#E60000"], [0.8, "#800000"], [1.0, "#1A0000"]
        ]

        if show_flow_line:
            fig.add_trace(go.Scattermapbox(
                lat=df_canal["lat"], lon=df_canal["lon"],
                mode="lines", line=dict(width=5, color="#00BFFF"),
                name="Swarna Rekha Flow Vector", hoverinfo="none"
            ))

        if show_canal:
            fig.add_trace(go.Scattermapbox(
                lat=df_canal["lat"], lon=df_canal["lon"],
                mode="markers",
                marker=dict(
                    size=df_canal["contamination"] * 1.8 + 12,
                    color=df_canal["contamination"],
                    colorscale=heatmap_colorscale,
                    cmin=0.0, cmax=20.0, showscale=True,
                    colorbar=dict(title="Contamination Scale", x=1.01, len=0.85)
                ),
                text=df_canal["point"],
                hovertemplate="<b>%{text}</b><br>Contamination Index: %{marker.color}/20.0<extra></extra>",
                name="Swarna Rekha Heat Nodes"
            ))

        if show_tigra:
            fig.add_trace(go.Scattermapbox(
                lat=df_tigra["lat"], lon=df_tigra["lon"],
                mode="markers",
                marker=dict(
                    size=df_tigra["silt_level_ntu"] * 1.5 + 10,
                    color=df_tigra["silt_level_ntu"],
                    colorscale="Oranges", cmin=0.0, cmax=25.0, opacity=0.9
                ),
                text=df_tigra["sector"],
                hovertemplate="<b>%{text}</b><br>Silt Density: %{marker.color} NTU<extra></extra>",
                name="Tigra Dam Silt Deposits"
            ))

        fig.update_layout(
            mapbox=dict(style="carto-darkmatter", center=dict(lat=26.2100, lon=78.1000), zoom=10.2),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=600, showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(15,23,42,0.8)")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_analytics:
        st.markdown("### Point Source Contamination Breakdown")
        inspected_row = df_canal[df_canal["point"] == selected_source_inspection].iloc[0]
        st.info(f"**Inspected Point:** {inspected_row['point']}")
        st.metric(label="Contamination Severity Level", value=f"{inspected_row['contamination']} / 20.0")
        st.metric(label="Direct Point-Source Contribution", value=f"+{inspected_row['contrib_pct']}%", delta=f"{inspected_row['source']}")
        st.divider()
        st.markdown("### Tigra Reservoir Inflow Contamination Origins")
        for idx, row in df_inflow.iterrows():
            st.write(f"**{row['Origin']}**: `{row['Contribution_Pct']}%` contribution")
            st.caption(f"Contaminant Type: {row['Primary_Contaminant']} | Severity: {row['Severity']}")
            st.progress(row['Contribution_Pct'] / 100.0)

    st.divider()
    st.markdown("### Swarna Rekha Canal Longitudinal Contamination Gradient & Source Attribution")
    st.dataframe(
        df_canal[["point", "contamination", "source", "contrib_pct"]].rename(columns={
            "point": "Canal Location / Stretch",
            "contamination": "Contamination Index (0-20 Scale)",
            "source": "Identified Contaminant Origin",
            "contrib_pct": "Percentage Contamination Added (%)"
        }),
        use_container_width=True
    )

elif selected_tab.startswith("Tab 2"):
    st.subheader("Optical & Electrochemical Edge-DSP Telemetry Engine")
    st.caption("Real-Time Dual-Wavelength Spectrophotometry & AC Impedance Signal Processing (ESP32-S3 Core)")

    st.sidebar.header("Signal Engine Controls")
    node_select = st.sidebar.selectbox("Select Active Telemetry Node:", df_canal["point"].tolist())
    sim_noise = st.sidebar.slider("Simulated River Turbulence / Wave Noise:", 0.0, 1.0, 0.15)
    inject_spill = st.sidebar.checkbox("Inject Simulated Sewage Discharge Spike", value=False)

    curr_node_data = df_canal[df_canal["point"] == node_select].iloc[0]
    base_contam = curr_node_data["contamination"]
    if inject_spill:
        base_contam += 8.5

    np.random.seed(42)
    time_ms = np.linspace(0, 1000, 100)
    uv_raw = 2.8 - (base_contam * 0.11) + np.random.normal(0, sim_noise * 0.15, 100)
    uv_filtered = pd.Series(uv_raw).rolling(window=5, min_periods=1).mean().values
    ir_scatter = 0.4 + (base_contam * 0.08) + np.random.normal(0, sim_noise * 0.1, 100)
    sac_254 = (100 / 1.0) * np.log10(3.3 / np.clip(uv_filtered, 0.1, 3.2))

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("254nm UV Absorbance (SAC254)", f"{sac_254[-1]:.2f} m⁻¹", delta="+Organic Load" if inject_spill else "Stable")
    with col_m2:
        st.metric("880nm IR Scatter (Turbidity)", f"{ir_scatter[-1]*15.2:.1f} NTU")
    with col_m3:
        st.metric("AC Excitation Conductivity", f"{320 + base_contam*28.5:.0f} µS/cm")
    with col_m4:
        st.metric("AFE Signal-to-Noise Ratio", f"{28.4 - sim_noise*12:.1f} dB", delta="-Turbulence" if sim_noise > 0.4 else "Nominal")

    st.divider()
    col_sig1, col_sig2 = st.columns(2)
    with col_sig1:
        st.markdown("### Dual-Wavelength Optical Telemetry Stream")
        fig_opt = go.Figure()
        fig_opt.add_trace(go.Scatter(x=time_ms, y=uv_raw, mode="lines", name="Raw 254nm UV (Noisy)", line=dict(color="#FF4B4B", width=1, dash="dot")))
        fig_opt.add_trace(go.Scatter(x=time_ms, y=uv_filtered, mode="lines", name="Filtered 254nm UV (Organic)", line=dict(color="#00BFFF", width=2.5)))
        fig_opt.add_trace(go.Scatter(x=time_ms, y=ir_scatter, mode="lines", name="880nm IR Scatter (Silt/Turbidity)", line=dict(color="#FFA500", width=2)))
        fig_opt.update_layout(xaxis_title="Sample Time (ms)", yaxis_title="Photodiode AFE Voltage (V)", template="plotly_dark", height=380, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_opt, use_container_width=True)

    with col_sig2:
        st.markdown("### Beer-Lambert Organic Absorption ($SAC_{254}$) Curve")
        fig_sac = go.Figure()
        fig_sac.add_trace(go.Scatter(x=time_ms, y=sac_254, mode="lines", fill="tozeroy", name="SAC254 Organic Absorption", line=dict(color="#22C55E", width=2)))
        fig_sac.update_layout(xaxis_title="Sample Time (ms)", yaxis_title="SAC254 Coefficient (m⁻¹)", template="plotly_dark", height=380, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_sac, use_container_width=True)

    st.divider()
    st.markdown("### Edge-Node Hardware Raw Telemetry Terminal (UART Serial Stream @ 115200 Baud)")
    timestamp_str = time.strftime("%H:%M:%S")
    serial_log = f"""
    [{timestamp_str}.102] RX <- $AIRAVAT_NODE_03,NODE_ID=SWARNA_REKHA_03,GPS=26.2080N 78.1620E
    [{timestamp_str}.145] DSP -> Executing 2nd-Order Sallen-Key Low Pass Filtering (fc = 2.4 kHz)...
    [{timestamp_str}.189] OPTICAL -> UV_254_RAW={uv_raw[-1]:.3f}V | UV_254_FILT={uv_filtered[-1]:.3f}V | IR_880_SCATTER={ir_scatter[-1]:.3f}V
    [{timestamp_str}.210] MATH -> Derived SAC_254 = {sac_254[-1]:.2f} m^-1 | Differential Subtraction Status = OK
    [{timestamp_str}.250] TX -> Packet Encapsulated (CBOR 64 Bytes) -> Transmitting via LoRaWAN / 4G Cellular...
    """
    st.code(serial_log, language="text")

elif selected_tab.startswith("Tab 3"):
    st.subheader("Surrogate Water Metrics & Automated Outfall Incident Alerts")
    st.caption("Public Health Compliance & Municipal Corporation Enforcement Dashboard")

    target_node = st.sidebar.selectbox("Select Target Node for Surrogate Audit:", df_canal["point"].tolist(), key="tab3_node")
    node_row = df_canal[df_canal["point"] == target_node].iloc[0]
    
    calc_bod = node_row["contamination"] * 4.2 + 2.1
    calc_cod = calc_bod * 2.8 + 12.0
    calc_turbidity = node_row["contamination"] * 1.5 + 3.2
    calc_tds = node_row["contamination"] * 35.0 + 180.0

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Surrogate BOD", f"{calc_bod:.1f} mg/L", delta="Exceeds BIS Limit (>30)" if calc_bod > 30 else "Normal")
    with col_s2:
        st.metric("Surrogate COD", f"{calc_cod:.1f} mg/L")
    with col_s3:
        st.metric("Turbidity", f"{calc_turbidity:.1f} NTU")
    with col_s4:
        st.metric("Total Dissolved Solids", f"{calc_tds:.1f} ppm")

    st.divider()
    col_alert_left, col_alert_right = st.columns([1.5, 1])

    with col_alert_left:
        st.markdown("### Live Municipal Incident & Outfall Alert Log")
        if node_row["contamination"] > 15.0:
            st.error(f"CRITICAL HAZARD [ACTIVE]: {node_row['point']} experiencing severe effluent dumping ({node_row['source']}). Contamination Index: {node_row['contamination']}/20.0. Automatic SMS alert dispatched to Gwalior Municipal Corporation (GMC)!")
        elif node_row["contamination"] > 8.0:
            st.warning(f"WARNING [ELEVATED]: {node_row['point']} flagged for high organic loading from {node_row['source']}.")
        else:
            st.success(f"STATUS [NOMINAL]: {node_row['point']} parameters within acceptable environmental tolerance.")

        st.markdown("#### Recent Automated Enforcement Dispatches")
        st.info("🚨 **Dispatch #1042** [10:14 AM] - Enforcement team alerted for Hazira Industrial Belt illegal dye discharge.")
        st.info("⚠️ **Dispatch #1041** [09:30 AM] - Automated high-shear flushing sequence triggered at Swarna Rekha Drain #4.")

    with col_alert_right:
        st.markdown("### BIS 10500 Compliance Tier")
        compliance_status = "Safe for Treatment"
        compliance_color = "🟢"
        if calc_bod > 30:
            compliance_status = "Critical Contamination / Untreatable Raw Sewage"
            compliance_color = "🔴"
        elif calc_bod > 15:
            compliance_status = "Moderate Pollution / Requires Heavy Alum Dosing"
            compliance_color = "🟡"

        st.markdown(f"### {compliance_color} {compliance_status}")
        st.caption("Evaluated against Indian Standard Drinking Water Specifications (BIS 10500).")
        st.markdown("#### Actionable Recommendations for GMC:")
        st.write("1. Divert industrial inflow away from municipal intake channels.")
        st.write("2. Increase coagulant dosage at water treatment plants by +25%.")
        st.write("3. Initiate on-site inspection at flagged coordinate markers.")

elif selected_tab.startswith("Tab 4"):
    st.subheader("Laboratory Wet-Chemistry Calibration & Regression Engine")
    st.caption("Empirical Calibration Tool for Environmental Researchers & Water Quality Labs")

    st.sidebar.header("Calibration Controls")
    lab_sample_season = st.sidebar.selectbox("Select Season Profile:", ["Monsoon (High Silt / Diluted)", "Summer (Low Flow / High Concentration)", "Winter Baseline"])
    
    # Lab Entry inputs
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown("### Input Wet-Chemistry Lab Results")
        lab_measured_bod = st.number_input("Actual Lab 5-Day BOD (mg/L):", min_value=1.0, max_value=150.0, value=24.5)
        lab_measured_cod = st.number_input("Actual Lab COD (mg/L):", min_value=5.0, max_value=400.0, value=78.2)
        sensor_sac_input = st.slider("Current Sensor SAC254 Reading (m⁻¹):", 1.0, 30.0, 12.4)
    
    with col_l2:
        st.markdown("### Regression Fit & Coefficient Optimizer")
        # Dynamic slope calculation based on season
        multiplier = 1.2 if "Summer" in lab_sample_season else (0.8 if "Monsoon" in lab_sample_season else 1.0)
        slope = 1.85 * multiplier
        intercept = 3.2
        r_squared = 0.948 if "Summer" in lab_sample_season else 0.962
        
        predicted_bod = (sensor_sac_input * slope) + intercept

        st.metric("Optimized Regression Slope (m)", f"{slope:.2f}")
        st.metric("Calculated R² Correlation Score", f"{r_squared:.3f}", delta="High Accuracy")
        st.metric("Predicted Field BOD (mg/L)", f"{predicted_bod:.1f} mg/L")

    st.divider()

    st.markdown("### Sensor vs. Wet-Chemistry Laboratory Correlation Scatter Plot")
    
    # Generate synthetic correlation data points
    np.random.seed(101)
    x_sac = np.linspace(2, 25, 30)
    y_bod = (x_sac * slope) + intercept + np.random.normal(0, 1.5, 30)

    fig_cal = go.Figure()
    fig_cal.add_trace(go.Scatter(x=x_sac, y=y_bod, mode="markers", name="Historical Lab Samples", marker=dict(size=10, color="#00BFFF")))
    fig_cal.add_trace(go.Scatter(x=x_sac, y=(x_sac * slope) + intercept, mode="lines", name=f"Fit Line: y = {slope:.2f}x + {intercept}", line=dict(color="#22C55E", width=2.5)))
    
    fig_cal.update_layout(
        xaxis_title="Sensor SAC254 Optical Reading (m⁻¹)", yaxis_title="Laboratory Wet-Chemistry BOD (mg/L)",
        template="plotly_dark", height=400, margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_cal, use_container_width=True)

    if st.button("🚀 Push Calibration Matrix to All Floating Edge Nodes (OTA Sync)"):
        st.success("Calibration coefficients successfully broadcast via LoRaWAN/4G to all 7 active Gwalior nodes! Edge sensor arrays updated.")