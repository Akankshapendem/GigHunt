
import os
import sqlite3
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, jsonify, g, send_from_directory, flash

APP_NAME = "GigHunt"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

STATUSES = ["Wishlist", "Applied", "Interview", "Offer", "Rejected"]
ACTIVITY_TYPES = ["Applications", "Interviews", "Offers", "Networking"]

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB upload
app.secret_key = "dev-secret-change-me"


def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
        ensure_schema(conn)
    return g.db


def ensure_schema(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT,
            link TEXT,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'Wishlist',
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            kind TEXT NOT NULL,
            due_date TEXT,
            is_completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            kind TEXT NOT NULL,
            url TEXT,
            file_path TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT,
            company TEXT,
            email TEXT,
            phone TEXT,
            notes TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()

   

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def board():
    db = get_db()
    rows = [dict(x) for x in db.execute("SELECT * FROM jobs ORDER BY id DESC")]
    columns = {s: [] for s in STATUSES}
    for r in rows:
        columns.setdefault(r["status"], []).append(r)
    return render_template("board.html", app_name=APP_NAME, statuses=STATUSES, columns=columns)


@app.route("/jobs", methods=["POST"])
def create_job():
    db = get_db()
    f = request.form
    title = f.get("title","").strip()
    if not title:
        flash("Job title is required", "error")
        return redirect(url_for("board"))
    db.execute(
        "INSERT INTO jobs (title, company, link, notes, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (title, f.get("company","").strip(), f.get("link","").strip(), f.get("notes","").strip(), f.get("status","Wishlist"), datetime.utcnow().isoformat())
    )
    db.commit()
    return redirect(url_for("board"))


@app.route("/api/jobs/<int:job_id>/move", methods=["POST"])
def move_job(job_id):
    db = get_db()
    data = request.get_json(force=True)
    status = data.get("status")
    if status not in STATUSES:
        return jsonify({"ok": False, "error":"Invalid status"}), 400
    db.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    db = get_db()
    db.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/activities")
def activities():
    db = get_db()
    flt = request.args.get("filter","all")
    today = date.today().isoformat()
    query = "SELECT * FROM activities"
    params = []
    if flt == "due_today":
        query += " WHERE due_date = ? AND is_completed = 0"; params.append(today)
    elif flt == "past_due":
        query += " WHERE due_date IS NOT NULL AND due_date < ? AND is_completed = 0"; params.append(today)
    elif flt == "pending":
        query += " WHERE is_completed = 0"
    elif flt == "completed":
        query += " WHERE is_completed = 1"
    query += " ORDER BY COALESCE(due_date,'9999-12-31') ASC, id DESC"
    items = [dict(x) for x in db.execute(query, params).fetchall()]
    return render_template("activities.html", app_name=APP_NAME, items=items, flt=flt, kinds=ACTIVITY_TYPES)


@app.route("/activities", methods=["POST"])
def add_activity():
    db = get_db()
    f = request.form
    title = f.get("title","").strip()
    if not title:
        flash("Activity title required", "error")
        return redirect(url_for("activities"))
    db.execute(
        "INSERT INTO activities (title, kind, due_date, is_completed, created_at) VALUES (?, ?, ?, ?, ?)",
        (title, f.get("kind","Applications"), (f.get("due_date") or None), 0, datetime.utcnow().isoformat())
    )
    db.commit()
    return redirect(url_for("activities"))


@app.route("/activities/<int:act_id>/complete", methods=["POST"])
def complete_activity(act_id):
    db = get_db()
    db.execute("UPDATE activities SET is_completed = 1 WHERE id = ?", (act_id,))
    db.commit()
    return redirect(url_for("activities"))


@app.route("/documents")
def documents():
    db = get_db()
    docs = [dict(x) for x in db.execute("SELECT * FROM documents ORDER BY id DESC").fetchall()]
    return render_template("documents.html", app_name=APP_NAME, docs=docs)


@app.route("/documents/link", methods=["POST"])
def add_link_document():
    db = get_db()
    f = request.form
    title = f.get("title","").strip()
    url = f.get("url","").strip()
    if not title or not url:
        flash("Both title and URL required", "error")
        return redirect(url_for("documents"))
    db.execute(
        "INSERT INTO documents (title, kind, url, file_path, created_at) VALUES (?, 'link', ?, NULL, ?)",
        (title, url, datetime.utcnow().isoformat())
    )
    db.commit()
    return redirect(url_for("documents"))


@app.route("/documents/upload", methods=["POST"])
def upload_document():
    db = get_db()
    file = request.files.get("file")
    title = request.form.get("title","").strip() or (file.filename if file else "")
    if not file or file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("documents"))
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    safe_name = file.filename.replace("/", "_")
    path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
    file.save(path)
    db.execute(
        "INSERT INTO documents (title, kind, url, file_path, created_at) VALUES (?, 'file', NULL, ?, ?)",
        (title, safe_name, datetime.utcnow().isoformat())
    )
    db.commit()
    return redirect(url_for("documents"))


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)


@app.route("/contacts")
def contacts():
    db = get_db()
    rows = [dict(x) for x in db.execute("SELECT * FROM contacts ORDER BY id DESC").fetchall()]
    return render_template("contacts.html", app_name=APP_NAME, contacts=rows)


@app.route("/contacts", methods=["POST"])
def add_contact():
    db = get_db()
    f = request.form
    name = f.get("name","").strip()
    if not name:
        flash("Name is required", "error")
        return redirect(url_for("contacts"))
    db.execute(
        "INSERT INTO contacts (name, role, company, email, phone, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, f.get("role","").strip(), f.get("company","").strip(), f.get("email","").strip(), f.get("phone","").strip(), f.get("notes","").strip(), datetime.utcnow().isoformat())
    )
    db.commit()
    return redirect(url_for("contacts"))


@app.route("/metrics")
def metrics():
    db = get_db()
    def c(q, p=()): return db.execute(q, p).fetchone()[0]
    jobs_saved = c("SELECT COUNT(*) FROM jobs")
    applications = c("SELECT COUNT(*) FROM jobs WHERE status='Applied'")
    interviews = c("SELECT COUNT(*) FROM jobs WHERE status='Interview'")
    offers = c("SELECT COUNT(*) FROM jobs WHERE status='Offer'")
    activities_started = c("SELECT COUNT(*) FROM activities")
    contacts_saved = c("SELECT COUNT(*) FROM contacts")
    notes_saved = c("SELECT COUNT(*) FROM jobs WHERE TRIM(COALESCE(notes,'')) <> ''")

    funnel_labels = ["Jobs Saved", "Applications", "Interviews", "Offers"]
    funnel_values = [jobs_saved, applications, interviews, offers]
    return render_template("metrics.html", app_name=APP_NAME,
        jobs_saved=jobs_saved, activities_started=activities_started,
        contacts_saved=contacts_saved, notes_saved=notes_saved,
        funnel_labels=funnel_labels, funnel_values=funnel_values)


if __name__ == "__main__":
    print("CareerBoard+ → http://127.0.0.1:5000")
    app.run(debug=True)
