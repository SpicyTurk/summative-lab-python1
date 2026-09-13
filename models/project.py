class Project:
    _id_counter = 1
    all_projects = []

    def __init__(self, title, description, due_date, user):
        self.id = Project._id_counter
        Project._id_counter += 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user = user
        self.tasks = []
        Project.all_projects.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a string and not empty.")
        self._title = value.strip()

    def add_task(self, task):
        self.tasks.append(task)

    @classmethod
    def find_by_title(cls, title):
        return next((project for project in cls.all_projects if project.title == title), None)

    def __repr__(self):
        return f"Project(id={self.id}, title='{self.title}', description='{self.description}', due_date='{self.due_date}', user={self.user}, tasks={self.tasks})"
