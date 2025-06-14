import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from geopy.distance import geodesic
import unicodedata

# Cargar datos
df = pd.read_csv("camaraslpr.csv", encoding="latin-1")

# Normalizar columnas
df.columns = df.columns.str.strip()

# Arreglar codificación de tipo: sin tildes, todo en minúsculas
df['Tipo'] = df['Tipo'].apply(lambda x: unicodedata.normalize('NFKD', x.lower()).encode('ascii', errors='ignore').decode())

# Convertir lat/lon a float
df['latitud'] = df['latitud'].astype(str).str.replace(',', '.', regex=False).astype(float)
df['longitud'] = df['longitud'].astype(str).str.replace(',', '.', regex=False).astype(float)

# Separar cámaras
df_lpr = df[df['Tipo'] == 'lpr']
df_comunes = df[df['Tipo'] == 'comun']

# Sidebar: seleccionar cámara LPR
st.sidebar.title("Seguimiento desde LPR")
camara_lpr_sel = st.sidebar.selectbox(
    "Seleccioná una cámara LPR",
    df_lpr['id_camara LPR'].unique()
)

# Coordenadas base
camara_base = df_lpr[df_lpr['id_camara LPR'] == camara_lpr_sel].iloc[0]
ubicacion_base = (camara_base['latitud'], camara_base['longitud'])

# Parámetro: radio en metros
radio_m = 3000

# Mapa base
m = folium.Map(location=ubicacion_base, zoom_start=14)

# Marcar cámara LPR seleccionada
folium.Marker(
    ubicacion_base,
    tooltip=f"Cámara LPR ID: {camara_lpr_sel}",
    icon=folium.Icon(color="red", icon="camera", prefix="fa")
).add_to(m)

# Dibujar círculo de alcance
folium.Circle(
    location=ubicacion_base,
    radius=radio_m,
    color='red',
    fill=True,
    fill_opacity=0.1
).add_to(m)

# Filtrar y marcar cámaras comunes dentro del radio
camaras_en_rango = []

for _, row in df_comunes.iterrows():
    ubic_comun = (row['latitud'], row['longitud'])
    dist = geodesic(ubicacion_base, ubic_comun).meters
    if dist <= radio_m:
        camaras_en_rango.append({
            'ID': row['id_camara'],
            'Latitud': row['latitud'],
            'Longitud': row['longitud'],
            'Distancia (m)': round(dist, 2)
        })
        folium.Marker(
            ubic_comun,
            tooltip=f"Cámara común ID: {row['id_camara']} ({round(dist)} m)",
            icon=folium.Icon(color="blue", icon="video-camera", prefix="fa")
        ).add_to(m)

# Mostrar en la app
st.title("Seguimiento desde cámara LPR")
st.markdown(f"Se muestran cámaras comunes a menos de **{radio_m} m** de la cámara **{camara_lpr_sel}**.")
st_folium(m, width=700, height=500)

# Mostrar tabla de cámaras en el rango
if camaras_en_rango:
    st.subheader("📋 Cámaras comunes cercanas (color azul)")
    df_rango = pd.DataFrame(camaras_en_rango)
    st.dataframe(df_rango)
else:
    st.info("No hay cámaras comunes dentro del radio especificado.")
