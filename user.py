import random
from collections import namedtuple

from errors import WeightError

# Connection makes working with a connection tuple easier
Connection = namedtuple('Connection', ['User', 'Weight'])


class User(object):
    """Define a user object

    Users in this case are a minimum representation with the following attrs:

        - name: Works as a unique identifier and user name for ease of
        implementation.
        - site_version: Site version could be based on a git commit hash, a
        git tag, or simply a number based system. It's a flexible way to
        handle what the user sees.
        - is_admin: Differentiate admin users so we can infect them first if
        we choose to.
        - connections: A dictionary of connections such that --
            name -> (user object, connection weight)

    In a more complete user model attributes such as age, gender, UUID, etc
    would be included in order to infect or reference users with specific
    matches.

    """
    def __init__(self, name, is_admin=False):
        self.name = name
        self.site_version = 1
        self.is_admin = is_admin
        self.connections = {}

    def add_connection(self, user, weight=None):
        """Add a connection if they aren't already connectionss.

        Neighbors are assigned a random weight (for demonstration purposes
        only). A Connection tuple is returned to provide easy access attrs.

        """
        if weight is not None and not isinstance(weight, int):
            raise WeightError

        if not self.connections.get(user.name):
            weight = weight if weight is not None else random.randrange(1, 50)
            self.connections[user.name] = Connection(user, weight)

    def remove_connection(self, user):
        """Remove a user's connection."""
        if not self.connections.get(user.name):
            return
        del self.connections[user.name]

    def get_connections(self):
        """Get all connections for a user. This generator returns tuples."""
        for key, user_data in self.connections.iteritems():
            yield user_data

    def get_weight(self, connection):
        """Get the weight of a connection to another user."""
        if not isinstance(connection, User):
            raise UserError

        connection = self.connections.get(connection.name)
        if not connection:
            return
        return connection.Weight

    def get_degree(self):
        """Get the degree or how connected the user is."""
        return len(self.connections.keys())

    def __repr__(self):
        """Object representation of a user."""
        return "<User: {name}>".format(name=self.name)

    def __str__(self):
        """String representation of a user."""
        return "User: {name}".format(name=self.name)
