import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
# SWARNA REKHA CANAL ROUTE DATA (Gwalior City GPS Points)
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

# ---------------------------------------------------------
# TIGRA RESERVOIR SILT & INFLOW ORIGIN DATA
# ---------------------------------------------------------
tigra_silt_data = [
    {"sector": "Tigra Spillway Deep Zone", "lat": 26.2167, "lon": 78.0167, "silt_level_ntu": 4.2, "status": "Low Silt"},
    {"sector": "Sank River Intake Mouth", "lat": 26.2100, "lon": 78.0050, "silt_level_ntu": 18.6, "status": "Critical Silt Deposit"},
    {"sector": "Kullu Catchment Basin", "lat": 26.2250, "lon": 78.0250, "silt_level_ntu": 12.4, "status": "Moderate Silt"},
    {"sector": "Southern Feeder Channel", "lat": 26.2020, "lon": 78.0120, "silt_level_ntu": 15.8, "status": "High Silt"}
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
        # Heatmap Gradient (0.0 Light Yellow -> 20.0 Dark Maroon/Black)
        heatmap_colorscale = [
            [0.0, "#FFFFE0"],   # Light Yellow (0.0)
            [0.2, "#FFD700"],   # Gold/Yellow (4.0)
            [0.4, "#FF7F00"],   # Orange (8.0)
            [0.6, "#E60000"],   # Red (12.0)
            [0.8, "#800000"],   # Dark Maroon (16.0)
            [1.0, "#1A0000"]    # Dark Near-Black (20.0)
        ]

        fig = px.scatter_mapbox(
            df_canal if show_canal else pd.DataFrame(),
            lat="lat",
            lon="lon",
            color="contamination",
            size="contamination",
            color_continuous_scale=heatmap_colorscale,
            range_color=[0.0, 20.0],
            hover_name="point",
            hover_data={"source": True, "contrib_pct": ":.1f%", "contamination": ":.1f", "lat": False, "lon": False},
            zoom=10.5,
            center={"lat": 26.2180, "lon": 78.1200},
            height=600,
            mapbox_style="carto-darkmatter"
        )

        # Overlay Blue Canal Flow Vector Line
        if show_flow_line:
            fig.add_trace(go.Scattermapbox(
                lat=df_canal["lat"],
                lon=df_canal["lon"],
                mode="lines",
                line=dict(width=4, color="#1E90FF"),
                name="Swarna Rekha Blue Water Flow",
                hoverinfo="none"
            ))

        # Overlay Tigra Reservoir Silt Deposits
        if show_tigra:
            fig.add_trace(go.Scattermapbox(
                lat=df_tigra["lat"],
                lon=df_tigra["lon"],
                mode="markers",
                marker=dict(
                    size=df_tigra["silt_level_ntu"] * 1.2 + 8,
                    color=df_tigra["silt_level_ntu"],
                    colorscale="YlOrRd",
                    opacity=0.85
                ),
                text=df_tigra["sector"],
                hovertemplate="<b>%{text}</b><br>Silt Level: %{marker.color} NTU<extra></extra>",
                name="Tigra Reservoir Silt Deposits"
            ))

        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(15,23,42,0.8)"),
            coloraxis_colorbar=dict(
                title="Contamination Scale",
                x=1.01,
                len=0.85
            )
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
        st.caption("City/Catchment sources contributing to Tigra Dam raw water inflow:")
        
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
    st.info("Tab 2: Optical & Electrochemical Signal Engine (Ready for Integration)")

elif selected_tab.startswith("Tab 3"):
    st.info("Tab 3: Surrogate Water Metrics & Alerts (Ready for Integration)")

elif selected_tab.startswith("Tab 4"):
    st.info("Tab 4: Lab Calibration Engine (Ready for Integration)")