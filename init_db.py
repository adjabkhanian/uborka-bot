import sqlite3

conn = sqlite3.connect("cleaning.db")
cursor = conn.cursor()

# Группы
cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    pcs TEXT NOT NULL
)
""")

# Текущий прогресс
cursor.execute("""
CREATE TABLE IF NOT EXISTS state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    next_group_id INTEGER NOT NULL
)
""")

# Расписание (кто когда убирает)
cursor.execute("""
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    completed_by TEXT
)
""")

# Начальное состояние
cursor.execute("INSERT OR IGNORE INTO state (id, next_group_id) VALUES (1, 1)")

conn.commit()
conn.close()
print("✅ DB создана")