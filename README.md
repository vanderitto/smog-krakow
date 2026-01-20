# 🐲 Kraków Smog Monitor

Interaktywna aplikacja monitorująca jakość powietrza w 18 dzielnicach Krakowa w czasie rzeczywistym. Projekt łączy pobieranie danych z zewnętrznego API, składowanie ich w bazie PostgreSQL oraz wizualizację na interaktywnej mapie.

## 📸 Podgląd

<p align="center">
  <img src="https://github.com/user-attachments/assets/bcc77927-8fe2-4fb2-b2c4-a837a118dc86" alt="Dashboard View" width="100%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/fed90dc8-8d46-4ad7-a281-deb59706f428" alt="Map Detail" width="48%">
</p>

## 🚀 Funkcjonalności

* **Real-time Data:** Automatyczne pobieranie danych o jakości powietrza (AQI) dla każdej z 18 dzielnic Krakowa (API WAQI).
* **Data Engineering:** Proces ETL (Extract, Transform, Load) zapisujący dane historyczne do bazy PostgreSQL.
* **Geospatial Visualization:** Interaktywna mapa Krakowa z precyzyjnym podziałem na oficjalne granice dzielnic (GeoJSON) i kolorystycznym oznaczeniem stanu powietrza.
* **Interactive Dashboard:** Możliwość wyboru dzielnicy z tabeli, co automatycznie podświetla ją na mapie (Fuzzy Matching nazw).
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
    *(Podmień `TWOJA_NAZWA` na swój nick z GitHuba)*
    ```bash
    git clone [https://github.com/TWOJA_NAZWA/smog-krakow.git](https://github.com/TWOJA_NAZWA/smog-krakow.git)
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
    *(Upewnij się, że masz uruchomioną bazę Postgres w Dockerze zgodnie z konfiguracją)*

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

* `main.py` - Skrypt backendowy (ETL), pobiera dane co godzinę i zapisuje do bazy.
* `dashboard.py` - Aplikacja Streamlit wizualizująca dane na mapie.
* `*.geojson` - Zestaw 18 plików z precyzyjnymi granicami dzielnic Krakowa.
* `requirements.txt` - Lista wymaganych bibliotek.

---
*Projekt stworzony w celach edukacyjnych.*
