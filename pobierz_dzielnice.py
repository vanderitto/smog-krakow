import requests
import os
import time

# Mapa: Nazwa pliku na GitHub -> Nazwa, którą Ty chcesz mieć
PLIKI = {
    "dzielnica i stare miasto.geojson": "dzielnica_I.geojson",
    "dzielnica ii grzegórzki.geojson": "dzielnica_II.geojson",
    "dzielnica iii prądnik czerwony.geojson": "dzielnica_III.geojson",
    "dzielnica iv prądnik biały.geojson": "dzielnica_IV.geojson",
    "dzielnica v krowodrza.geojson": "dzielnica_V.geojson",
    "dzielnica vi bronowice.geojson": "dzielnica_VI.geojson",
    "dzielnica vii zwierzyniec.geojson": "dzielnica_VII.geojson",
    "dzielnica viii dębniki.geojson": "dzielnica_VIII.geojson",
    "dzielnica ix łagiewniki-borek fałęcki.geojson": "dzielnica_IX.geojson",
    "dzielnica x swoszowice.geojson": "dzielnica_X.geojson",
    "dzielnica xi podgórze duchackie.geojson": "dzielnica_XI.geojson",
    "dzielnica xii biezanow-prokocim.geojson": "dzielnica_XII.geojson",
    "dzielnica xiii podgórze.geojson": "dzielnica_XIII.geojson",
    "dzielnica xiv czyżyny.geojson": "dzielnica_XIV.geojson",
    "dzielnica xv mistrzejowice.geojson": "dzielnica_XV.geojson",
    "dzielnica xvi bieńczyce.geojson": "dzielnica_XVI.geojson",
    "dzielnica xvii wzgórza krzeszławickie.geojson": "dzielnica_XVII.geojson",
    "dzielnica xviii nowa huta.geojson": "dzielnica_XVIII.geojson"
}

BASE_URL = "https://raw.githubusercontent.com/andilabs/krakow-dzielnice-geojson/master/"

print("⬇️ Rozpoczynam pobieranie 18 dzielnic...")

for github_name, my_name in PLIKI.items():
    # GitHub nie lubi spacji w linkach, zamieniamy je na %20
    safe_url = BASE_URL + github_name.replace(" ", "%20")
    
    try:
        response = requests.get(safe_url)
        response.raise_for_status()
        
        # Zapisujemy poprawny plik JSON
        with open(my_name, 'wb') as f:
            f.write(response.content)
            
        print(f"✅ Pobrano: {my_name}")
    except Exception as e:
        print(f"❌ Błąd przy {my_name}: {e}")
    
    time.sleep(0.5) # Mała przerwa, żeby GitHub nas nie zablokował

print("\n🎉 Gotowe! Masz teraz poprawne pliki GeoJSON.")