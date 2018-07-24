from data.models.ModelTypeMetric import ModelTypeMetric
from .BaseRepository import BaseRepository
from data.utils.string_processor import normalize_string


class DuplicatedModelTypeMetric(Exception):

    def __init__(self, scanner_model, name):
        super().__init__(f'Metric with name {name} for scanner model {scanner_model} is exist')


class ModelTypeMetricRepository(BaseRepository):

    def __init__(self):
        super().__init__(ModelTypeMetric)

    def add(self, metric_dict, result_JSON= False):
        """
        Create model type metric object

        Parameters
        ----------
        metric_dict: dict
            Model type metric data
        result_JSON: bool
            If True result will be returned as JSON

        Returns
        -------
        Created object
        """
        normalized_name = normalize_string(metric_dict.get('name'))
        model_type = metric_dict.get('model_type')
        if self.get_by_name_and_scanner_model(model_type, normalized_name):
            raise DuplicatedModelTypeMetric(model_type, metric_dict.get('name', ''))
        processed_dict = dict(processed_name=normalized_name)
        return super(ModelTypeMetricRepository, self).add({**metric_dict, **processed_dict, }, result_JSON=result_JSON)

    def update(self, query_dict, metric_dict):
        """
        Update scan metric object

        Parameters
        ----------
        query_dict: dict
            Scan metric query data
        metric_dict: dict
            Data which should be changed in filtered objects

        Returns
        -------
        Updated object
        """
        processed_dict = dict()
        if 'name' in metric_dict:
            processed_dict.update(processed_name=normalize_string(metric_dict.get('name')))

        return super(ModelTypeMetricRepository, self).update(
            query_dict,
            {**metric_dict, **processed_dict, }
        )

    def get_by_name_and_scanner_model(self, model_type, metric_name):
        """
        Return object by model type and metric name

        Parameters
        ----------
        model_type: data.models.ModelType.ModelType
            Model type object
        metric_name: str
            Name of metric

        Returns
        -------
        data.models.ModelTypeMetric.ModelTypeMetric
        """
        metric = super(ModelTypeMetricRepository, self).get(
            dict(
                processed_name=normalize_string(metric_name),
                model_type=model_type,
            )
        )
        return metric[0] if metric else None
