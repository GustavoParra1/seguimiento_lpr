# Seguimiento de Vehículos desde LPR

Este proyecto permite:
- Seleccionar una cámara LPR.
- Mostrar en un mapa todas sus cámaras comunes asociadas.

## Instalación

```bash
git clone https://github.com/TU-USUARIO/seguimiento-lpr.git
cd seguimiento-lpr
python3 -m venv venv
source venv/bin/activate
pip install streamlit pandas folium streamlit-folium
streamlit run seguimiento_lpr.py
