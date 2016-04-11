from optparse import OptionParser
from Queue import Queue

from errors import FileError
from graph import UserGraph


def total_infection(graph, args):
    """Total infection infects selected users and all of their connections.

    This process will move down a graph of connected users infecting everyone
    until their exists no more connections. It could potentially infect an
    entire user base if the connections are there.

    """
    infected = set()
    queue = Queue()

    return infected


def limited_infection(graph, args):
    """Limited infection allows an infection to remain contained.

    Instead of allowing a full infection, we can keep the potential number of
    infections to a set number. This approach will use weighted connections as
    a means to decide which connections to infect.

    """
    infected = set()
    queue = Queue()

    return infected


def admin_infection(graph, args):
    """Admin infection ensures that admin users and their connections will be
    infected.

    In this case, we begin with the Khan Academy team and their students.
    It will act like total_infection in its range but it will not start on a
    user which is not an admin account.

    """
    infected = set()
    queue = Queue()

    return infected


def run_infection(option, graph, args):
    """Based on the option selected in the CLI, run the infection function."""
    switcher = {
        'total': total_infection,
        'limited': limited_infection,
        'admin': admin_infection,
    }
    return switcher.get(option, lambda x: 'Option not found...')(graph, args)


def add_user(graph, str):
    """Tiny function to ensure we add the correct type of user"""
    split = str.split(":")

    if len(split) > 2:
        raise FileError
    elif len(split) == 2:
        name, type = split

        if type not in ['default', 'admin']:
            raise FileError

        return graph.add_admin(name) if type == 'admin' else graph.add_user(name)

    return graph.add_user(str)


def build_graph(file):
    """Load a .txt file into a UserGraph object"""
    graph = UserGraph()

    with open(file) as f:
        for line in f.readlines():
            vals = line.split()
            try:
                user1 = add_user(graph, vals[0])
                user2 = add_user(graph, vals[1])
                graph.add_connection(user1, user2, int(vals[2]))
            except:
                raise FileError

    return graph


if __name__ == '__main__':
    msgs = {
        'type': 'Infection types may be [total, limited, admin]',
        'data': ('Specify a .txt file with each line specifying graph edges '
                 'and weights EX: Dan Jesse 5'),
    }

    parser = OptionParser()
    parser.add_option('-t', '--type', dest='type', help=msgs['type'],
                      action='store')
    parser.add_option('-d', '--data', dest='data', help=msgs['data'],
                      action='store')

    (options, args) = parser.parse_args()

    if not options.type:
        exit('ERROR: You must select a type of infection to run')

    if options.type not in ['total', 'limited', 'admin']:
        exit('ERROR: Infection type should be either "total", "limited", or "admin"')

    if not options.data:
        exit('ERROR: You must specify a file to load from')

    graph = build_graph(options.data)
    infected_users = run_infection(options.type, graph, args)

    print infected_users
