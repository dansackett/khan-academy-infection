from Queue import Queue, PriorityQueue

from user import User


INFECTION_TYPES = ['total', 'limited', 'exact', 'admin']


def total_infection(graph, options):
    """Total infection infects selected users and all of their connections.

    This process will move down a graph of connected users infecting everyone
    until their exists no more connections. It could potentially infect an
    entire user base if the connections are there.

    """
    infected = set()

    user = graph.get_user(options.infect)

    if not user:
        exit('ERROR: User not found')

    queue = Queue()
    queue.put(user)

    while not queue.empty():
        user = queue.get()

        if user not in infected:
            user.site_version = 2
            infected.add(user)

            for connection in user.get_connections():
                queue.put(connection.User)


def exact_infection(graph, options):
    """Exact infection will infect exactly the number specified.

    It works just like limited infection but if the number cannot be satisfied
    then it fails.

    """
    infected = set()
    queue = PriorityQueue()
    initial_user = graph.get_user(options.infect)
    multiplier = 1

    if not initial_user:
        exit('ERROR: User not found')

    if graph.size() < options.max:
        exit('ERROR: Graph has less than {max} users'.format(max=options.max))

    queue.put((0, initial_user))

    while len(infected) < options.max:
        if queue.empty() and len(infected) < options.max:
            exit('ERROR: Not enough connections')

        weight, user = queue.get()

        if user not in infected:
            user.site_version = 2
            infected.add(user)

            for connection in user.get_connections():
                queue.put((-multiplier * connection.Weight, connection.User))

        multiplier += 1


def limited_infection(graph, options):
    """Limited infection allows an infection to remain contained.

    Instead of allowing a full infection, we can keep the potential number of
    infections to a set number. This approach will use weighted connections as
    a means to decide which connections to infect. This weight will likely
    correlate to participation in a class so students who frequent more with
    the teacher see what they see.

    """
    infected = set()
    queue = PriorityQueue()
    initial_user = graph.get_user(options.infect)
    multiplier = 1

    if not initial_user:
        exit('ERROR: User not found')

    queue.put((0, initial_user))

    while len(infected) < options.max:
        if queue.empty():
            break

        weight, user = queue.get()

        if user not in infected:
            user.site_version = 2
            infected.add(user)

            for connection in user.get_connections():
                queue.put((-multiplier * connection.Weight, connection.User))

        multiplier += 1


def admin_infection(graph, options):
    """Admin infection ensures that admin users and their connections will be
    infected.

    In this case, we begin with the Khan Academy team and their students.
    It will act like total_infection in its range but it will not start on a
    user which is not an admin account. We add all admins to the queue instead
    of a selected user.

    """
    infected = set()
    queue = Queue()

    for user in graph.get_admin_users():
        queue.put(user)

    while not queue.empty():
        user = queue.get()

        if user not in infected:
            user.site_version = 2
            infected.add(user)

            for connection in user.get_connections():
                queue.put(connection.User)


def run_infection(options, graph):
    """Based on the option selected in the CLI, run the infection function."""
    switcher = {
        'total': total_infection,
        'limited': limited_infection,
        'exact': exact_infection,
        'admin': admin_infection,
    }
    return switcher.get(options.type)(graph, options)
