from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
import string
import random
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json

# === CONFIG ===
DATABASE = "biat.db"

app = Flask(__name__)
app.secret_key = 'une_clef_secrete_pour_la_session'
app.permanent_session_lifetime = timedelta(minutes=30)

# === UTILITIES ===
def generate_request_pdf(data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, y, "Fiche d'accès - BIAT Assurance")
    y -= 30

    p.setFont("Helvetica", 12)
    for key, value in data.items():
        p.drawString(40, y, f"{key}:")
        y -= 20
        # Support multi-line values, e.g. system info
        if isinstance(value, str) and '\n' in value:
            for line in value.split('\n'):
                p.drawString(60, y, line)
                y -= 15
        else:
            p.drawString(60, y, str(value))
            y -= 15
        y -= 5

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def send_password_email(to_email, password):
    print(f"[DEBUG] Sending email to {to_email} with password: {password}")

    msg = EmailMessage()
    msg['Subject'] = 'Votre mot de passe - ABIAT'
    msg['From'] = 'haroun.riiahii@gmail.com'  # Change with your email
    msg['To'] = to_email
    msg.set_content(f'''Bonjour,

Vous venez de créer un compte. Voici votre mot de passe pour accéder à la plateforme ABIAT :

{password}

Merci.
''')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('haroun.riiahii@gmail.com', 'hukreegcgmihoybi')  # Use your Gmail app password here!
            smtp.send_message(msg)
            print("[DEBUG] Email sent successfully to", to_email)
    except Exception as e:
        print("[ERROR] Email sending error:", e)

# === DATABASE INIT ===
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executescript("""
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
            department_id INTEGER,
            pole_id INTEGER,
            password TEXT NOT NULL,
            role TEXT,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (pole_id) REFERENCES poles(id)
        );
        CREATE TABLE IF NOT EXISTS collaborator_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            objet_demande TEXT NOT NULL,
            date_demande DATE NOT NULL,
            collaborator_type_id INTEGER,
            date_debut_stage DATE,
            date_fin_stage DATE,
            acces_partages TEXT,
            signature TEXT,
            status TEXT,
            responsable_id INTEGER,
            rejection_comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (collaborator_type_id) REFERENCES collaborator_types(id)
        );
        CREATE TABLE IF NOT EXISTS branches_requests (
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
        CREATE TABLE IF NOT EXISTS network_accesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS request_network_accesses (
            request_id INTEGER NOT NULL,
            network_access_id INTEGER NOT NULL,
            PRIMARY KEY (request_id, network_access_id),
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (network_access_id) REFERENCES network_accesses(id)
        );
        CREATE TABLE IF NOT EXISTS request_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            actor_id INTEGER,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (actor_id) REFERENCES users(id)
        );
        """)
        conn.commit()

init_db()

# === ROUTES ===

