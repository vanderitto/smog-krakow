import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from sqlalchemy import create_engine
import os
import json
import glob
from dotenv import load_dotenv

st.set_page_config(page_title="Smog Kraków (Final)", page_icon="🐲", layout="wide")
load_dotenv()

st.title("🐲 Kraków Smog: Mapa Dzielnic")

# --- 1. KONFIGURACJA ---
DB_PASS = os.getenv("DB_PASSWORD")
if not DB_PASS:
    st.error("Brak hasła w pliku .env")
    st.stop()

db_url = f'postgresql://myuser:{DB_PASS}@localhost:5432/weather_db'
engine = create_engine(db_url)

# --- 2. MAPOWANIE (Tego brakowało!) ---
# Klucz: Nazwa pliku (bez .geojson) widoczna u Ciebie w folderze
# Wartość: Dokładna nazwa dzielnicy w Twojej bazie danych
MAPOWANIE = {
    "dzielnica_I": "Dzielnica I Stare Miasto",
    "dzielnica_II": "Dzielnica II Grzegórzki",
    "dzielnica_III": "Dzielnica III Prądnik Czerwony",
    "dzielnica_IV": "Dzielnica IV Prądnik Biały",
    "dzielnica_V": "Dzielnica V Krowodrza",
    "dzielnica_VI": "Dzielnica VI Bronowice",
    "dzielnica_VII": "Dzielnica VII Zwierzyniec",
    "dzielnica_VIII": "Dzielnica VIII Dębniki",
    "dzielnica_IX": "Dzielnica IX Łagiewniki-Borek Fałęcki",
    "dzielnica_X": "Dzielnica X Swoszowice",
    "dzielnica_XI": "Dzielnica XI Podgórze Duchackie",
    "dzielnica_XII": "Dzielnica XII Bieżanów-Prokocim",
    "dzielnica_XIII": "Dzielnica XIII Podgórze",
    "dzielnica_XIV": "Dzielnica XIV Czyżyny",
    "dzielnica_XV": "Dzielnica XV Mistrzejowice",
    "dzielnica_XVI": "Dzielnica XVI Bieńczyce",
    "dzielnica_XVII": "Dzielnica XVII Wzgórza Krzesławickie",
    "dzielnica_XVIII": "Dzielnica XVIII Nowa Huta"
}

# --- 3. POBIERANIE DANYCH ---
def get_data():
    try:
        query = "SELECT DISTINCT ON (miasto) * FROM smog_polska ORDER BY miasto, czas DESC;"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        return pd.DataFrame()

df = get_data()

# --- 4. INTERFEJS ---
if st.sidebar.button("🔄 Odśwież dane"):
    st.rerun()

if df.empty:
    st.error("❌ Baza danych jest pusta! Uruchom najpierw main.py.")
    st.stop()

# --- 5. INTERAKTYWNA TABELA ---
col1, col2 = st.columns([1, 2])
wybrana_dzielnica = None

with col1:
    st.subheader("📊 Wybierz dzielnicę")
    tabela_view = df[['miasto', 'aqi', 'stan']].sort_values(by='aqi', ascending=False)
    tabela_view.columns = ['Dzielnica', 'AQI', 'Stan']
    
    event = st.dataframe(
        tabela_view,
        hide_index=True,
        use_container_width=True,
        height=500,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    if len(event.selection.rows) > 0:
        idx = event.selection.rows[0]
        wybrana_dzielnica = tabela_view.iloc[idx]['Dzielnica']

# --- 6. MAPA ---
with col2:
    # Słowniki danych
    aqi_dict = df.set_index('miasto')['aqi'].to_dict()
    stan_dict = df.set_index('miasto')['stan'].to_dict()

    m = folium.Map(location=[50.0647, 19.9450], zoom_start=11, tiles="CartoDB positron")
    
    pliki_na_dysku = glob.glob("*.geojson")
    
    for sciezka_pliku in pliki_na_dysku:
        klucz_pliku = os.path.basename(sciezka_pliku).replace(".geojson", "")
        
        if klucz_pliku in MAPOWANIE:
            nazwa_w_bazie = MAPOWANIE[klucz_pliku]
            
            # Pobieramy dane
            aqi = aqi_dict.get(nazwa_w_bazie)
            stan = stan_dict.get(nazwa_w_bazie, "Brak danych")
            
            # Kolory
            fill_color = 'gray'
            if aqi:
                if aqi <= 50: fill_color = '#00CC00'
                elif aqi <= 100: fill_color = '#FF9900'
                else: fill_color = '#CC0000'
            
            # Logika podświetlania (jeśli kliknięto w tabeli)
            czy_aktywna = (nazwa_w_bazie == wybrana_dzielnica)
            opacity = 0.8 if czy_aktywna else 0.5
            line_weight = 4 if czy_aktywna else 1
            line_color = 'black' if czy_aktywna else 'white'

            try:
                with open(sciezka_pliku, 'r', encoding='utf-8') as f:
                    geo_data = json.load(f)
                
                # Budujemy Feature
                feature = {
                    "type": "Feature",
                    "geometry": geo_data,
                    "properties": {
                        "name": nazwa_w_bazie,
                        "aqi": str(aqi) if aqi else "Brak",
                        "stan": stan
                    }
                }
                
                folium.GeoJson(
                    feature,
                    name=nazwa_w_bazie,
                    style_function=lambda x, fc=fill_color, op=opacity, lw=line_weight, lc=line_color: {
                        'fillColor': fc,
                        'fillOpacity': op,
                        'color': lc,
                        'weight': lw,
                    },
                    # To odpowiada za podświetlenie po najechaniu myszką (hover)
                    highlight_function=lambda x: {
                        'weight': 3, 
                        'color': '#666',
                        'fillOpacity': 0.8
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=['name', 'aqi', 'stan'],
                        aliases=['Dzielnica:', 'AQI:', 'Stan:'],
                        style="font-size: 14px"
                    )
                ).add_to(m)
                
            except Exception as e:
                st.error(f"Błąd pliku {sciezka_pliku}: {e}")

    st_folium(m, width=900, height=700, returned_objects=[])