import swiftclient


class Container(object):
    __connection: swiftclient.Connection = None
    name: str = None

    def __init__(self, conn, name):
        self.connection = conn
        self.name = name

    def add_object(self, name, content):
        self.__connection.put_object(self.name, name, contents=content, content_type='text/plain')

    def list_objects(self):
        self.__connection.get_container(self.name)

    def get_object(self, name):
        self.__connection.get_object(self.name, name)

    def delete_object(self, name):
        self.__connection.delete_object(self.name, name)

    def delete(self):
        self.__connection.delete_container(self.name)
