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


def connect_database(host, user, password, is_initial_drop=False):
    global graph
    graph = Graph(Config.from_url(host, user, password, is_initial_drop))
    graph.create_all(NodeBase.registry)
    graph.create_all(RelationshipBase.registry)


def get_dbsize():
    global graph
    if is_connected():
        return graph.client.db_size()
