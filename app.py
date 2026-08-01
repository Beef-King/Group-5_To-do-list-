
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from email_service import send_email
import sqlite3

app = Flask(__name__)

app.secret_key = "group5_secret_key"

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("view_tasks"))
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for("login"))

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        connection.close()
        flash("Email already exists", "error")
        return redirect(url_for("login"))

    hashed_password = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users(first_name, last_name, email, password)
        VALUES (?, ?, ?, ?)
    """, (first_name, last_name, email, hashed_password))

    connection.commit()
    connection.close()

    flash("Account created successfully! Please sign in.", "success")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("view_tasks"))

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["first_name"] = user["first_name"]
            flash(f"Welcome back, {user['first_name']}!", "success")
            return redirect(url_for("view_tasks"))

        flash("Invalid email or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/create", methods=["GET", "POST"])
def create_task():

    if "user_id" not in session:
            return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        print("Form data received:", request.form)  # Debugging line
        
        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        priority = request.form["priority"]
        due_date = request.form.get("due_date")
 
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, category, priority, due_date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            (title, description, category, priority, due_date, user_id)
        )
        connection.commit()
        connection.close()
 
        return redirect(url_for("view_tasks"))
 
    return render_template("create_task.html")

@app.route("/about")
def about():
    return render_template("about.html")

#send everything from here down to Beef_King

@app.route("/tasks")
def view_tasks():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
    "SELECT * FROM tasks WHERE user_id=?",
    (session["user_id"],)
)
    tasks = cursor.fetchall()


    connection.close()

    return render_template("view_task.html", tasks=tasks)

@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():

    if "user_id" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id=?", (session["user_id"],))
    tasks = [dict(task) for task in cursor.fetchall()]

    connection.close()
    return jsonify(tasks), 200

@app.route("/api/tasks/<int:id>", methods=["GET"])
def api_get_task(id):
    if "user_id" not in session:
        return jsonify({"message": "Unauthorized"}), 401
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", (id, session["user_id"]))
    task = cursor.fetchone()

    connection.close()

    if task:
        return jsonify(dict(task)), 200

    return jsonify({"message": "Task not found"}), 404




@app.route("/api/tasks", methods=["POST"])
def api_create_task():

    data = request.get_json()

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (title, description, category, priority, due_date, status, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["category"],
        data["priority"],
        data["due_date"],
        "Pending",
        session["user_id"]
    ))

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Task created successfully",
        "id": task_id
    }), 201

@app.route("/api/tasks/<int:id>", methods=["PUT"])
def api_update_task(id):

    if "user_id" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE tasks
    SET
        title=?,
        description=?,
        category=?,
        priority=?,
        due_date=?
    WHERE id=? AND user_id=?
""", (
    data["title"],
    data["description"],
    data["category"],
    data["priority"],
    data["due_date"],
    id,
    session["user_id"]
))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Task updated successfully"
    }), 200

@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def api_delete_task(id):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200

@app.route("/api/tasks/search", methods=["GET"])
def api_search_tasks():

    query = request.args.get("q", "")

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE (title LIKE ? OR description LIKE ?) AND user_id=?
    """, (
        f"%{query}%",
        f"%{query}%",
        session["user_id"]
    ))

    tasks = [dict(task) for task in cursor.fetchall()]

    connection.close()

    return jsonify(tasks), 200

@app.route("/api/tasks/filter", methods=["GET"])
def api_filter_tasks():

    category = request.args.get("category")
    priority = request.args.get("priority")
    status = request.args.get("status")

    sql = "SELECT * FROM tasks WHERE user_id=?"
    values = [session["user_id"]]

    if category:
        sql += " AND category=?"
        values.append(category)

    if priority:
        sql += " AND priority=?"
        values.append(priority)

    if status:
        sql += " AND status=?"
        values.append(status)

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(sql, values)

    tasks = [dict(task) for task in cursor.fetchall()]

    connection.close()

    return jsonify(tasks), 200

@app.route("/complete/<int:id>", methods=["POST"])
def complete_task(id):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT status FROM tasks WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )

    task = cursor.fetchone()

    if task:
        current_status = task[0]

        if current_status == "Pending":
            new_status = "Completed"
        else:
            new_status = "Pending"

        cursor.execute(
            "UPDATE tasks SET status=? WHERE id=? AND user_id=?",
            (new_status, id, session["user_id"])
        )

        connection.commit()

    connection.close()

    return redirect(url_for("view_tasks"))

@app.route("/api/reminders")
def api_reminders():

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT
            tasks.id,
            tasks.title,
            tasks.due_date,
            users.email
        FROM tasks
        JOIN users
        ON tasks.user_id = users.id
        WHERE
            tasks.status = 'Pending'
            AND tasks.reminder_sent = 0
            AND DATE(tasks.due_date) = ?
    """, (tomorrow,))

    reminders = cursor.fetchall()

    emails_sent = 0

    for reminder in reminders:

        subject = "⏰ Task Reminder"

        body = f"""
Hello!

This is a reminder that your task:

{reminder['title']}

is due tomorrow ({reminder['due_date']}).

Log into TaskHub to complete it.

Have a productive day!

- TaskHub
"""

        send_email(
            reminder["email"],
            subject,
            body
        )

        cursor.execute("""
            UPDATE tasks
            SET reminder_sent = 1
            WHERE id = ?
        """, (reminder["id"],))

        emails_sent += 1

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "emails_sent": emails_sent
    })


if __name__ == "__main__":
    app.run(debug=True)