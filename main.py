from datetime import datetime
from flask import Flask, request, Response

app = Flask(__name__)

class Task:
    def __init__(self, id: int, title: str, completed: bool, created_at: str):
        self.id = id
        self.title = title
        self.completed = completed
        self.created_at = created_at

tasks = []

@app.route("/tasks", methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        content = request.json

        # check if POST request body is valid
        if 'title' not in content or 'completed' not in content:
            return Response(status=400)
        
        # check for duplicate records
        for task in tasks:
            if task.title == content['title']:
                return Response(status=403)
        
        task = Task(len(tasks), content['title'], content['completed'], datetime.now().strftime('%d%m%Y_%H:%M:%S'))
        tasks.append(task)

        return Response(status=201)
    
    completed = request.args.get('completed')
    if completed is None:
        return {'tasks': tasks}
    
    filtered_tasks = []
    for task in tasks:
        if bool(completed) == task.completed:
            filtered_tasks.append({'title': task.title, 'completed': task.completed})

    return {'tasks': filtered_tasks}

@app.route("/tasks/<id>", methods=['DELETE', 'PATCH'])
def update_task(id):
    content = request.json

    id = int(id)
    if id < 0 or id >= len(tasks):
        return Response(status=404)
    
    if request.method == 'PATCH':
        # title and completed not present - body is malformed
        if 'title' not in content and 'completed' not in content:
            return Response(status=400)
        
        if 'title' in content:
            tasks[id].title = content['title']
        
        if 'completed' in content:
            tasks[id].completed = content['completed']

        return Response(status=200)
    
    if request.method == 'DELETE':
        del tasks[id]
        return Response(status=204)
    