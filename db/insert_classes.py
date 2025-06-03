import sqlite3

# Connexion à la base
conn = sqlite3.connect("scannerSYS.db")
cursor = conn.cursor()

# Liste des classes à insérer
classes = ["AMPHI1", "AMPHI2", "B19", "B20", "B21", "B22", "C6", "C5"]

# Insertion dans la table
for nom_classe in classes:
    try:
        cursor.execute("INSERT INTO classe (nom_classe) VALUES (?)", (nom_classe,))
        print(f"✅ Classe insérée : {nom_classe}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Classe déjà existante (ignorée) : {nom_classe}")

conn.commit()
conn.close()

print("✅ Toutes les classes ont été insérées dans la table 'classe'.")
