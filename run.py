import sys
from optparse import OptionParser

from errors import FileError
from graph import UserGraph
from infections import (
    INFECTION_TYPES,
    total_infection,
    limited_infection,
    exact_infection,
    admin_infection,
    run_infection,
)

RED = '\033[31m'
COLOROFF = '\033[0m'


def add_user(graph, str):
    """Convenience function to ensure we add the correct type of user"""
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


def infected_print(user, str):
    """Add color codes to print output for a TTY shell"""
    if user.site_version == 2:
        if sys.stdout.isatty():
            return '{red}{str}{off}'.format(red=RED, str=str, off=COLOROFF)
        return 'X - {}'.format(str)
    else:
        return '{}'.format(str)


def show_infection(graph):
    """Show infections prints the graph representation in an adjacency list"""
    for user in graph.get_all_users():
        print infected_print(user, user.name) + ' ::',
        for connection in user.get_connections():
            name = connection.User.name
            print infected_print(connection.User, name),
        print


if __name__ == '__main__':
    types_str = ', '.join(INFECTION_TYPES)
    msgs = {
        'type': 'Infection types may be {types}'.format(types=types_str),
        'data': ('Specify a .txt file with each line specifying graph edges '
                 'and weights: EX: Dan Jesse 5'),
        'infect': ('State a name to start the infection from NOTE: '
                   'applicable to total and admin infections only'),
        'max': ('Limit the number of infections. NOTE: Applicable to limited '
                'and exact infections only'),
    }

    parser = OptionParser()
    parser.add_option('-t', '--type', dest='type', help=msgs['type'],
                      action='store')
    parser.add_option('-d', '--data', dest='data', help=msgs['data'],
                      action='store')
    parser.add_option('-i', '--infect', dest='infect', help=msgs['infect'],
                      action='store')
    parser.add_option('-m', '--max', dest='max', help=msgs['max'],
                      action='store', type='int')

    (options, args) = parser.parse_args()

    if not options.type:
        exit('ERROR: You must select a type of infection to run')

    if options.type not in INFECTION_TYPES:
        exit('ERROR: Infection type should be either {types}',format(types=types_str))

    if not options.data:
        exit('ERROR: You must specify a file to load from')

    if options.type != 'admin' and not options.infect:
        exit('ERROR: You must specify a user to infect')

    if options.type == 'limited' and not options.max:
        exit('ERROR: You must specify a maximum number of users to infect')

    graph = build_graph(options.data)
    run_infection(options, graph)
    show_infection(graph)
