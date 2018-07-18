from pyorient import OrientRecordLink

from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from data.repositories import ComparisonRuleMetricRepository
from data.repositories import ModelTypeMetricRepository
from data.repositories import ScanMetricRepository
from data.repositories import ScannerModelRepository
from data.repositories import ModelMetricValueRepository
from data.repositories import ComparisonResultRepository

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()
_compRuleMetricRep = ComparisonRuleMetricRepository()
_modelTypeMetricRep = ModelTypeMetricRepository()
_scanMetricRep = ScanMetricRepository()
_scannerModelRep = ScannerModelRepository()
_modelMetricValueRep = ModelMetricValueRepository()
_comparisonResultRep = ComparisonResultRepository()


class ProductActionsService:
    """
    Service for actions with product model

    Methods
    -------
    add_comp_rule_metric(cls, product_obj, size, scan_metric, value, modeltype_metric, f1, shift, f2)
        Update or create comparision rule metric
    get_model_type_metrics(cls, model_types, metric_name)
        Return model types for metric
    divide_table(cls, fields, side_fields, tbl, suffix)
        Divide table
    update_product(cls, product_id, product_data)
        Update product by id
    """

    @classmethod
    def add_comp_rule_metric(cls, product_obj, size, scan_metric, value, modeltype_metric, f1, shift, f2):
        """
        Update or create comparision rule metric

        Parameters
        ----------
        product_obj: data.models.Product.Product
            Entity of product model
        size: data.models.Size.Size
            Entity of size model
        scan_metric: data.models.ScanMetric.ScanMetric
            Entity of scan metric model
        value: str
            Value of comparision rule metric
        modeltype_metric: data.models.ModelTypeMetric.ModelTypeMetric
            Entity of model type metric model
        f1: float
        shift: float
        f2: float

        Returns
        -------
        comp_rule_metr_obj: data.models.ComparisionRuleMetric.ComparisionRuleMetric
        """
        model_type_obj = modeltype_metric.model_type
        model_obj = _modelRep.get({'product': product_obj, 'model_type': model_type_obj, 'size': size})
        if not model_obj:
            model_obj = _modelRep.add({'product': product_obj, 'model_type': model_type_obj, 'size': size})
        else:
            model_obj = model_obj[0]

        model_metric_value_obj = _modelMetricValueRep.get({'model': model_obj, 'metric': modeltype_metric})
        if not model_metric_value_obj:
            _modelMetricValueRep.add({'model': model_obj, 'metric': modeltype_metric, 'value': value})
        else:
            _modelMetricValueRep.update({'model': model_obj, 'metric': modeltype_metric}, {'value': value})

        comp_rule_metr_obj = _compRuleMetricRep.get({'model': model_obj,
                                                     'model_metric': modeltype_metric,
                                                     'scan_metric': scan_metric})
        if not comp_rule_metr_obj:
            _compRuleMetricRep.add({'model': model_obj,
                                 'model_metric': modeltype_metric,
                                 'scan_metric': scan_metric,
                                 'rule': product_obj.default_comparison_rule})
        comp_rule_metr_obj = _compRuleMetricRep.update({'model': model_obj,
                                                        'model_metric': modeltype_metric,
                                                        'scan_metric': scan_metric},
                                                       {'f1': f1, 'shift': shift, 'f2': f2})

        _comparisonResultRep.delete(dict(model=model_obj))
        return comp_rule_metr_obj

    @classmethod
    def update_product(cls, product_id, product_data, metrics_data):
        """
        Update product by rid

        Parameters
        ----------
        product_id: str
            Record id in orient data base or product uuid
        product_data: dict
            Product data which should be saved

        Returns
        -------
        product_obj: dict
            Updated product
        """
        product_obj = _productRep.get({'@rid': product_id})[0]
        for metric_data in metrics_data:
            cls.add_comp_rule_metric(product_obj, *metric_data)
        product_data['brand'] = OrientRecordLink(product_data['brand'])
        product_data['default_comparison_rule'] = OrientRecordLink(product_data['default_comparison_rule'])

        product_obj = _productRep.get({'uuid': product_id})
        if not product_obj:
            product_obj = _productRep.update({'@rid': product_id}, product_data)
        else:
            product_obj = _productRep.update({'uuid': product_id}, product_data)
        if product_obj:
            product_obj = product_obj[0]
        return {'@rid': product_obj._id, 'name': product_obj.name}
