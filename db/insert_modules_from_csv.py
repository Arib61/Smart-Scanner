import sqlite3
import pandas as pd

# === Lire le fichier CSV avec pandas
df = pd.read_csv("Modules_GINF2.csv", encoding="utf-8")

# === Renommer proprement la colonne
df = df.rename(columns={"Module GINF2": "nom_module"})[["nom_module"]]

# === Connexion à la bonne base
conn = sqlite3.connect("scannerSYS.db")
cursor = conn.cursor()

# === ID du niveau GINF2
id_niveau = 14

# === Insertion ligne par ligne dans la table module
for module in df["nom_module"]:
    nom_module = module.strip()
    if nom_module:
        cursor.execute(
            "INSERT INTO module (nom_module, id_niveau) VALUES (?, ?)",
            (nom_module, id_niveau)
        )
        print(f"✅ Module inséré : {nom_module}")

conn.commit()
conn.close()

print("✅ Tous les modules ont été insérés dans la table 'module' de scannerSYS.db")
