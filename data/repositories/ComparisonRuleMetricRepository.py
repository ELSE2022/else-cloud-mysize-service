from data.models.ComparisonRuleMetric import ComparisonRuleMetric
from .base import RepositoryBase


class ComparisonRuleMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ComparisonRuleMetric)

    def get_reference_ids(self, comparison_rule):
        return self.sql_command("select distinct(scan_metric.@rid) as scan, distinct(model_metric.@rid) as model\
                                                from comparisonrulemetric where rule = {0}".format(comparison_rule._id), result_as_dict=True)

    def get_size_ids(self, comparison_rule):
        return self.sql_command("select distinct(size.@rid) as size\
                                                from comparisonrulemetric where rule = {0}".format(comparison_rule._id), result_as_dict=True)