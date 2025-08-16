from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Determine base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure QR directory exists (absolute path)
QR_FOLDER = os.path.join(BASE_DIR, "static", "qrcodes")
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

# ----------------- Database Setup -----------------
def init_db():
    with sqlite3.connect(os.path.join(BASE_DIR, "database.db")) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS qrcodes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            link TEXT,
                            qr_filename TEXT,
                            FOREIGN KEY(user_id) REFERENCES users(id))''')
    print("✅ Database initialized")

init_db()

# ----------------- Routes -----------------

@app.route("/")
def home():
    return redirect(url_for("login"))

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        try:
            with sqlite3.connect(os.path.join(BASE_DIR, "database.db")) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for("login"))
        except:
            flash("Username already exists!", "danger")
    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect(os.path.join(BASE_DIR, "database.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    with sqlite3.connect(os.path.join(BASE_DIR, "database.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT link, qr_filename FROM qrcodes WHERE user_id=?", (session["user_id"],))
        qrcodes = cursor.fetchall()
    return render_template("dashboard.html", qrcodes=qrcodes, username=session["username"])

# QR Generator
# QR Generator
@app.route("/generate", methods=["GET", "POST"])
def generate_qr():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        link = request.form["link"]
        filename = f"{session['username']}_{len(link)}.png"
        filepath = os.path.join(QR_FOLDER, filename)

        # ----- Debug prints -----
        print("BASE_DIR =>", BASE_DIR)
        print("QR_FOLDER =>", QR_FOLDER)
        print("Folder exists? =>", os.path.exists(QR_FOLDER))
        print("Files inside =>", os.listdir(QR_FOLDER))
        # ------------------------

        qr_img = qrcode.make(link)
        qr_img.save(filepath)
        with sqlite3.connect(os.path.join(BASE_DIR, "database.db")) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO qrcodes (user_id, link, qr_filename) VALUES (?, ?, ?)",
                           (session["user_id"], link, filename))
            conn.commit()
        flash("QR Code generated successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("generate.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
# 🔺 until here

# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run(debug=True)