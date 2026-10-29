from flask import Flask, jsonify
import psycopg2
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import config

app = Flask(__name__)
def save_plug_to_db(moc, napiecie, natezenie):
    try:
        conn = psycopg2.connect(**config.DB_CONFIG)
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
def fetch_shelly_data():
    try:
        response = requests.get(config.SHELLY_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            moc = data.get("apower")       
            napiecie = data.get("voltage") 
            natezenie = data.get("current")
            
            print(f"[SHELLY POLL] Pobrano z urządzenia -> Moc: {moc}W, Napięcie: {napiecie}V, Natężenie: {natezenie}A")
            save_plug_to_db(moc, napiecie, natezenie)
        else:
            print(f"[SHELLY ERROR] Błąd HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"[SHELLY ERROR] Nie powiodło się połączenie z gniazdkiem: {e}")

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_shelly_data, trigger="interval", seconds=5)
    scheduler.start()
    try:
        app.run(host='0.0.0.0', port=5000, use_reloader=False)
    finally:
        scheduler.shutdown()