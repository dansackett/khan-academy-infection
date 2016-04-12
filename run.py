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
    infected_users = run_infection(options, graph)

    print infected_users
