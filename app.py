from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "food_calculator.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
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
