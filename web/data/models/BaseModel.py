from orientdb_data_layer import data_connection


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


class BaseModel:
    
    @classproperty
    def query_set(cls):
    	return cls.objects.query() if hasattr(cls, 'objects') else None


BaseNode = data_connection.NodeBase
