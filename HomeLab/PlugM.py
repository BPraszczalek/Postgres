from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Konfiguracja połączenia z Twoją bazą danych 'homelab'
DB_CONFIG = {
    "dbname": "homelab",
    "user": "postgres",     # Podmień na swój login
    "password": "123",     # Podmień na swoje hasło
    "host": "localhost",
    "port": "5432"
}

def save_plug_to_db(moc, napiecie, natezenie):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')  # <--- Dodaj tę linijkę, aby wymusić poprawne kodowanie
        cursor = conn.cursor()
        
        query = """
            INSERT INTO shellyp (moc, napiecie, natezenie) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (moc, napiecie, natezenie))
        conn.commit()
        print(f"[DB] Zapisano pomiar -> Moc: {moc}W, Napięcie: {napiecie}V, Natężenie: {natezenie}A")
        
    except Exception as e:
        print(f"[DB ERROR] Błąd zapisu do bazy: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/webhook/plug', methods=['GET', 'POST'])
def plug_webhook():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form.to_dict()
    else:
        data = request.args.to_dict()
        
    print(f"[PLUG WEBHOOK] Otrzymano dane: {data}")
    
    try:
        power = data.get("power")
        voltage = data.get("voltage")
        current = data.get("current")
        
        # Bezpieczna konwersja (obsługa napisu 'null' i pustych wartości)
        def safe_float(val):
            if val is None:
                return None
            val_str = str(val).strip().lower()
            if val_str in ['', 'none', 'null']:
                return None
            try:
                return float(val)
            except ValueError:
                return None

        moc_val = safe_float(power)
        napiecie_val = safe_float(voltage)
        natezenie_val = safe_float(current)

        # Wywołanie zapisu z dokładnie 3 argumentami
        save_plug_to_db(moc_val, napiecie_val, natezenie_val)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"[ERROR] Błąd przetwarzania żądania: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)