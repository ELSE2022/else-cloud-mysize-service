from pyorient.ogm.property import Boolean
from orientdb_data_layer.data_connection import NodeBase


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


class BaseModel(NodeBase):

    @classproperty
    def query_set(cls):
        return cls.objects.query() if hasattr(cls, 'objects') else None

    @classmethod
    def add(cls, prop_dict, result_as_json=False):
        if not result_as_json:
            return cls.objects.create(**prop_dict)
        return cls.objects.g.client.command(
            "SELECT @this.toJson('rid,version,fetchPlan:*:-1') AS data FROM ({})"
            .format("SELECT * FROM V WHERE @rid = {}"
                    .format(cls.objects.create(**prop_dict)))
        )[0].oRecordData['data'] if hasattr(cls, 'objects') else None

    @classmethod
    def update(cls, elem_id, prop_dict):
        return cls.objects.g.save_element(cls, prop_dict, elem_id)

    @classmethod
    def get(cls, elem_id):
        return cls.objects.g.get_element(elem_id)

    @classmethod
    def delete(cls, elem_id):
        cluster, id = (int(val) for val in elem_id.replace('#', '').split(':'))
        return cls.objects.g.client.record_delete(cluster, id)


class SoftDeleteModel(BaseModel):

    is_delete = Boolean(default=True)

    @classproperty
    def query_set(cls):
        return cls.objects.query().filter(cls.is_delete.__eq__(False)) if hasattr(cls, 'objects') else None

    @classmethod
    def add(cls, prop_dict, result_as_json=False):
        props = {**prop_dict, **dict(is_delete=False)}
        if not result_as_json:
            return cls.objects.create(**props)
        return cls.objects.g.client.command(
            'SELECT @this.toJson("rid,version,fetchPlan:*:-1") AS data FROM ({})'
                .format('SELECT * FROM V WHERE @rid = {}'
                        .format(cls.objects.create(**props)))
        )[0].oRecordData['data'] if hasattr(cls, 'objects') else None

    @classmethod
    def get(cls, elem_id):
        query_dict = {'rid': elem_id}
        return cls.query_set.filter_by(**query_dict).one()

    @classmethod
    def delete(cls, elem_id):
        return cls.update(elem_id, dict(is_delete=True))


BaseNode = NodeBase
