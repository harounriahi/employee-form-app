import sqlite3

conn = sqlite3.connect('biat.db')
cur = conn.cursor()

# Pôles
cur.execute("INSERT OR IGNORE INTO poles (name) VALUES (?)", ('Back Office',))
cur.execute("INSERT OR IGNORE INTO poles (name) VALUES (?)", ('Front Office',))

# Départements (en supposant pole_id = 1 pour les deux)
cur.execute("INSERT OR IGNORE INTO departments (name, pole_id) VALUES (?, ?)", ("Systèmes d'information", 1))
cur.execute("INSERT OR IGNORE INTO departments (name, pole_id) VALUES (?, ?)", ('Recouvrement', 1))

# Branches
branches = ['AUTO', 'IARDS', 'Transport', 'Santé', 'Epargne', 'Prévoyance', 'Comptabilité', 'Recouvrement', 'RH']
for b in branches:
    cur.execute("INSERT OR IGNORE INTO branches (name) VALUES (?)", (b,))

# Systèmes
systems = ['ARIMA', 'AGORA', 'ESPASS', 'SAGE']
for s in systems:
    cur.execute("INSERT OR IGNORE INTO systems (name) VALUES (?)", (s,))

# Profils (exemple avec AUTO + ARIMA)
cur.execute("SELECT id FROM branches WHERE name = 'AUTO'")
branch_auto = cur.fetchone()
cur.execute("SELECT id FROM systems WHERE name = 'ARIMA'")
system_arima = cur.fetchone()

if branch_auto and system_arima:
    branch_auto_id = branch_auto[0]
    system_arima_id = system_arima[0]

    profils_auto_arima = ['Gestionnaire AUTO Niveau 1', 'Gestionnaire AUTO Niveau 2']
    for profil in profils_auto_arima:
        cur.execute("""
            INSERT OR IGNORE INTO profiles (branch_id, system_id, name) VALUES (?, ?, ?)
        """, (branch_auto_id, system_arima_id, profil))

conn.commit()
conn.close()
print("Données de référence insérées.")
