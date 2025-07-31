import sqlite3

conn = sqlite3.connect('biat.db')
cur = conn.cursor()

# Create tables
cur.executescript("""
CREATE TABLE IF NOT EXISTS poles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pole_id INTEGER NOT NULL,
    FOREIGN KEY (pole_id) REFERENCES poles(id)
);

CREATE TABLE IF NOT EXISTS branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS systems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id INTEGER NOT NULL,
    system_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(id),
    FOREIGN KEY (system_id) REFERENCES systems(id),
    UNIQUE(branch_id, system_id, name)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    pole_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (pole_id) REFERENCES poles(id)
);

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    objet_demande TEXT NOT NULL,
    date_demande DATE NOT NULL,
    department_id INTEGER NOT NULL,
    pole_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (pole_id) REFERENCES poles(id)
);

CREATE TABLE IF NOT EXISTS request_branches (
    request_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    PRIMARY KEY (request_id, branch_id),
    FOREIGN KEY (request_id) REFERENCES requests(id),
    FOREIGN KEY (branch_id) REFERENCES branches(id)
);

CREATE TABLE IF NOT EXISTS request_system_profiles (
    request_id INTEGER NOT NULL,
    system_id INTEGER NOT NULL,
    profile_id INTEGER NOT NULL,
    environment TEXT NOT NULL CHECK(environment IN ('TEST', 'PROD')),
    PRIMARY KEY (request_id, system_id, profile_id, environment),
    FOREIGN KEY (request_id) REFERENCES requests(id),
    FOREIGN KEY (system_id) REFERENCES systems(id),
    FOREIGN KEY (profile_id) REFERENCES profiles(id)
);
""")

conn.commit()
conn.close()

print("Database and tables created!")
