from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/tasks")
def view_tasks():
    return render_template("view_task.html")

if __name__ == "__main__":
    app.run(debug=True)