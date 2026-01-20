import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from sqlalchemy import create_engine
import os
import glob
import json 
from dotenv import load_dotenv

st.set_page_config(page_title="Smog Kraków (Auto)", page_icon="🗺️", layout="wide")
load_dotenv()

st.title("🗺️ Kraków Smog: Mapa Dzielnic")

PLIKI_GEOJSON = glob.glob("*.geojson")

if not PLIKI_GEOJSON:
    st.error("❌ BŁĄD: Nie widzę plików .geojson w folderze!")
    st.stop()
else:
    st.success(f"✅ Załadowano {len(PLIKI_GEOJSON)} map dzielnic.")

DB_PASS = os.getenv("DB_PASSWORD")
if not DB_PASS:
    st.error("Brak hasła w pliku .env")
    st.stop()

db_url = f'postgresql://myuser:{DB_PASS}@localhost:5432/weather_db'
engine = create_engine(db_url)

def get_data():
    try:
        query = """
            SELECT DISTINCT ON (miasto) * FROM smog_polska 
            ORDER BY miasto, czas DESC;
        """
        df = pd.read_sql(query, engine)
        
        df = df[df['miasto'].str.startswith('Dzielnica')]
        
        def wybierz_kolor(aqi):
            if aqi <= 50: return 'green'
            elif aqi <= 100: return 'orange'
            else: return 'red'
            
        if not df.empty:
            df['kolor'] = df['aqi'].apply(wybierz_kolor)
            
        return df
    except Exception as e:
        st.error(f"Błąd bazy: {e}")
        return pd.DataFrame()


if st.sidebar.button("🔄 Odśwież dane"):
    st.rerun()

df = get_data()

if not df.empty:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Aktualne Pomiary")
        tabela = df[['miasto', 'aqi', 'stan']].sort_values(by='aqi', ascending=False)
        st.dataframe(tabela, hide_index=True, height=500)

    with col2:
        m = folium.Map(location=[50.0647, 19.9450], zoom_start=11)

        for plik in PLIKI_GEOJSON:
            try:
                with open(plik, 'r', encoding='utf-8') as f:
                    geo_data = json.load(f)
                
                nazwa_ladna = os.path.basename(plik).replace(".geojson", "").replace("_", " ").title()

                dane_naprawione = {
                    "type": "Feature",
                    "geometry": geo_data,  
                    "properties": {"name": nazwa_ladna} 
                }

                folium.GeoJson(
                    dane_naprawione,
                    name=nazwa_ladna,
                    style_function=lambda x: {
                        'fillColor': 'blue',
                        'fillOpacity': 0.05,
                        'color': 'gray',
                        'weight': 1,
                        'dashArray': '5, 5'
                    },
                    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Obszar:'], labels=False) 
                ).add_to(m)
            except Exception as e:
                st.warning(f"Nie udało się wczytać mapy: {plik} ({e})")

        for index, row in df.iterrows():
            html = f"<b>{row['miasto']}</b><br>AQI: {row['aqi']}<br>{row['stan']}"
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=12,
                color='black',
                weight=1,
                fill=True,
                fill_color=row['kolor'],
                fill_opacity=0.8,
                popup=folium.Popup(html, max_width=200),
                tooltip=f"{row['miasto']}: {row['aqi']}"
            ).add_to(m)

        st_folium(m, width=800, height=600, returned_objects=[])

else:
    st.info("Baza jest połączona, ale main.py jeszcze nie zapisał danych dla dzielnic.")