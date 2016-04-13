# Khan Academy Infection Problem

This is my implementation of the Khan Academy "Infection" problem. It does not
require any additional dependencies to be installed but does work best when
using **Python 2.7+** and a TTY shell which has color support.

It implements four different types of A/B testing infection situations
including:

- **Total Infection:** Starting with a single user, it changes the site
  version of that user and all other connections in the system. This includes
  relationships such as "is coach of" and "coached by". Total infection will
  stop once all connections have been exhausted and has a possibility of
  infecting the entire system.
- **Limited Infection:** Starting with a single user, it attempts to infect a
  certain number of users within the system without exceeding that number.
  This implementation favors users with a greater connection (students more
  active in the class) before those who are not as active.
- **Exact Infection:** Starting with a single user, the system attempts to
  infect the exact number of users. If there are not enough users in the
  system then it raises an error. If there are not enough connections to
  fullfill the infection then it also raises an error.
- **Admin Infection:** To make infecting Khan Academy admin users easier, an
  admin infection will target all admin users and their connections acting as
  a total infection would. This does not require a starting user.

## Design Decisions

In this process, I attempted to keep the models as simple as possible. The
user model uses a "name" as a unique identifier. In a normal situation
incremental IDs or UUIDs would be used to identify a user with name, gender,
age, etc all being a part of the model.

I'm using an undirected graph to model the relationships between users with
weighted edges being supported. In this demonstration the weights can be
randomized or supplied via a config file. In reality I imagine weights will
correlate to particiation in a Khan Academy course. For instance if a student
interacts with the teacher every day the edge between them will carry a higher
weight. This knowledge can then be used in limited and exact infections where
we may have members of a class with different site versions. This will favor
those students leading to a less likely chance of noticable difference.

A priority queue is used (rather than a normal queue) in limited and exact
infections where higher weights are preferred. For this reason a multiplier is
used which will push further connections down leading to closer connections
being satisfied first.

It is a useful system although it certainly has flaws seeing as there may
still be discrepencies between classrooms depending on the infection upper
bound.

## Writing Test Cases

Config files can be used to build a graph of connected users. Config files can
be found in the `data` directory. Config files should follow the format:

```
User1 User2 Weight
User1 User3 Weight
```

If the file can not be loaded then an error will occur stating so. The names
used in the config file will be the indentifiers for each user in the system
and will be the key used in the `-i` command to choose an infection starting
point.

**User Types:**
User types can be specified in a config file using the following notation:

```
User1:admin User2:default Weight
```

If no type is specified then it is assumed they are a default user.

## Running Infections

Running infections can be done in a shell by using the `run.py` file. For
help, use the `-h` flag like so:

```
$ python run.py -h
Usage: run.py [options]

Options:
  -h, --help            show this help message and exit
  -t TYPE, --type=TYPE  Infection types may be total, limited, exact, admin
  -d DATA, --data=DATA  Specify a .txt file with each line specifying graph
                        edges and weights: EX: Dan Jesse 5
  -i INFECT, --infect=INFECT
                        State a name to start the infection from NOTE:
                        applicable to total and admin infections only
  -m MAX, --max=MAX     Limit the number of infections. NOTE: Applicable to
                        limited and exact infections only
```

**Total Infection:**
Running a total infection can be done via:

```
python run.py -t total -d data/random.txt -i user43
```

**Limited Infection:**
Running a limited infection can be done via:

```
python run.py -t limited -d data/random.txt -i user43 -m 20
```

**Exact Infection:**
Running an exact infection can be done via:

```
python run.py -t exact -d data/random.txt -i user43 -m 10
```

**Admin Infection:**
Running an admin infection requires admin users in the config file. It can be done via:

```
python run.py -t admin -d data/admin.txt
```
