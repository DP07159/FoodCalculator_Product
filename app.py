from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "food_calculator.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Tabelle für Rezepte
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

        # Tabelle für Wochenpläne
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

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recipes', methods=['GET'])
def get_recipes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, calories, breakfast, lunch, dinner, snack FROM recipes")
    recipes = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": r[0], "name": r[1], "calories": r[2], "breakfast": bool(r[3]), "lunch": bool(r[4]), "dinner": bool(r[5]), "snack": bool(r[6])}
        for r in recipes
    ])

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipes (name, calories, breakfast, lunch, dinner, snack) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data["name"], data["calories"], data["breakfast"], data["lunch"], data["dinner"], data["snack"]))
    conn.commit()
    conn.close()

    return jsonify({"message": "Rezept erfolgreich hinzugefügt!"}), 201

@app.route('/delete_recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Rezept erfolgreich gelöscht!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

# Wochenplan speichern
@app.route('/save_weekly_plan', methods=['POST'])
def save_weekly_plan():
    data = request.get_json()

    required_fields = ["name", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weekly_plans (name, monday, tuesday, wednesday, thursday, friday, saturday, sunday) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data["name"], data["monday"], data["tuesday"], data["wednesday"], data["thursday"], 
          data["friday"], data["saturday"], data["sunday"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Wochenplan erfolgreich gespeichert!"}), 201

# Gespeicherte Wochenpläne abrufen
@app.route('/get_weekly_plans', methods=['GET'])
def get_weekly_plans():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM weekly_plans")
    plans = cursor.fetchall()
    conn.close()

    return jsonify([{"id": p[0], "name": p[1]} for p in plans])

# Einen Wochenplan laden
@app.route('/load_weekly_plan/<int:plan_id>', methods=['GET'])
def load_weekly_plan(plan_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weekly_plans WHERE id = ?", (plan_id,))
    plan = cursor.fetchone()
    conn.close()

    if plan:
        return jsonify({
            "id": plan[0],
            "name": plan[1],
            "monday": plan[2],
            "tuesday": plan[3],
            "wednesday": plan[4],
            "thursday": plan[5],
            "friday": plan[6],
            "saturday": plan[7],
            "sunday": plan[8]
        })
    else:
        return jsonify({"error": "Wochenplan nicht gefunden"}), 404
