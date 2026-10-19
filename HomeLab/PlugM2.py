from flask import Flask, jsonify
import psycopg2
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Konfiguracja bazy danych 'homelab'
DB_CONFIG = {
    "dbname": "homelab",
    "user": "postgres",     # Podmień na swój login
    "password": "123",     # Podmień na swoje hasło
    "host": "localhost",
    "port": "5432"
}

# Adres IP Twojego gniazdka Shelly w sieci lokalnej
SHELLY_IP = "192.168.1.23"  # Twoje IP z logów

def save_plug_to_db(moc, napiecie, natezenie):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        cursor = conn.cursor()
        
        query = """
            INSERT INTO shellyp (moc, napiecie, natezenie) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (moc, napiecie, natezenie))
        conn.commit()
        print(f"[DB] Zapisano pomiar -> Moc: {moc}W, Napięcie: {napiecie}V, Natężenie: {natezenie}A")
        
    except Exception as e:
        err_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8')
        print(f"[DB ERROR] Błąd zapisu do bazy: {err_msg}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

# Funkcja uruchamiana automatycznie co określoną liczbę sekund
def fetch_shelly_data():
    try:
        url = f"http://192.168.1.23/rpc/Switch.GetStatus?id=0"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Shelly zwraca pełny zestaw danych
            moc = data.get("apower")       # Moc czynna
            napiecie = data.get("voltage") # Napięcie
            natezenie = data.get("current")# Prąd
            
            print(f"[SHELLY POLL] Pobrano z urządzenia -> Moc: {moc}W, Napięcie: {napiecie}V, Natężenie: {natezenie}A")
            
            # Zapisujemy do bazy danych
            save_plug_to_db(moc, napiecie, natezenie)
        else:
            print(f"[SHELLY ERROR] Błąd HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"[SHELLY ERROR] Nie powiodło się połączenie z gniazdkiem: {e}")

if __name__ == '__main__':
    # Konfiguracja harmonogramu: pobieraj dane co 60 sekund
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_shelly_data, trigger="interval", seconds=60)
    scheduler.start()
    
    try:
        # Uruchomienie serwera Flask
        app.run(host='0.0.0.0', port=5000, use_reloader=False)
    finally:
        scheduler.shutdown()