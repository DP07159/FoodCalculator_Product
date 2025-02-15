import sqlite3

conn = sqlite3.connect("food_calculator.db")
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

print("Datenbank wurde initialisiert!")