@app.route('/register', methods=['GET', 'POST'])
def register():
    # --- TEMP: Commented out role restriction so anyone can register for testing ---
    # if 'user' not in session:
    #     return redirect(url_for('login'))

    # with sqlite3.connect(DATABASE) as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT role FROM users WHERE email = ?", (session['user'],))
    #     row = cursor.fetchone()
    #     if not row or row[0] != "informatique":
    #         flash("Seuls les informaticiens peuvent créer des comptes.", "danger")
    #         return redirect(url_for('dashboard'))
    # --- END TEMP ---

    if request.method == 'POST':
        nom = request.form['nom'].strip()
        prenom = request.form['prenom'].strip()
        email = request.form['email'].strip().lower()
        departement = request.form['departement'].strip()
        pole = request.form['pole'].strip()
        role = request.form.get('role')

        # Validate role
        if role not in ["responsable", "validateur", "informatique"]:
            flash("Rôle invalide.", "danger")
            return redirect(url_for('register'))

        password = generate_password()
        hashed_password = generate_password_hash(password)

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Get or create pole
            cursor.execute("SELECT id FROM poles WHERE name = ?", (pole,))
            pole_row = cursor.fetchone()
            if not pole_row:
                cursor.execute("INSERT INTO poles (name) VALUES (?)", (pole,))
                pole_id = cursor.lastrowid
            else:
                pole_id = pole_row[0]
            # Get or create department
            cursor.execute("SELECT id FROM departments WHERE name = ? AND pole_id = ?", (departement, pole_id))
            dep_row = cursor.fetchone()
            if not dep_row:
                cursor.execute("INSERT INTO departments (name, pole_id) VALUES (?, ?)", (departement, pole_id))
                department_id = cursor.lastrowid
            else:
                department_id = dep_row[0]

            try:
                cursor.execute('''
                    INSERT INTO users (nom, prenom, email, department_id, pole_id, password, role)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (nom, prenom, email, department_id, pole_id, hashed_password, role))
                conn.commit()
                send_password_email(email, password)
                flash("Compte créé. Un mot de passe a été envoyé par email.", "success")
                return redirect(url_for('dashboard'))
            except sqlite3.IntegrityError:
                flash("Un utilisateur avec cet email existe déjà.", "danger")
                return redirect(url_for('register'))
            except Exception as e:
                print("[REGISTER ERROR]", e)
                flash("Erreur serveur lors de la création du compte.", "danger")
                return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password, role, nom, prenom FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
        if row and check_password_hash(row[0], password):
            session.permanent = True
            session['user'] = email
            session['role'] = row[1]
            session['user_name'] = f"{row[2]} {row[3]}"
            flash("Connexion réussie.", "success")
            # Always redirect to the form after login
            return redirect(url_for('form'))
        else:
            flash("Email ou mot de passe incorrect.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', role=session.get('role'), user_name=session.get('user_name'))

@app.route('/')
def form():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    nom, prenom = '', ''
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nom, prenom FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            nom, prenom = user

        cursor.execute("SELECT name FROM branches ORDER BY name")
        branches = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT name FROM systems ORDER BY name")
        systems = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT name FROM collaborator_types ORDER BY name")
        collaborator_types = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT name FROM network_accesses ORDER BY name")
        network_accesses = [row[0] for row in cursor.fetchall()]
        cursor.execute("""
            SELECT b.name, s.name, p.name
            FROM profiles p
            JOIN branches b ON p.branch_id = b.id
            JOIN systems s ON p.system_id = s.id
        """)
        profiles = cursor.fetchall()
    profiles_dict = {}
    for branch, system, profile in profiles:
        profiles_dict.setdefault(branch, {}).setdefault(system, []).append(profile)
    demandeur = f"{nom} {prenom}"
    return render_template(
        'form.html',
        demandeur=demandeur,
        branches=branches,
        systems=systems,
        collaborator_types=collaborator_types,
        network_accesses=network_accesses,
        profiles_dict=profiles_dict
    )
@app.route('/demande/<int:request_id>/view')
def view_demande(request_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch the main request row
    row = cursor.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
    if not row:
        flash("Demande introuvable.", "danger")
        conn.close()
        return redirect(url_for('mes_demandes'))

    demande = {
        "id": row[0],
        "user_id": row[1],
        "objet_demande": row[2],
        "date_demande": row[3],
        "collaborator_type_id": row[4],
        "date_debut_stage": row[5],
        "date_fin_stage": row[6],
        "acces_partages": row[7] or "",
        "signature": row[8],
        "status": row[9],
        "responsable_id": row[10],
        "rejection_comment": row[11],
    }

    # Fetch demandeur info
    cursor.execute("SELECT nom, prenom, email FROM users WHERE id = ?", (demande["user_id"],))
    user_row = cursor.fetchone()
    if user_row:
        demande["nom_complet"] = f"{user_row[0]} {user_row[1]}"
        demande["demandeur"] = demande["nom_complet"]
        demande["email"] = user_row[2]
    else:
        demande["nom_complet"] = ""
        demande["demandeur"] = ""
        demande["email"] = ""

    # Fetch department and pole
    cursor.execute("""
        SELECT d.name, p.name
        FROM users u
        LEFT JOIN departments d ON u.department_id = d.id
        LEFT JOIN poles p ON u.pole_id = p.id
        WHERE u.id = ?
    """, (demande["user_id"],))
    dep_pole = cursor.fetchone()
    demande["departement"] = dep_pole[0] if dep_pole else ""
    demande["pole"] = dep_pole[1] if dep_pole else ""

    # Collaborator type
    cursor.execute("SELECT name FROM collaborator_types WHERE id = ?", (demande["collaborator_type_id"],))
    ct = cursor.fetchone()
    demande["collaborator_type"] = ct[0] if ct else ""

    # Matricule (if you have it in your users table; otherwise leave blank)
    demande["matricule"] = ""

    # Branches for this request
    cursor.execute("""
        SELECT b.name FROM branches_requests br
        JOIN branches b ON br.branch_id = b.id
        WHERE br.request_id = ?
    """, (request_id,))
    demande["branches"] = [r[0] for r in cursor.fetchall()]

    # All branches for display
    cursor.execute("SELECT name FROM branches ORDER BY name")
    all_branches = [row[0] for row in cursor.fetchall()]

    # Network accesses for this request
    cursor.execute("""
        SELECT na.name
        FROM request_network_accesses rna
        JOIN network_accesses na ON rna.network_access_id = na.id
        WHERE rna.request_id = ?
    """, (request_id,))
    demande["network_access"] = [r[0] for r in cursor.fetchall()]

    # All network accesses for display
    cursor.execute("SELECT name FROM network_accesses ORDER BY name")
    all_network_accesses = [row[0] for row in cursor.fetchall()]

    # Profils_env: {branch: {profile: [envs]}}
    cursor.execute("""
        SELECT b.name, s.name, p.name, rsp.environment
        FROM request_system_profiles rsp
        JOIN profiles p ON rsp.profile_id = p.id
        JOIN systems s ON rsp.system_id = s.id
        JOIN branches b ON p.branch_id = b.id
        WHERE rsp.request_id = ?
    """, (request_id,))
    profils_env = {}
    for branch, system, profile, env in cursor.fetchall():
        # Group by branch and system/profile
        profils_env.setdefault(branch, {}).setdefault(f"{system} - {profile}", []).append(env)
    demande["profils_env"] = profils_env

    # Make sure all expected fields exist
    for key in [
        "objet_demande", "date_demande", "demandeur", "departement", "pole", "collaborator_type",
        "date_debut_stage", "date_fin_stage", "nom_complet", "matricule", "email",
        "branches", "profils_env", "network_access", "acces_partages"
    ]:
        if key not in demande:
            if key in ["branches", "network_access"]:
                demande[key] = []
            elif key == "profils_env":
                demande[key] = {}
            else:
                demande[key] = ""

    conn.close()
    return render_template(
        'view_demande.html',
        demande=demande,
        all_branches=all_branches,
        all_network_accesses=all_network_accesses
    )

@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # 1. Get the user ID
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
        user_row = cursor.fetchone()
        if not user_row:
            flash("Utilisateur non trouvé.", "danger")
            return redirect(url_for('form'))
        user_id = user_row[0]

        # 2. Get form fields
        objet_demande = request.form.get('objet_demande')
        if not objet_demande:
            flash("Veuillez sélectionner l'objet de la demande.", "danger")
            return redirect(url_for('form'))

        date_demande = request.form.get('date_demande') or datetime.now().strftime('%Y-%m-%d')
        collaborator_type = request.form.get('collaborator_type')
        date_debut_stage = request.form.get('date_debut_stage') or None
        date_fin_stage = request.form.get('date_fin_stage') or None
        signature = request.form.get('signature') or None
        acces_partages = request.form.get('acces_partages') or None

        # 3. Get collaborator_type_id
        cursor.execute("SELECT id FROM collaborator_types WHERE name = ?", (collaborator_type,))
        collab_type_row = cursor.fetchone()
        if not collab_type_row and collaborator_type:
            cursor.execute("INSERT INTO collaborator_types (name) VALUES (?)", (collaborator_type,))
            collaborator_type_id = cursor.lastrowid
        elif collab_type_row:
            collaborator_type_id = collab_type_row[0]
        else:
            collaborator_type_id = None

        # 4. Insert request (status/responsable will be set after)
        cursor.execute("""
            INSERT INTO requests (
                user_id, objet_demande, date_demande, collaborator_type_id,
                date_debut_stage, date_fin_stage, acces_partages, signature
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, objet_demande, date_demande, collaborator_type_id, date_debut_stage, date_fin_stage, acces_partages, signature))
        request_id = cursor.lastrowid

        # 5. Branches
        branches = request.form.getlist('branches[]')
        for branch_name in branches:
            cursor.execute("SELECT id FROM branches WHERE name = ?", (branch_name,))
            branch_row = cursor.fetchone()
            if branch_row:
                branch_id = branch_row[0]
                cursor.execute("INSERT OR IGNORE INTO branches_requests (request_id, branch_id) VALUES (?, ?)", (request_id, branch_id))

        # 6. Systems/profiles/environments
        for key, env_list in request.form.lists():
            if key.startswith("profils_env["):
                m = re.match(r'profils_env\[(.+?)\]\[(.+?)\]\[(.+?)\]', key)
                if m:
                    branch_name = m.group(1)
                    system_name = m.group(2)
                    profile_name = m.group(3)
                    cursor.execute("SELECT id FROM systems WHERE name = ?", (system_name,))
                    sys_row = cursor.fetchone()
                    if not sys_row:
                        continue
                    system_id = sys_row[0]
                    cursor.execute("SELECT id FROM profiles WHERE name = ? AND system_id = ?", (profile_name, system_id))
                    prof_row = cursor.fetchone()
                    if not prof_row:
                        if profile_name == "Aucun Profil":
                            continue
                        continue
                    profile_id = prof_row[0]
                    for env in env_list:
                        if env in ['TEST', 'PROD']:
                            cursor.execute("""
                                INSERT OR IGNORE INTO request_system_profiles (request_id, system_id, profile_id, environment)
                                VALUES (?, ?, ?, ?)
                            """, (request_id, system_id, profile_id, env))

        # 7. Network accesses
        network_accesses = request.form.getlist('network_access[]')
        for net_acc_name in network_accesses:
            cursor.execute("SELECT id FROM network_accesses WHERE name = ?", (net_acc_name,))
            net_acc_row = cursor.fetchone()
            if not net_acc_row:
                cursor.execute("INSERT INTO network_accesses (name) VALUES (?)", (net_acc_name,))
                net_acc_id = cursor.lastrowid
            else:
                net_acc_id = net_acc_row[0]
            cursor.execute("INSERT OR IGNORE INTO request_network_accesses (request_id, network_access_id) VALUES (?, ?)", (request_id, net_acc_id))

        # 8. Workflow logic: Set status, responsable, history
        cursor.execute("SELECT id FROM users WHERE role='responsable' LIMIT 1")
        resp_row = cursor.fetchone()
        responsable_id = resp_row[0] if resp_row else None

        cursor.execute("UPDATE requests SET status=?, responsable_id=? WHERE id=?", ('soumis', responsable_id, request_id))

        # Add to history
        cursor.execute(
            "INSERT INTO request_history (request_id, action, actor_id) VALUES (?, 'soumis', ?)",
            (request_id, user_id)
        )
        conn.commit()

        # 9. Notify responsable by email
        if responsable_id:
            cursor.execute("SELECT email FROM users WHERE id=?", (responsable_id,))
            responsable_email = cursor.fetchone()[0]
            msg_resp = EmailMessage()
            msg_resp['Subject'] = 'Nouvelle demande à valider'
            msg_resp['From'] = 'haroun.riiahii@gmail.com'
            msg_resp['To'] = responsable_email
            msg_resp.set_content(
                f"Vous avez une nouvelle demande à valider. Rendez-vous sur la page /responsable/requests."
            )
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('haroun.riiahii@gmail.com', 'hukreegcgmihoybi')
                    smtp.send_message(msg_resp)
            except Exception as e:
                print("[ERROR] Email to responsable error:", e)

        # 10. Gather submitted data for PDF
        systeme_info_details = []
        for key, env_list in request.form.lists():
            if key.startswith("profils_env["):
                m = re.match(r'profils_env\[(.+?)\]\[(.+?)\]\[(.+?)\]', key)
                if m:
                    branch_name = m.group(1)
                    system_name = m.group(2)
                    profile_name = m.group(3)
                    envs = ', '.join(env_list)
                    systeme_info_details.append(f"Branche: {branch_name} | Système: {system_name} | Profil: {profile_name} | Environnements: {envs}")

        pdf_data = {
            "Demandeur": session['user'],
            "Objet de la demande": objet_demande,
            "Date de la demande": date_demande,
            "Type de collaborateur": collaborator_type,
            "Département": request.form.get('departement', ''),
            "Pôle": request.form.get('pole', ''),
            "Nom complet": request.form.get('nom_complet', ''),
            "Matricule": request.form.get('matricule', ''),
            "Email": request.form.get('email', ''),
            "Branches": ', '.join(request.form.getlist('branches[]')),
            "Accès partagés": acces_partages if acces_partages else '',
            "Network access": ', '.join(request.form.getlist('network_access[]')),
            "Systèmes d'information demandés": '\n'.join(systeme_info_details)
        }

        # 11. Generate PDF
        pdf_buffer = generate_request_pdf(pdf_data)

        # 12. Email PDF to demandeur
        msg = EmailMessage()
        msg['Subject'] = 'Votre fiche d\'accès BIAT - PDF'
        msg['From'] = 'haroun.riiahii@gmail.com'
        msg['To'] = session['user']
        msg.set_content('Veuillez trouver en pièce jointe votre fiche d\'accès BIAT au format PDF.')

        pdf_bytes = pdf_buffer.getvalue()
        msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename='fiche_acces_biat.pdf')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('haroun.riiahii@gmail.com', 'hukreegcgmihoybi')
                smtp.send_message(msg)
                print("[DEBUG] Fiche PDF envoyée à", session['user'])
        except Exception as e:
            print("[ERROR] Email PDF sending error:", e)

    flash("Demande enregistrée avec succès!", "success")
    return redirect(url_for('mes_demandes'))

@app.route('/success')
def success():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('mes_demandes.html')

@app.route('/mes-demandes')
def mes_demandes():
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Récupérer l'utilisateur
        cursor.execute("SELECT id, nom, prenom FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if not user:
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for('form'))
        
        user_id, nom, prenom = user

        # Montrer toutes les demandes pour validateur/informatique, sinon seulement celles de l'utilisateur
        role = session.get('role')
        if role in ['validateur', 'informatique']:
            cursor.execute("""
                SELECT r.id, r.objet_demande, r.date_demande, ct.name, r.date_debut_stage, r.date_fin_stage, r.acces_partages, r.status, r.rejection_comment
                FROM requests r
                LEFT JOIN collaborator_types ct ON r.collaborator_type_id = ct.id
                ORDER BY r.date_demande DESC
            """)
        else:
            cursor.execute("""
                SELECT r.id, r.objet_demande, r.date_demande, ct.name, r.date_debut_stage, r.date_fin_stage, r.acces_partages, r.status, r.rejection_comment
                FROM requests r
                LEFT JOIN collaborator_types ct ON r.collaborator_type_id = ct.id
                WHERE r.user_id = ?
                ORDER BY r.date_demande DESC
            """, (user_id,))
        demandes = cursor.fetchall()

        # Récupérer l'historique pour chaque demande
        demandes_with_history = []
        for d in demandes:
            request_id = d[0]
            cursor.execute("""
                SELECT action, comment, timestamp, actor_id
                FROM request_history
                WHERE request_id = ?
                ORDER BY timestamp ASC
            """, (request_id,))
            history_rows = cursor.fetchall()
            history = []
            for h in history_rows:
                # Get actor's name/email
                cursor.execute("SELECT nom, prenom, email FROM users WHERE id = ?", (h[3],))
                actor_row = cursor.fetchone()
                if actor_row:
                    actor = f"{actor_row[0]} {actor_row[1]} ({actor_row[2]})"
                else:
                    actor = f"Utilisateur {h[3]}"
                history.append({
                    "action": h[0],
                    "comment": h[1],
                    "timestamp": h[2],
                    "actor": actor
                })
            demandes_with_history.append({
                "demande": d,
                "history": history
            })

    return render_template('mes_demandes.html', demandes_with_history=demandes_with_history, demandeur=f"{nom} {prenom}")

@app.route('/admin/requests')
def admin_requests():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM requests')
        data = cursor.fetchall()
    return render_template('admin_table.html', rows=data)

@app.route('/user-access')
def user_access():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name as system, p.name as profile, rsp.environment
            FROM requests r
            JOIN users u ON r.user_id = u.id
            JOIN request_system_profiles rsp ON rsp.request_id = r.id
            JOIN systems s ON rsp.system_id = s.id
            JOIN profiles p ON rsp.profile_id = p.id
            WHERE u.email = ?
            ORDER BY s.name, p.name, rsp.environment
        """, (email,))
        access_rows = cursor.fetchall()
    return render_template('user_access.html', access_rows=access_rows)
@app.route('/responsable/requests')
def responsable_requests():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE email=?", (email,))
        user_row = cursor.fetchone()
        if not user_row or user_row[1] not in ['responsable', 'informatique', 'validateur']:
            flash("Accès refusé.", "danger")
            return redirect(url_for('form'))
        responsable_id = user_row[0]
        cursor.execute("""
            SELECT r.id, r.objet_demande, r.date_demande, u.nom, u.prenom, u.email
            FROM requests r
            JOIN users u ON r.user_id = u.id
            WHERE r.responsable_id=? AND r.status='soumis'
            ORDER BY r.date_demande DESC
        """, (responsable_id,))
        demandes = cursor.fetchall()
    return render_template('responsable_dashboard.html', demandes=demandes)
@app.route('/responsable/validate/<int:request_id>', methods=['POST'])
def validate_request(request_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE email=?", (email,))
        user_row = cursor.fetchone()
        # ALLOW responsable, validateur, informatique to validate
        if not user_row or user_row[1] not in ['responsable', 'informatique', 'validateur']:
            flash("Accès refusé.", "danger")
            return redirect(url_for('form'))
        validator_id = user_row[0]
        action = request.form.get('action')
        comment = request.form.get('comment', '')

        if action == 'valider':
            cursor.execute("UPDATE requests SET status=? WHERE id=?", ('validé', request_id))
            cursor.execute("INSERT INTO request_history (request_id, action, actor_id, comment) VALUES (?, 'validé', ?, ?)", (request_id, validator_id, comment))
            # Notify informatique if validator is not informatique
            if user_row[1] != 'informatique':
                cursor.execute("SELECT email FROM users WHERE role='informatique' LIMIT 1")
                info_email = cursor.fetchone()
                if info_email:
                    msg_info = EmailMessage()
                    msg_info['Subject'] = 'Nouvelle demande à traiter'
                    msg_info['From'] = 'haroun.riiahii@gmail.com'
                    msg_info['To'] = info_email[0]
                    msg_info.set_content("Une demande est à traiter. Rendez-vous sur la page /informatique/requests.")
                    try:
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                            smtp.login('haroun.riiahii@gmail.com', 'hukreegcgmihoybi')
                            smtp.send_message(msg_info)
                    except Exception as e:
                        print("[ERROR] Email to informatique error:", e)
        elif action == 'rejeter':
            cursor.execute("UPDATE requests SET status=?, rejection_comment=? WHERE id=?", ('rejeté', comment, request_id))
            cursor.execute("INSERT INTO request_history (request_id, action, actor_id, comment) VALUES (?, 'rejeté', ?, ?)", (request_id, validator_id, comment))
            # Notify demandeur
            cursor.execute("SELECT u.email FROM requests r JOIN users u ON r.user_id=u.id WHERE r.id=?", (request_id,))
            demandeur_email = cursor.fetchone()
            if demandeur_email:
                msg_dem = EmailMessage()
                msg_dem['Subject'] = 'Votre demande a été rejetée'
                msg_dem['From'] = 'haroun.riiahii@gmail.com'
                msg_dem['To'] = demandeur_email[0]
                msg_dem.set_content(f"Votre demande a été rejetée pour la raison suivante : {comment}")
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login('haroun.riiahii@gmail.com', 'hukreegcgmihoybi')
                        smtp.send_message(msg_dem)
                except Exception as e:
                    print("[ERROR] Email to demandeur error:", e)
        conn.commit()
    flash("Action effectuée.", "success")
    return redirect(url_for('view_demande', request_id=request_id))
@app.route('/informatique/requests')
def informatique_requests():
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE email=?", (email,))
        user_row = cursor.fetchone()
        if not user_row or user_row[1] != 'informatique':
            flash("Accès refusé.", "danger")
            return redirect(url_for('form'))
        info_id = user_row[0]

        cursor.execute("""
            SELECT r.id, r.objet_demande, r.date_demande, u.nom, u.prenom, u.email
            FROM requests r
            JOIN users u ON r.user_id = u.id
            WHERE r.status='en traitement'
            ORDER BY r.date_demande DESC
        """)
        demandes = cursor.fetchall()
    return render_template('informatique_dashboard.html', demandes=demandes)
@app.route('/cloturer/<int:request_id>', methods=['POST'])
def cloturer_request(request_id):
    if 'user' not in session or session.get('role') != 'informatique':
        flash("Accès refusé.", "danger")
        return redirect(url_for('form'))
    email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Mark as closed
        cursor.execute("UPDATE requests SET status=? WHERE id=?", ('cloturée', request_id))
        # Add to history
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        user_row = cursor.fetchone()
        if user_row:
            info_id = user_row[0]
            cursor.execute("INSERT INTO request_history (request_id, action, actor_id) VALUES (?, 'clôturée', ?)", (request_id, info_id))
        conn.commit()
    flash("Demande clôturée.", "success")
    return redirect(url_for('view_demande', request_id=request_id))

@app.route('/informatique/traite/<int:request_id>', methods=['POST'])
def traite_request(request_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    email = session['user']
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE email=?", (email,))
        user_row = cursor.fetchone()
        if not user_row or user_row[1] != 'informatique':
            flash("Accès refusé.", "danger")
            return redirect(url_for('form'))
        info_id = user_row[0]
        cursor.execute("UPDATE requests SET status=? WHERE id=?", ('traité', request_id))
        cursor.execute("INSERT INTO request_history (request_id, action, actor_id) VALUES (?, 'traité', ?)", (request_id, info_id))
        cursor.execute("SELECT u.email FROM requests r JOIN users u ON r.user_id=u.id WHERE r.id=?", (request_id,))
        demandeur_email = cursor.fetchone()
        if demandeur_email:
            msg_dem = EmailMessage()
            msg_dem['Subject'] = 'Votre demande est traitée'
            msg_dem['From'] = 'haroun.riiahii@gmail.com'
            msg_dem['To'] = demandeur_email[0]
            msg_dem.set_content("Votre demande a été traitée par le service informatique.")
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('haroun.riiahii@gmail.com', 'hukreegcgmihoybi')
                    smtp.send_message(msg_dem)
            except Exception as e:
                print("[ERROR] Email to demandeur error:", e)
        conn.commit()
    flash("Demande marquée comme traitée.", "success")
    return redirect(url_for('view_demande', request_id=request_id))

if __name__ == '__main__':
    app.run(debug=True)