import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import unicodedata

# Cargar datos
df = pd.read_csv("camaraslpr.csv", encoding="latin-1")
df.columns = df.columns.str.strip()

# Normalizar texto en 'Tipo'
df['Tipo'] = df['Tipo'].apply(lambda x: unicodedata.normalize('NFKD', x.lower()).encode('ascii', errors='ignore').decode())

# Convertir coordenadas
df['latitud'] = df['latitud'].astype(str).str.replace(',', '.', regex=False).astype(float)
df['longitud'] = df['longitud'].astype(str).str.replace(',', '.', regex=False).astype(float)

# Separar cámaras
df['Tipo'] = df['Tipo'].astype(str).str.strip().str.lower()
df_lpr = df[df['Tipo'].str.contains('lpr')]
df_comunes = df[df['Tipo'].str.contains('común')]

# Sidebar
st.sidebar.title("Seguimiento desde LPR")
camara_lpr_sel = st.sidebar.selectbox("Seleccioná una cámara LPR", df_lpr['id_camara LPR'].unique())

# Datos de la cámara LPR elegida
camara_base = df_lpr[df_lpr['id_camara LPR'] == camara_lpr_sel].iloc[0]
ubicacion_base = (camara_base['latitud'], camara_base['longitud'])

# Radio
radio_m = 2000
m = folium.Map(location=ubicacion_base, zoom_start=14)

# Agregar marcador LPR (rojo)
folium.Marker(
    location=ubicacion_base,
    tooltip=f"LPR ID: {camara_lpr_sel}",
    icon=folium.Icon(color="red", icon="camera", prefix="fa")
).add_to(m)

# Mostrar ID de LPR como texto encima
folium.map.Marker(
    ubicacion_base,
    icon=folium.DivIcon(
        html=f"""<div style="font-size: 21px; color: red; font-weight: bold">{camara_lpr_sel}</div>"""
    )
).add_to(m)

# Círculo del radio
folium.Circle(
    location=ubicacion_base,
    radius=radio_m,
    color='red',
    fill=True,
    fill_opacity=0.1
).add_to(m)

# Cámaras comunes cercanas
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

        # Marcador azul
        folium.Marker(
            ubic_comun,
            tooltip=f"Común ID: {row['id_camara']} ({round(dist)} m)",
            icon=folium.Icon(color="blue", icon="video-camera", prefix="fa")
        ).add_to(m)

        # Mostrar ID como texto azul
        folium.map.Marker(
            ubic_comun,
            icon=folium.DivIcon(
                html=f"""<div style="font-size: 21px; color: blue; font-weight: bold">{row['id_camara']}</div>"""
            )
        ).add_to(m)

# Mostrar mapa
st.title("Seguimiento desde cámara LPR")
st.markdown(f"Cámaras comunes a menos de **{radio_m} m** de la LPR **{camara_lpr_sel}**:")
st_folium(m, width=1000, height=700)

# Mostrar tabla
if camaras_en_rango:
    st.subheader("📋 Cámaras comunes en rango (azules):")
    df_rango = pd.DataFrame(camaras_en_rango)
    st.dataframe(df_rango)
else:
    st.info("No hay cámaras comunes dentro del radio.")"
                                                         ^
