import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# --- Cargar datos ---
df_camaras = pd.read_csv("camaras.csv")
df_relaciones = pd.read_csv("relaciones.csv")

# --- UI: Seleccionar LPR ---
lprs_disponibles = df_camaras[df_camaras["Tipo"] == "LPR"]["ID_Camara"].tolist()
lpr_seleccionada = st.selectbox("Seleccioná una cámara LPR", lprs_disponibles)

# --- Ubicación de la LPR ---
lpr_info = df_camaras[df_camaras["ID_Camara"] == lpr_seleccionada].iloc[0]
lat_lpr = lpr_info["Latitud"]
lon_lpr = lpr_info["Longitud"]

# --- Cámaras relacionadas ---
relacion = df_relaciones[df_relaciones["LPR_ID"] == lpr_seleccionada]
if not relacion.empty:
    camaras_relacionadas = relacion.iloc[0]["Camaras_Seguimiento"].split(",")
    camaras_relacionadas = [c.strip() for c in camaras_relacionadas]
else:
    camaras_relacionadas = []

# --- Mapa ---
m = folium.Map(location=[lat_lpr, lon_lpr], zoom_start=15)
marker_cluster = MarkerCluster().add_to(m)

# Marcar todas las cámaras
for idx, row in df_camaras.iterrows():
    cam_id = row["ID_Camara"]
    lat = row["Latitud"]
    lon = row["Longitud"]

    if cam_id == lpr_seleccionada:
        color = "red"
        icon = "star"
    elif cam_id in camaras_relacionadas:
        color = "blue"
        icon = "camera"
    else:
        color = "gray"
        icon = "circle"

    folium.Marker(
        location=[lat, lon],
        popup=cam_id,
        icon=folium.Icon(color=color, icon=icon, prefix='fa')
    ).add_to(marker_cluster)

st.title("Seguimiento desde cámara LPR")
st.markdown(f"**LPR seleccionada:** {lpr_seleccionada}")
st_folium(m, width=700, height=500)
