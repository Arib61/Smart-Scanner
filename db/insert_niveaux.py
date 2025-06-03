import sqlite3

conn = sqlite3.connect("scannerSYS.db")
cursor = conn.cursor()

# === Supprimer l'ancienne table module
cursor.execute("DROP TABLE IF EXISTS module")

# === Recréer la table module avec id_niveau
cursor.execute("""
CREATE TABLE IF NOT EXISTS module (
    id_module INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_module TEXT NOT NULL,
    id_niveau INTEGER NOT NULL,
    FOREIGN KEY (id_niveau) REFERENCES niveau(id_niveau)
);
""")

conn.commit()
conn.close()

print("✅ Table 'module' recréée avec l'attribut 'id_niveau'.")
