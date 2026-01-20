# 🐲 Kraków Smog Monitor

Interaktywna aplikacja monitorująca jakość powietrza w 18 dzielnicach Krakowa w czasie rzeczywistym. Projekt łączy pobieranie danych z zewnętrznego API, składowanie ich w bazie PostgreSQL oraz wizualizację na mapie.

## 📸 Podgląd




## 🚀 Funkcjonalności

* **Real-time Data:** Automatyczne pobieranie danych o jakości powietrza (AQI) dla każdej z 18 dzielnic Krakowa (API WAQI).
* **Data Engineering:** Proces ETL (Extract, Transform, Load) zapisujący dane historyczne do bazy PostgreSQL.
* **Geospatial Visualization:** Interaktywna mapa Krakowa z podziałem na oficjalne granice dzielnic (GeoJSON) i kolorystycznym oznaczeniem stanu powietrza.
* **Dockerized Database:** Baza danych uruchamiana w bezpiecznym kontenerze Docker.

## 🛠️ Technologie

* **Python 3.11+**
* **Streamlit** (Frontend & Dashboard)
* **Folium & GeoJSON** (Mapy)
* **PostgreSQL** (Baza danych)
* **Docker** (Konteneryzacja)
* **SQLAlchemy & Pandas** (Obsługa danych)

## ⚙️ Instalacja i Uruchomienie

1.  **Sklonuj repozytorium:**
    ```bash
    git clone [https://github.com/TWOJA_NAZWA_UZYTKOWNIKA/smog-krakow.git](https://github.com/TWOJA_NAZWA_UZYTKOWNIKA/smog-krakow.git)
    cd smog-krakow
    ```

2.  **Stwórz plik `.env`:**
    Utwórz plik `.env` w głównym katalogu i dodaj swoje klucze:
    ```text
    WAQI_TOKEN=twoj_token_z_aqicn_org
    DB_PASSWORD=twoje_haslo_do_bazy
    ```

3.  **Zainstaluj biblioteki:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uruchom bazę danych (Docker):**
    *(Upewnij się, że masz plik docker-compose.yml lub uruchomioną bazę Postgres)*

5. **Uruchom aplikację:**
    * **Backend (zbieranie danych):**
      ```bash
      python main.py
      ```
      > 💡 **Wskazówka:** Skrypt działa w pętli nieskończonej (zbiera dane co godzinę). Aby bezpiecznie przerwać jego działanie, wciśnij w terminalu skrót **`Ctrl + C`**.

    * **Frontend (dashboard):**
      Uruchom w nowym oknie terminala:
      ```bash
      streamlit run dashboard.py
      ```
      *(Dashboard otworzy się automatycznie w Twojej przeglądarce).*

## 📂 Struktura Projektu

* `main.py` - Skrypt backendowy (ETL), pobiera dane co godzinę.
* `dashboard.py` - Aplikacja Streamlit wizualizująca dane.
* `krakow_dzielnice_master.geojson` - Plik z granicami dzielnic.
* `requirements.txt` - Lista wymaganych bibliotek.

---
*Projekt stworzony w celach edukacyjnych.*
