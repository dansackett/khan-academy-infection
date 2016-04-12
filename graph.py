from errors import ConnectionError, UserError
from user import User


class UserGraph(object):
    """UserGraph defines the relationships between independent users.

    It's an implementation of an undirected graph where relationships go both
    ways allowing us to handle "is coached by" and "is student of"
    relationships. Users in the graph are reprsented as a hash map with the
    name of the user (unique identifier) being the key to the user object.

    """
    def __init__(self):
        self.users = {}

    def size(self):
        """Get the size of the graph"""
        return len(self.users.keys())

    def add_user(self, name, is_admin=False):
        """Add a user to the graph if they aren't already included."""
        user = self.users.get(name)
        if not user:
            user = User(name, is_admin)
            self.users[name] = user
        return user

    def add_admin(self, name):
        """Add an admin user to the graph if they aren't already included."""
        return self.add_user(name, True)

    def get_user(self, name):
        """Get a single user from the graph"""
        return self.users.get(name)

    def get_all_users(self):
        """Return all users in the graph through a generator."""
        for user in self.users.values():
            yield user

    def get_admin_users(self):
        """Return only admin users in the graph through a generator."""
        for user in self.get_all_users():
            if user.is_admin:
                yield user

    def remove_user(self, user):
        """Remove a user from the graph. Requires a user.User object"""
        if not isinstance(user, User):
            raise UserError

        if self.users.get(user.name):
            del self.users[user.name]

    def add_connection(self, coach, student, weight=None):
        """Add a connection between a coach and a student.

        This connection requires two user.User objects and creates an
        undirected relationship between the two.

        """
        if not isinstance(coach, User) or not isinstance(student, User):
            raise ConnectionError

        coach.add_connection(student, weight)
        student.add_connection(coach, weight)

    def remove_connection(self, coach, student):
        """Remove a connection between a coach and student.

        The users must both be user.User objects and removes the connection on
        both ends of the undirected graph.

        """
        if not isinstance(coach, User) or not isinstance(student, User):
            raise ConnectionError

        coach.remove_connection(student)
        student.remove_connection(coach)
