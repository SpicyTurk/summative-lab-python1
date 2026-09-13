import argparse
from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from utils.file_io import (
    save_to_json, load_from_json,
    users_to_dict, projects_to_dict, tasks_to_dict,
)

console = Console()

USERS_FILE = "data/users.json"
PROJECTS_FILE = "data/projects.json"
TASKS_FILE = "data/tasks.json"


def load_all():
    users_data = load_from_json(USERS_FILE)
    for u in users_data:
        user = User(u["name"], u["email"])
        user.id = u["id"]
    User._id_counter = max((u.id for u in User.all_users), default=0) + 1

    projects_data = load_from_json(PROJECTS_FILE)
    for p in projects_data:
        user = next((u for u in User.all_users if u.id == p["user_id"]), None)
        if user:
            project = Project(p["title"], p["description"], p["due_date"], user)
            project.id = p["id"]
    Project._id_counter = max((p.id for p in Project.all_projects), default=0) + 1

    tasks_data = load_from_json(TASKS_FILE)
    for t in tasks_data:
        project = next((p for p in Project.all_projects if p.id == t["project_id"]), None)
        if project:
            task = Task(t["title"], project, t.get("assigned_to"), t.get("status", "To Do"))
            task.id = t["id"]
    Task._id_counter = max((t.id for t in Task.all_tasks), default=0) + 1


def save_all():
    save_to_json(USERS_FILE, users_to_dict(User.all_users))
    save_to_json(PROJECTS_FILE, projects_to_dict(Project.all_projects))
    save_to_json(TASKS_FILE, tasks_to_dict(Task.all_tasks))

def build_parser():
    parser = argparse.ArgumentParser(description="Task Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_user = subparsers.add_parser("add-user")
    add_user.add_argument("--name", required=True)
    add_user.add_argument("--email", required=True)

    add_project = subparsers.add_parser("add-project")
    add_project.add_argument("--user", required=True)
    add_project.add_argument("--title", required=True)
    add_project.add_argument("--description", default="")
    add_project.add_argument("--due-date", default="")

    add_task = subparsers.add_parser("add-task")
    add_task.add_argument("--project", required=True)
    add_task.add_argument("--title", required=True)
    add_task.add_argument("--assigned-to", default=None)

    subparsers.add_parser("list-users")
    subparsers.add_parser("list-projects")
    subparsers.add_parser("list-tasks")

    complete_task = subparsers.add_parser("complete-task")
    complete_task.add_argument("--title", required=True)

    return parser

def handle_command(args):
    if args.command == "add-user":
        user = User(args.name, args.email)
        console.print(f"[green]Added user:[/green] {user}")

    elif args.command == "add-project":
        user = User.find_name(args.user)
        if not user:
            console.print(f"[red]No user found named '{args.user}'[/red]")
            return
        project = Project(args.title, args.description, args.due_date, user)
        console.print(f"[green]Added project:[/green] {project}")

    elif args.command == "add-task":
        project = Project.find_by_title(args.project)
        if not project:
            console.print(f"[red]No project found titled '{args.project}'[/red]")
            return
        task = Task(args.title, project, assigned_to=args.assigned_to)
        console.print(f"[green]Added task:[/green] {task}")

    elif args.command == "list-users":
        table = Table(title="Users")
        table.add_column("ID"); table.add_column("Name"); table.add_column("Email"); table.add_column("Projects")
        for u in User.all_users:
            table.add_row(str(u.id), u.name, u.email, str(len(u.projects)))
        console.print(table)

    elif args.command == "list-projects":
        table = Table(title="Projects")
        table.add_column("ID"); table.add_column("Title"); table.add_column("Owner"); table.add_column("Tasks")
        for p in Project.all_projects:
            table.add_row(str(p.id), p.title, p.user.name, str(len(p.tasks)))
        console.print(table)

    elif args.command == "list-tasks":
        table = Table(title="Tasks")
        table.add_column("ID"); table.add_column("Title"); table.add_column("Status"); table.add_column("Project")
        for t in Task.all_tasks:
            table.add_row(str(t.id), t.title, t.status, t.project.title)
        console.print(table)

    elif args.command == "complete-task":
        task = next((t for t in Task.all_tasks if t.title == args.title), None)
        if not task:
            console.print(f"[red]No task found titled '{args.title}'[/red]")
            return
        task.status = "Done"
        console.print(f"[green]Marked complete:[/green] {task}")

    else:
        console.print("[yellow]No command given. Use --help to see options.[/yellow]")

if __name__ == "__main__":
    load_all()
    parser = build_parser()
    args = parser.parse_args()
    handle_command(args)
    save_all()