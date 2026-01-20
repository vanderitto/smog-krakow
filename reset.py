import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DB_PASS = os.getenv("DB_PASSWORD")
db_url = f'postgresql://myuser:{DB_PASS}@localhost:5432/weather_db'
engine = create_engine(db_url)

with engine.connect() as conn:
    # To polecenie niszczy tabelę razem z danymi
    conn.execute(text("DROP TABLE IF EXISTS smog_polska"))
    conn.commit()
    print("✅ Tabela 'smog_polska' została usunięta. Jest czysto!")