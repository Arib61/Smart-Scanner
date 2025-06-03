import sqlite3
import os
import traceback

# === Chemin vers la base
db_path = "scannerSYS.db"

# === SUPPRIMER la base existante
if os.path.exists(db_path):
    os.remove(db_path)
    print("🗑️ Ancienne base supprimée.")
else:
    print("ℹ️ Aucune base existante à supprimer.")

# === Connexion (nouvelle base vide)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# === 1. Table des classes
cursor.execute("""
CREATE TABLE IF NOT EXISTS classe (
    id_classe INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_classe TEXT NOT NULL UNIQUE
);
""")

# === 2. Table des niveaux
cursor.execute("""
CREATE TABLE IF NOT EXISTS niveau (
    id_niveau INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_niveau TEXT NOT NULL UNIQUE
);
""")

# === 3. Table des étudiants
cursor.execute("""
CREATE TABLE IF NOT EXISTS etudiant (
    code_apoge TEXT PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    id_niveau INTEGER NOT NULL,
    FOREIGN KEY (id_niveau) REFERENCES niveau(id_niveau)
);
""")

# === 4. Table des modules
cursor.execute("""
CREATE TABLE IF NOT EXISTS module (
    id_module INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_module TEXT NOT NULL
);
""")

# === 5. Table des présences
cursor.execute("""
CREATE TABLE IF NOT EXISTS presence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_apoge TEXT NOT NULL,
    date TEXT NOT NULL,
    id_module INTEGER,
    id_niveau INTEGER NOT NULL,
    nbr_present INTEGER NOT NULL,

    FOREIGN KEY (code_apoge) REFERENCES etudiant(code_apoge),
    FOREIGN KEY (id_module) REFERENCES module(id_module),
    FOREIGN KEY (id_niveau) REFERENCES niveau(id_niveau)
);
""")

conn.commit()
conn.close()

print("✅ Nouvelle base 'scanner1.db' créée avec succès avec la structure corrigée.")
