from data.models.ComparisonRuleMetric import ComparisonRuleMetric
from orientdb_data_layer.data import RepositoryBase


class ComparisonRuleMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ComparisonRuleMetric)

    def get_distinct_reference_ids(self, rule_name, product_uuid, model_type):
        return self.sql_command("select distinct(scan_metric.@rid) as scan, distinct(model_metric.@rid) as model\
                                  from comparisonrulemetric\
                                  where rule.name = '{0}'\
                                  and model.product.uuid = '{1}'\
                                  and model.model_type = {2}".format(rule_name, product_uuid, model_type._id), result_as_dict=True)

    def get_config_by_product(self, rule_name, product_uuid, model_type):
        return self.sql_command("select model.size.order as order, model.size.string_value as size, model_metric.name as metric, f1, shift, f2\
                                 from comparisonrulemetric\
                                  where rule.name = '{0}'\
                                  and model.product.uuid = '{1}'\
                                   and model.model_type = {2}\
                                   order by order, metric".format(rule_name, product_uuid, model_type._id), result_as_dict=True)
