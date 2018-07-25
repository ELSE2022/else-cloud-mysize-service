from orientdb_data_layer import data_connection
from data import models


def connect(host, db_name, user, password, initial_drop=False):
    data_connection.connect_database(f'{host}/{db_name}', user, password, initial_drop)


def database_connect_service(host, db_name, user, password):
    connect(host, db_name, user, password)
    data_connection.attach_models()


def database_update_service(host, db_name, user, password, initial_drop):
    connect(host, db_name, user, password, initial_drop)
    data_connection.refresh_models()
