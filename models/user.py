from models.person import Person

class User(Person):
    _id_counter = 1
    all_users = []

    def __init__(self, name, email):
        super().__init__(name, email)
        self.id = User._id_counter
        User._id_counter += 1
        self.projects = []
        User.all_users.append(self)

    def add_project(self, project):
        self.projects.append(project)

    @classmethod
    def find_name(cls, name):
        return next((user for user in cls.all_users if user.name == name), None)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', projects={self.projects})"
