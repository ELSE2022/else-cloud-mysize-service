from pyorient.ogm import Graph, Config
from pyorient.ogm.declarative import declarative_node, declarative_relationship

NodeBase = declarative_node()
RelationshipBase = declarative_relationship()

graph: Graph = None


def is_connected():
    global graph
    return graph is not None

def get_graph():
    return graph

def connect_database(host, database, user, password):
    global graph
    graph = Graph(Config.from_url('plocal://5.153.55.125:2424/test', 'root', '5e256570-8870-4441-9f88-6194f4fefd9a'))
    graph.create_all(NodeBase.registry)
    graph.create_all(RelationshipBase.registry)


def get_dbsize():
    global graph
    if is_connected():
        return graph.client.db_size()
