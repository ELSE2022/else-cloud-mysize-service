from data.models.ModelMetricValue import ModelMetricValue
from orientdb_data_layer.data import RepositoryBase


class ModelMetricValueRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelMetricValue)

    def get_values_for_comparison(self, rule_name, product_uuid, model_type):
        return self.sql_command("select model.size.order as order, model.size.string_value as size, metric.name as metric, value\
                                    from modelmetricvalue\
                                    where metric in (select model_metric from comparisonrulemetric\
                                                     where rule.name = '{0}'\
                                                      and model.product.uuid = '{1}'\
                                                      and model.model_type = {2})\
                                    and model.product.uuid = '{1}'\
                                    order by order, metric".format(rule_name, product_uuid, model_type._id), result_as_dict=True)
