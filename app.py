from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create_task():
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
            "INSERT INTO tasks (title, description, category, priority, due_date) VALUES (?, ?, ?, ?, ?)",
            (title, description, category, priority, due_date)
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
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    connection.close()

    print("Tasks retrieved:", tasks)  # Debugging line

    return render_template("view_task.html", tasks=tasks)


@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = [dict(task) for task in cursor.fetchall()]

    connection.close()
    return jsonify(tasks), 200

@app.route("/api/tasks/<int:id>", methods=["GET"])
def api_get_task(id):

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
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
        (title, description, category, priority, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["category"],
        data["priority"],
        data["due_date"],
        "Pending"
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
        WHERE id=?
    """, (
        data["title"],
        data["description"],
        data["category"],
        data["priority"],
        data["due_date"],
        id
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
        "DELETE FROM tasks WHERE id=?",
        (id,)
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
        WHERE title LIKE ?
        OR description LIKE ?
    """, (
        f"%{query}%",
        f"%{query}%"
    ))

    tasks = [dict(task) for task in cursor.fetchall()]

    connection.close()

    return jsonify(tasks), 200

@app.route("/api/tasks/filter", methods=["GET"])
def api_filter_tasks():

    category = request.args.get("category")
    priority = request.args.get("priority")
    status = request.args.get("status")

    sql = "SELECT * FROM tasks WHERE 1=1"
    values = []

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
        "SELECT status FROM tasks WHERE id=?",
        (id,)
    )

    task = cursor.fetchone()

    if task:
        current_status = task[0]

        if current_status == "Pending":
            new_status = "Completed"
        else:
            new_status = "Pending"

        cursor.execute(
            "UPDATE tasks SET status=? WHERE id=?",
            (new_status, id)
        )

        connection.commit()

    connection.close()

    return redirect(url_for("view_tasks"))

if __name__ == "__main__":
    app.run(debug=True)