from data.models.ScanMetric import ScanMetric
from orientdb_data_layer.data import RepositoryBase
from data.utils.string_processor import normalize_string


class ScanMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScanMetric)

    def add(self, metric_dict, result_JSON= False):
        processed_dict = dict(processed_name=normalize_string(metric_dict.get('name')))
        return super(ScanMetricRepository, self).add({**metric_dict, **processed_dict, }, result_JSON=result_JSON)

    def update(self, query_dict, metric_dict):
        processed_dict = dict()
        if 'name' in metric_dict:
            processed_dict.update(processed_name=normalize_string(metric_dict.get('name')))

        return super(ScanMetricRepository, self).update(
            query_dict,
            {**metric_dict, **processed_dict, }
        )

    def get_by_name(self, metric_name):
        return super(ScanMetricRepository, self).get(dict(processed_name=normalize_string(metric_name)))
