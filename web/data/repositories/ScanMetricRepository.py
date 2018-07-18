from data.models.ScanMetric import ScanMetric
from orientdb_data_layer.data import RepositoryBase
from data.utils.string_processor import normalize_string


class DuplicatedScanMetric(Exception):

    def __init__(self, scanner_model, name):
        super().__init__(f'Metric with name {name} for scanner model {scanner_model} is exist')


class ScanMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScanMetric)

    def add(self, metric_dict, result_JSON= False):
        """
        Create scan metric object

        Parameters
        ----------
        metric_dict: dict
            Scan metric model data
        result_JSON: bool
            If True result will be returned as JSON

        Returns
        -------
        Created object
        """
        normalized_name = normalize_string(metric_dict.get('name'))
        scanner_model = metric_dict.get('scanner_model')
        if self.get_by_name_and_scanner_model(scanner_model, normalized_name):
            raise DuplicatedScanMetric(scanner_model, metric_dict.get('name', ''))
        processed_dict = dict(processed_name=normalized_name)
        return super(ScanMetricRepository, self).add({**metric_dict, **processed_dict, }, result_JSON=result_JSON)

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

        return super(ScanMetricRepository, self).update(
            query_dict,
            {**metric_dict, **processed_dict, }
        )

    def get_by_name_and_scanner_model(self, scanner_model, metric_name):
        """
        Return object by scanner model and metric name

        Parameters
        ----------
        scanner_model: data.models.ScannerModel.ScannerModel
            Scanner model object
        metric_name: str
            Name of metric

        Returns
        -------
        data.models.ScanMetric.ScanMetric
        """
        metric = super(ScanMetricRepository, self).get(
            dict(
                processed_name=normalize_string(metric_name),
                scanner_model=scanner_model,
            )
        )
        return metric[0] if metric else None
