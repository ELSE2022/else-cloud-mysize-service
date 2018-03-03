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

    @classmethod
    def add(cls, prop_dict, result_as_json=False):
        if not result_as_json:
            return cls.objects.create(**prop_dict)
        return cls.objects.g.client.command(
                    "SELECT @this.toJson('rid,version,fetchPlan:*:-1') AS data FROM ({})".format("SELECT * FROM V WHERE @rid = {}"
                                        .format(cls.objects.create(**prop_dict)))
                )[0].oRecordData['data'] if hasattr(cls, 'objects') else None

    @classmethod
    def update(cls, elem_id, prop_dict):
        return cls.objects.g.save_element(cls, prop_dict, elem_id)

BaseNode = data_connection.NodeBase
