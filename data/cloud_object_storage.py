import swiftclient
from .Container import Container

connection: swiftclient.Connection = None


def connect_to_storage(credentials: dict):
    global connection
    connection = swiftclient.Connection(**credentials)


def get_containers():
    global connection
    account = connection.get_account()

    if account is not None and len(account) > 1:
        return [Container(connection, con['name']) for con in account[1]]


def get_container(name):
    containers = get_containers()
    for con in containers:
        if con.name == name:
            return con
