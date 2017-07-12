from data.data_connection import get_graph, is_connected as is_data_connected


class RepositoryBase(object):

    __model_type = None
    __graph = None
    __broker = None

    def is_connected(self):
        if is_data_connected():
            if self.__graph is None or self.__broker is None:
                self.__graph = get_graph()
                if hasattr(self.__model_type, 'element_plural'):
                    self.__broker = getattr(self.__graph, self.__model_type.element_plural)
                elif hasattr(self.__model_type, 'label'):
                    self.__broker = getattr(self.__graph, self.__model_type.label)
            return self.__graph is not None and self.__broker is not None
        return False

    def __init__(self, model_type):
        self.__model_type = model_type

    def add(self, prop_dict):
        """
        add record by properties dict
        :param prop_dict: dictionary of values for properties updating (OUT OF TYPE will be ignored)
        :return: created MODEL OBJECT)
        """
        if self.__broker:
            return self.__broker.create(**prop_dict)

    def get(self, query_dict):
        """
        get records by query dict
        :param query_dict: dictionary of values for records searching
        :return: list of MODEL OBJECTS
        """
        if self.is_connected():
            return [obj for obj in self.__broker.query(**query_dict)]

    def update(self, query_dict, prop_dict):
        """
        update records in database
        Example:
        update(dict(name='test2', id=1), dict(name= 'test3')
        will update all records with name = 'test2' and id =1, and set value of name = 'test3'

        :param query_dict: dictionary of values for records searching
        :param prop_dict: dictionary of values for properties updating (OUT OF TYPE will be ignored)
        :return: list of updated orient records
        """
        if self.is_connected():
            result = []
            for rec in self.__broker.query(**query_dict):
                for key in prop_dict:
                    setattr(rec, key, prop_dict[key])
                cluster, id = (int(val) for val in rec._id.replace('#', '').split(':'))
                result.append(self.__graph.client.record_update(cluster, id, rec._props))
            return result

    def delete(self, query_dict):
        if self.is_connected():
            result = []
            for rec in self.__broker.query(**query_dict):
                cluster, id = (int(val) for val in rec._id.replace('#', '').split(':'))
                result.append(self.__graph.client.record_delete(cluster, id))
            return result.count(True)

    def pure_sql_query(self, sqlquery):
        """
        Call direct SQL query
        :param sqlquery: query string
        :return: list of orient records
        """
        if self.is_connected():
            return self.__graph.client.query(sqlquery)