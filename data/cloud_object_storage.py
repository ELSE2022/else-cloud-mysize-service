import swiftclient

connection: swiftclient.Connection = None


def connect_to_storage(credentials:dict):
    global connection
    connection = swiftclient.Connection(**credentials)


def get_containers():
    account = connection.get_account()
    return account[1] if account is not None and len(account) > 1 else None
