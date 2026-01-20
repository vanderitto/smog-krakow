# 🐲 Kraków Smog Monitor

An interactive application monitoring air quality across 18 districts of Kraków in real-time. The project combines data fetching from an external API, storage in a PostgreSQL database, and visualization on an interactive map.

## 📸 Preview

<p align="center">
  <img src="https://github.com/user-attachments/assets/bcc77927-8fe2-4fb2-b2c4-a837a118dc86" alt="Dashboard View" width="100%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/fed90dc8-8d46-4ad7-a281-deb59706f428" alt="Map Detail" width="48%">
</p>

## 🚀 Features

* **Real-time Data:** Automatic fetching of air quality data (AQI) for each of Kraków's 18 districts (WAQI API).
* **Data Engineering:** ETL process (Extract, Transform, Load) saving historical data to a PostgreSQL database.
* **Geospatial Visualization:** Interactive map of Kraków with precise division into official district boundaries (GeoJSON) and color-coded air status.
* **Interactive Dashboard:** Ability to select a district from the table, automatically highlighting it on the map (Fuzzy Matching of names).
* **Dockerized Database:** Database running in a secure Docker container.

## 🛠️ Technologies

* **Python 3.11+**
* **Streamlit** (Frontend & Dashboard)
* **Folium & GeoJSON** (Maps)
* **PostgreSQL** (Database)
* **Docker** (Containerization)
* **SQLAlchemy & Pandas** (Data Handling)

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    *(Replace `YOUR_USERNAME` with your GitHub username)*
    ```bash
    git clone [https://github.com/YOUR_USERNAME/smog-krakow.git](https://github.com/YOUR_USERNAME/smog-krakow.git)
    cd smog-krakow
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the main directory and add your keys:
    ```text
    WAQI_TOKEN=your_token_from_aqicn_org
    DB_PASSWORD=your_database_password
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the database (Docker):**
    *(Ensure you have the Postgres database running in Docker according to the configuration)*

5.  **Run the application:**
    * **Backend (data collection):**
        ```bash
        python main.py
        ```
        > 💡 **Tip:** The script runs in an infinite loop (collects data every hour). To safely stop it, press **`Ctrl + C`** in the terminal.

    * **Frontend (dashboard):**
        Run in a new terminal window:
        ```bash
        streamlit run dashboard.py
        ```
        *(The dashboard will open automatically in your browser).*

## 📂 Project Structure

* `main.py` - Backend script (ETL), fetches data every hour and saves it to the database.
* `dashboard.py` - Streamlit application visualizing data on the map.
* `*.geojson` - Set of 18 files with precise boundaries of Kraków districts.
* `requirements.txt` - List of required libraries.

---
*Project created for educational purposes.*
