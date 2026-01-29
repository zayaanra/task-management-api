from flask import Flask, request

app = Flask(__name__)

task_id = 0
class Task:
    def __init__(self, id: int, title: str, completed: bool, created_at: str):
        self.id = id
        self.title = title
        self.completed = completed
        self.created_at = created_at

tasks = []


@app.route("/tasks", methods=['POST'])
def create_task():
    content = request.json
    