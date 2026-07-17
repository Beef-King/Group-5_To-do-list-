from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create")
def create_task():
    return render_template("create_task.html")

@app.route("/tasks")
def view_tasks():
    return render_template("view_task.html")

if __name__ == "__main__":
    app.run(debug=True)