import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Cargar datos
df = pd.read_csv("camaraslpr.csv", encoding="latin-1")

# Convertir lat/lon a float (estaban con coma decimal)
df['latitud'] = df['latitud'].str.replace(',', '.', regex=False).astype(float)
df['longitud'] = df['longitud'].str.replace(',', '.', regex=False).astype(float)

# Separar cámaras por tipo
df_lpr = df[df['Tipo'].str.lower() == 'lpr']
df_comunes = df[df['Tipo'].str.lower() == 'común']

# Sidebar: selección de cámara LPR
st.sidebar.title("Seguimiento desde LPR")
camara_lpr_sel = st.sidebar.selectbox(
    "Seleccioná una cámara LPR",
    df_lpr['id_cámara LPR'].unique()
)

# Cargar coordenadas de esa cámara
camara_base = df_lpr[df_lpr['id_cámara LPR'] == camara_lpr_sel].iloc[0]
ubicacion_base = (camara_base['latitud'], camara_base['longitud'])

# Crear mapa
m = folium.Map(location=ubicacion_base, zoom_start=14)

# Cámara LPR seleccionada
folium.Marker(
    ubicacion_base,
    tooltip=f"LPR Seleccionada: {camara_lpr_sel}",
    icon=folium.Icon(color="red", icon="camera", prefix="fa")
).add_to(m)

# Cámaras comunes asociadas (ejemplo: en radio de 500 metros)
from geopy.distance import geodesic

radio_metros = 500

for _, row in df_comunes.iterrows():
    ubicacion_comun = (row['latitud'], row['longitud'])
    distancia = geodesic(ubicacion_base, ubicacion_comun).meters
    if distancia <= radio_metros:
        folium.Marker(
            ubicacion_comun,
            tooltip=f"Común ID: {row['id_cámara']}",
            icon=folium.Icon(color="blue", icon="video-camera", prefix="fa")
        ).add_to(m)

# Mostrar mapa
st.title("Seguimiento desde cámara LPR")
st.markdown(f"Mostrando cámaras comunes a menos de {radio_metros} metros de **{camara_lpr_sel}**.")
st_folium(m, width=700, height=500)

