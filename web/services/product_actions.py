import base64
import tempfile
import petl
import operator
import itertools
from toolz import functoolz
from functools import partial

from orientdb_data_layer import data_connection
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


class ProductActionsService:

    @classmethod
    def add_comp_rule_metric(cls, product_obj, size, scan_metric, value, modeltype_metric, f1, shift, f2):
        print(product_obj, size, scan_metric, value, modeltype_metric, f1, shift, f2)
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

        return comp_rule_metr_obj

    @classmethod
    def csv_field_converter(cls, fields, func, tbl):
        return petl.convert(tbl, fields, func)

    @classmethod
    def get_model_type_metrics(cls, model_types, metric_name):
        return tuple(
            map(
                partial(_modelTypeMetricRep.get_by_name_and_scanner_model, metric_name=metric_name),
                model_types,
            )
        )

    @classmethod
    def divide_rows(cls, fields, side_fields, tbl, suffix):
        return petl.cut(tbl, fields + tuple(map(partial(functoolz.flip, operator.add, suffix), side_fields)))

    @classmethod
    def update_product(cls, product_id, product_data):
        _graph = data_connection.get_graph()
        product_obj = _productRep.get({'@rid': product_id})[0]
        if product_obj and 'files' in product_data:
            filecodestring = product_data['files'][0]['src']
            data = base64.b64decode(filecodestring.split(',')[1])
            file = tempfile.NamedTemporaryFile(delete=False)
            file.write(data)
            file.close()
            comparision_rule = _compRuleRep.get({'@rid': product_obj.default_comparison_rule})[0]
            model_types = comparision_rule.model_types
            scanner_model = comparision_rule.scanner_model
            float_columns = (
                'value',
                'f1_l',
                'shift_l',
                'f2_l',
                'f1_r',
                'shift_r',
                'f2_r',
            )
            str_columns = (
                'size',
                'model_metric',
                'scan_metric',
            )
            model_type_objects = list(map(_graph.element_from_link, model_types))
            rows_divider = partial(
                cls.divide_rows,
                ('size', 'scan_metric', 'value',),
                ('model_metric', 'f1', 'shift', 'f2',),
            )
            table_creator = functoolz.compose(
                partial(petl.skip, n=1),
                lambda tbls: petl.stack(*tbls),
                lambda tbl: (rows_divider(tbl, '_l'), rows_divider(tbl, '_r')),
                partial(
                    cls.csv_field_converter,
                    'size',
                    partial(_sizeRep.get_model_types_size, model_type_objects)
                ),
                partial(petl.unpack, field='model_metric', newfields=['model_metric_l', 'model_metric_r']),
                partial(
                    cls.csv_field_converter,
                    'model_metric',
                    partial(cls.get_model_type_metrics, model_types)
                ),
                partial(
                    cls.csv_field_converter,
                    'scan_metric',
                    partial(_scanMetricRep.get_by_name_and_scanner_model, scanner_model)
                ),
                partial(cls.csv_field_converter, float_columns, float),
                partial(cls.csv_field_converter, str_columns, 'strip'),
                partial(petl.setheader, header=str_columns + float_columns),
                partial(petl.fromcsv, delimiter=','),
            )
            list(itertools.starmap(partial(cls.add_comp_rule_metric, product_obj), table_creator(file.name)))

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
