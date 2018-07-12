from data.models.ModelTypeMetric import ModelTypeMetric
from orientdb_data_layer.data import RepositoryBase
from data.utils.string_processor import normalize_string


class DuplicatedModelTypeMetric(Exception):

    def __init__(self, scanner_model, name):
        super().__init__(f'Metric with name {name} for scanner model {scanner_model} is exist')


class ModelTypeMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelTypeMetric)

    def add(self, metric_dict, result_JSON= False):
        normalized_name = normalize_string(metric_dict.get('name'))
        model_type = metric_dict.get('model_type')
        if self.get_by_name_and_scanner_model(model_type, normalized_name):
            raise DuplicatedModelTypeMetric(model_type, metric_dict.get('name', ''))
        processed_dict = dict(processed_name=normalized_name)
        return super(ModelTypeMetricRepository, self).add({**metric_dict, **processed_dict, }, result_JSON=result_JSON)

    def update(self, query_dict, metric_dict):
        processed_dict = dict()
        if 'name' in metric_dict:
            processed_dict.update(processed_name=normalize_string(metric_dict.get('name')))

        return super(ModelTypeMetricRepository, self).update(
            query_dict,
            {**metric_dict, **processed_dict, }
        )

    def get_by_name_and_scanner_model(self, model_type, metric_name):
        return super(ModelTypeMetricRepository, self).get(
            dict(
                processed_name=normalize_string(metric_name),
                model_type=model_type,
            )
        )
