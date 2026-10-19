from flask import Flask, request, jsonify
import psycopg2  # lub inny moduł do bazy, którego używasz

app = Flask(__name__)

# Konfiguracja połączenia z bazą PostgreSQL (dostosuj do siebie)
DB_CONFIG = {
    "dbname": "homelab",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

def save_to_db(temp, humidity):
    """Funkcja zapisująca odczyty do bazy PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Przykład zapytania INSERT (dostosuj nazwę tabeli i kolumn do swojej struktury z Tablespace)
        query = "INSERT INTO measurements (temperatura, wilgotnosc) VALUES (%s, %s);"
        cur.execute(query, (temp, humidity))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Zapisano pomyślnie: Temp={temp}°C, Wilgotność={humidity}%")
    except Exception as e:
        print(f"[DB ERROR] Błąd podczas zapisu do bazy: {e}")
        raise e


@app.route('/webhook/shelly', methods=['GET', 'POST'])
def shelly_webhook():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form.to_dict()
    else:
        data = request.args.to_dict()
        
    print(f"[WEBHOOK] Otrzymano żądanie ({request.method})! Dane: {data}")
    
    try:
        # Wyciągamy wartości
        temp = data.get("temp")
        humidity = data.get("hum") or data.get("humidity")
        
        # Filtrujemy - sprawdzamy, czy cokolwiek przyszło i czy nie jest pustym napisem ''
        has_temp = temp is not None and str(temp).strip() != ''
        has_hum = humidity is not None and str(humidity).strip() != ''

        if has_temp or has_hum:
            print(f"[OK] Odebrano poprawne dane -> Temp: {temp}, Wilgotność: {humidity}")
            
            # W tym miejscu wywołamy zapis do bazy PostgreSQL:
            # save_to_db(temp, humidity)
            
            return jsonify({"status": "success"}), 200
        else:
            print("[WARN] Parametry są puste lub ich brakuje w nadesłanym żądaniu:", data)
            return jsonify({"status": "error", "message": "Puste dane"}), 400

    except Exception as e:
        print(f"[ERROR] Wyjątek w endpointcie: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Uruchomienie serwera na wszystkich interfejsach, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)