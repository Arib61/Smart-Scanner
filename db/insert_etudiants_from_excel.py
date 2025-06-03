import sqlite3
import pandas as pd

# === Charger le fichier Excel
excel_path = "Students_GINF2.xlsx"
df = pd.read_excel(excel_path)

# === ID du niveau GINF2
id_niveau = 14

# === Vérifie les noms de colonnes du fichier
print("Colonnes trouvées dans Excel :", df.columns)

# === Renommer les colonnes pour correspondre à la base
df = df.rename(columns={
    "code_apogée": "code_apoge",
    "Nom": "nom",
    "Prénom": "prenom"
})[["code_apoge", "nom", "prenom"]]

# === Ajouter la colonne id_niveau manuellement
df["id_niveau"] = id_niveau

# === Connexion à la base SQLite
conn = sqlite3.connect("scannerSYS.db")

# === Insertion dans la table
df.to_sql("etudiant", conn, if_exists="append", index=False)

conn.close()
print("✅ Étudiants insérés avec succès dans la base.")
