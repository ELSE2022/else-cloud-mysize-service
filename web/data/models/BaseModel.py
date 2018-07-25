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
    """
    Base model class. Contains logic for working with query sets

    Class properties
    ----------------
    query_set(cls)
        Get query with all objects

    Class methods
    -------------
    add(cls, prop_dict, result_as_json=False)
        Create object with prop_dict data
    update(cls, elem_id, prop_dict)
        Update object by ID
    get(cls, elem_id)
        Get object by ID
    delete(cls, elem_id)
        Delete object by ID
    """

    @classproperty
    def query_set(cls):
        """
        Return query object fro class model

        Returns
        -------
        pyorient.ogm.query.Query
            Query object with all elements form class model
        """
        return cls.objects.query() if hasattr(cls, 'objects') else None

    @classmethod
    def add(cls, prop_dict, result_as_json=False):
        """
        Create class model with data from prop_dict

        Parameters
        ----------
        prop_dict: dict
            Dict with data which should be in created object
        result_as_json: bool
            If true, result will be returned as dict

        Returns
        -------
        Class model if result_as_json is false, else dict
        """
        if not result_as_json:
            return cls.objects.create(**prop_dict)
        return cls.objects.g.client.command(
            "SELECT @this.toJson('rid,version,fetchPlan:*:-1') AS data FROM ({})"
            .format("SELECT * FROM V WHERE @rid = {}"
                    .format(cls.objects.create(**prop_dict)))
        )[0].oRecordData['data'] if hasattr(cls, 'objects') else None

    @classmethod
    def update(cls, elem_id, prop_dict):
        """
        Update object

        Parameters
        ----------
        elem_id: str
            ID of element which should be updated
        prop_dict: dict
            Data which should be updated

        Returns
        -------
        False
        """
        return cls.objects.g.save_element(cls, prop_dict, elem_id)

    @classmethod
    def get(cls, elem_id):
        """
        Get element by ID

        Parameters
        ----------
        elem_id: str
            ID of element

        Returns
        -------
        Class model object
        """
        return cls.objects.g.get_element(elem_id)

    @classmethod
    def delete(cls, elem_id):
        """
        Delete element by ID

        Parameters
        ----------
        elem_id: str
            ID of element

        Returns
        -------
        int
        """
        cluster, id = (int(val) for val in elem_id.replace('#', '').split(':'))
        return cls.objects.g.client.record_delete(cluster, id)


class SoftDeleteModel(BaseModel):
    """
    Base model class with soft delete. Contains logic for working with query sets

    Properties
    ----------
    is_delete: pyorient.ogm.property.Boolean
        Is object deleted

    Class properties
    ----------------
    query_set(cls)
        Get query with all objects

    Class methods
    -------------
    add(cls, prop_dict, result_as_json=False)
        Create object with prop_dict data
    get(cls, elem_id)
        Get object by ID
    delete(cls, elem_id)
        Delete object by ID
    """
    is_delete = Boolean(default=True)

    @classproperty
    def query_set(cls):
        """
        Return query object fro class model

        Returns
        -------
        pyorient.ogm.query.Query
            Query object with all elements form class model
        """
        return cls.objects.query().filter(cls.is_delete.__eq__(False)) if hasattr(cls, 'objects') else None

    @classmethod
    def add(cls, prop_dict, result_as_json=False):
        """
        Create class model with data from prop_dict

        Parameters
        ----------
        prop_dict: dict
            Dict with data which should be in created object
        result_as_json: bool
            If true, result will be returned as dict

        Returns
        -------
        Class model if result_as_json is false, else dict
        """
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
        """
        Get element by ID

        Parameters
        ----------
        elem_id: str
            ID of element

        Returns
        -------
        Class model object
        """
        query_dict = {'rid': elem_id}
        return cls.query_set.filter_by(**query_dict).one()

    @classmethod
    def delete(cls, elem_id):
        """
        Delete element by ID

        Parameters
        ----------
        elem_id: str
            ID of element

        Returns
        -------
        int
        """
        return cls.update(elem_id, dict(is_delete=True))


BaseNode = NodeBase
