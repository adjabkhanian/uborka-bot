import sqlite3

groups = [
    ("Группа 1", "1,2,3,4,5"),
    ("Группа 2", "6,7,8,9,10"),
    ("Группа 3", "11,12,13,14,15"),
    ("Группа 4", "16,17,18,19,20"),
    ("Группа 5", "21,22,23,24,25"),
    ("Группа 6", "26,27,28,29,PS1"),
    ("Группа 7", "30,31,32,33,34"),
    ("Группа 8", "35,36,37,38,PS2")
]

conn = sqlite3.connect("cleaning.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM groups")

for i, (name, pcs) in enumerate(groups, start=1):
    cursor.execute("INSERT INTO groups (id, name, pcs) VALUES (?, ?, ?)", (i, name, pcs))

conn.commit()
conn.close()
print("✅ Группы загружены")