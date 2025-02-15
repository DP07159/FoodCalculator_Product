from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "food_calculator.db"

# Funktion zum Initialisieren der Datenbank (wird beim Start aufgerufen)
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Rezepte-Tabelle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                calories INTEGER NOT NULL,
                breakfast INTEGER NOT NULL,
                lunch INTEGER NOT NULL,
                dinner INTEGER NOT NULL,
                snack INTEGER NOT NULL
            )
        ''')

        # Wochenpläne-Tabelle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                monday TEXT,
                tuesday TEXT,
                wednesday TEXT,
                thursday TEXT,
                friday TEXT,
                saturday TEXT,
                sunday TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Datenbank wurde erstellt!")

# Datenbank beim Start initialisieren
init_db()

# Route für den Test
@app.route('/')
def index():
    return "✅ Food Calculator Backend läuft mit SQLite!"

# Route zum Abrufen der Rezepte
@app.route('/get_recipes', methods=['GET'])
def get_recipes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, calories, breakfast, lunch, dinner, snack FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
