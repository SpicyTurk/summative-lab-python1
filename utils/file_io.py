import json
import os

def save_to_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def load_from_json(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def users_to_dict(users):
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "projects": [project.id for project in user.projects],
        }
        for user in users
    ]

def projects_to_dict(projects):
    return [
        {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "due_date": project.due_date,
            "user_id": project.user.id,
            "tasks": [task.id for task in project.tasks],
        }
        for project in projects
    ]

def tasks_to_dict(tasks):
    return [
        {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "project_id": task.project.id,
            "assigned_to": task.assigned_to.id if task.assigned_to else None,
        }
        for task in tasks
    ]
