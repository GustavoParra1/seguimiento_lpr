import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from geopy.distance import geodesic

# Cargar datos
df = pd.read_csv("camaraslpr.csv", encoding="latin-1")

# Convertir lat/lon a float (tenían comas)
df['latitud'] = df['latitud'].str.replace(',', '.', regex=False).astype(float)
df['longitud'] = df['longitud'].str.replace(',', '.', regex=False).astype(float)

# Separar cámaras
df_lpr = df[df['Tipo'].str.lower() == 'lpr']
df_comunes = df[df['Tipo'].str.lower() == 'común']

# Sidebar: cámara LPR
st.sidebar.title("Seguimiento desde LPR")
camara_lpr_sel = st.sidebar.selectbox(
    "Seleccioná una cámara LPR",
    df_lpr['id_cámara LPR'].unique()
)

# Coordenadas base
camara_base = df_lpr[df_lpr['id_cámara LPR'] == camara_lpr_sel].iloc[0]
ubicacion_base = (camara_base['latitud'], camara_base['longitud'])

# Mapa base
m = folium.Map(location=ubicacion_base, zoom_start=14)

# Marcar cámara LPR
# Círculo rojo alrededor de la cámara LPR
folium.CircleMarker(
    location=ubicacion_base,
    radius=15,
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.3,
    tooltip=f"Círculo de referencia LPR: {camara_lpr_sel}"
).add_to(m)


# Marcar cámaras comunes en un radio
radio_m = 500
for _, row in df_comunes.iterrows():
    ubic_comun = (row['latitud'], row['longitud'])
    dist = geodesic(ubicacion_base, ubic_comun).meters
    if dist <= radio_m:
        folium.Marker(
            ubic_comun,
            tooltip=f"Común ID: {row['id_cámara']}",
            folium.Icon(color="blue", icon="video-camera", prefix="fa")
        ).add_to(m)

# Mostrar
st.title("Seguimiento desde cámara LPR")
st.markdown(f"Se muestran cámaras comunes a menos de **{radio_m} m** de la cámara **{camara_lpr_sel}**.")
st_folium(m, width=700, height=500)
