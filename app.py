from flask import Flask, jsonify, request, render_template
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# ---------- API Routes ----------

@app.route("/api/todos", methods=["GET"])
def get_todos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.json
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title) VALUES (%s)", (data['title'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task added successfully"}), 201

@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET completed=%s WHERE id=%s", (data['completed'], todo_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task updated successfully"})

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=%s", (todo_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task deleted successfully"})

# ---------- UI Route ----------

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
