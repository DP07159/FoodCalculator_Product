from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Route für die Startseite
@app.route('/')
def index():
    return "Food Calculator Backend läuft!"

# Route zum Abrufen der Rezepte
@app.route('/get_recipes', methods=['GET'])
def get_recipes():
    conn = sqlite3.connect("food_calculator.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, calories, breakfast, lunch, dinner, snack FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
