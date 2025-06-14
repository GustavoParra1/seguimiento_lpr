import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# --- Carga de datos ---
df_camaras = pd.read_csv("camaraslpr.csv", encoding="latin-1")
df_relaciones = pd.read_csv("relaciones.csv")

# --- Selección UI de LPR ---
lprs = df_camaras[df_camaras["Tipo"] == "LPR"]["ID_Camara"].tolist()
lpr_sel = st.selectbox("Seleccioná una cámara LPR", lprs)

lpr_info = df_camaras[df_camaras["ID_Camara"] == lpr_sel].iloc[0]
lat_lpr, lon_lpr = lpr_info["Latitud"], lpr_info["Longitud"]
# Reemplazar comas por puntos y convertir a float
df_camaras['latitud'] = df_camaras['latitud'].str.replace(',', '.', regex=False).astype(float)
df_camaras['longitud'] = df_camaras['longitud'].str.replace(',', '.', regex=False).astype(float)


rel = df_relaciones[df_relaciones["LPR_ID"] == lpr_sel]
if not rel.empty:
    cams_rel = [c.strip() for c in rel.iloc[0]["Camaras_Seguimiento"].split(",")]
else:
    cams_rel = []

# --- Mapa con Folium ---
m = folium.Map(location=[lat_lpr, lon_lpr], zoom_start=15)
cluster = MarkerCluster().add_to(m)

for _, r in df_camaras.iterrows():
    cid, lat, lon = r["ID_Camara"], r["Latitud"], r["Longitud"]
    if cid == lpr_sel:
        color, icon = "red", "star"
    elif cid in cams_rel:
        color, icon = "blue", "camera"
    else:
        color, icon = "gray", "circle"
    folium.Marker(
        [lat, lon],
        popup=cid,
        icon=folium.Icon(color=color, icon=icon, prefix="fa")
    ).add_to(cluster)

st.title("Seguimiento desde cámara LPR")
st.markdown(f"**LPR seleccionada:** {lpr_sel}")
st_folium(m, width=700, height=500)
