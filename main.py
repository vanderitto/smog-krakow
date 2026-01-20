import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("WAQI_TOKEN")
DB_PASS = os.getenv("DB_PASSWORD")

db_url = f'postgresql://myuser:{DB_PASS}@localhost:5432/weather_db'
engine = create_engine(db_url)

DZIELNICE = {
    "Dzielnica I Stare Miasto": [50.061, 19.937],
    "Dzielnica II Grzegórzki": [50.057, 19.965],
    "Dzielnica III Prądnik Czerwony": [50.088, 19.980],
    "Dzielnica IV Prądnik Biały": [50.091, 19.921],
    "Dzielnica V Krowodrza": [50.073, 19.919],
    "Dzielnica VI Bronowice": [50.076, 19.889],
    "Dzielnica VII Zwierzyniec": [50.055, 19.870],
    "Dzielnica VIII Dębniki": [50.035, 19.900],
    "Dzielnica IX Łagiewniki-Borek Fałęcki": [50.019, 19.933],
    "Dzielnica X Swoszowice": [49.995, 19.940],
    "Dzielnica XI Podgórze Duchackie": [50.015, 19.960],
    "Dzielnica XII Bieżanów-Prokocim": [50.017, 20.016],
    "Dzielnica XIII Podgórze": [50.043, 19.955],
    "Dzielnica XIV Czyżyny": [50.065, 20.010],
    "Dzielnica XV Mistrzejowice": [50.095, 20.015],
    "Dzielnica XVI Bieńczyce": [50.085, 20.030],
    "Dzielnica XVII Wzgórza Krzesławickie": [50.090, 20.060],
    "Dzielnica XVIII Nowa Huta": [50.070, 20.070]
}

def pobierz_smog_krakow():
    teraz = datetime.now()
    print(f"\n[{teraz.strftime('%H:%M:%S')}] 🐲 Sprawdzam 18 dzielnic Krakowa...")
    
    lista_danych = []

    for nazwa, coords in DZIELNICE.items():
        lat, lon = coords
        url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={TOKEN}"
        
        try:
            response = requests.get(url)
            dane = response.json()
            
            if dane['status'] == 'ok':
                wynik = dane['data']
                aqi = wynik['aqi']
                
                geo = wynik.get('city', {}).get('geo', [lat, lon])
                
                opis = "DOBRE"
                if aqi > 50: opis = "ŚREDNIE"
                if aqi > 100: opis = "ZŁE"
                if aqi > 150: opis = "TRAGICZNE"
                
                lista_danych.append({
                    "czas": teraz,
                    "miasto": nazwa, 
                    "aqi": aqi,
                    "stan": opis,
                    "lat": geo[0],
                    "lon": geo[1]
                })
                print(f" -> {nazwa}: AQI {aqi}")
            else:
                print(f" -> Brak danych dla {nazwa}")

        except Exception as e:
            print(f" -> Błąd połączenia: {e}")

    if lista_danych:
        df = pd.DataFrame(lista_danych)
        df.to_sql('smog_polska', engine, if_exists='append', index=False)
        print("✅ Dane zapisane w bazie.")
    else:
        print("⚠️ Nie pobrano żadnych danych.")

if __name__ == "__main__":
    pobierz_smog_krakow()
    schedule.every(1).hours.do(pobierz_smog_krakow)

    while True:
        schedule.run_pending()
        time.sleep(1)