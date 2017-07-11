import pyorient

__data_client = None


def __is_connected():
    global __data_client
    return __data_client is not None


def connect_database(host, database, user, password):
    global __data_client
    __data_client = pyorient.OrientDB(host, 2424)
    __data_client.db_open(database, user, password)


def get_dbsize():
    global __data_client
    if __is_connected():
        return __data_client.db_size()
