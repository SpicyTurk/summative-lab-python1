from models.user import User

class Task:
    _id_counter = 1
    all_tasks = []
    VALID_STATUSES = ["To Do", "In Progress", "Done"]

    def __init__(self, title, project, assigned_to=None, status="To Do"):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.project = project
        self.assigned_to = assigned_to
        self.status = status
        project.add_task(self)
        Task.all_tasks.append(self)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}.")
        self._status = value

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value):
        if value is not None and not isinstance(value, User):
            raise ValueError("assigned_to must be a User instance or None.")
        self._assigned_to = value

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}', assigned_to={self.assigned_to})"