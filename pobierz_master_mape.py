import requests
import os

# To jest sprawdzony, precyzyjny plik z granicami wszystkich dzielnic w jednym
URL = "https://raw.githubusercontent.com/tomekloch/sierotki/master/krakow-dzielnice.geojson"
NAZWA_PLIKU = "krakow_dzielnice_master.geojson"

print(f"⬇️ Pobieram precyzyjną mapę Krakowa...")

try:
    response = requests.get(URL)
    response.raise_for_status()
    
    # Zapisz zawartość
    with open(NAZWA_PLIKU, "wb") as f:
        f.write(response.content)
        
    print(f"✅ SUKCES! Zapisano plik: {NAZWA_PLIKU}")
    print("   To jest jeden plik zawierający wszystkie 18 dzielnic.")
    
except Exception as e:
    print(f"❌ Błąd: {e}")