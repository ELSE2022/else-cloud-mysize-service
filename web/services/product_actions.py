import base64
import tempfile
import petl
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
    def add_comp_rule_metric(cls, modeltype_metr, scan_metric, value, f1, shift, f2, product_obj, model_type_obj,
                             size_obj):
        model_obj = _modelRep.get({'product': product_obj, 'model_type': model_type_obj, 'size': size_obj})
        if not model_obj:
            model_obj = _modelRep.add({'product': product_obj, 'model_type': model_type_obj, 'size': size_obj})
        else:
            model_obj = model_obj[0]

        scanner_model_obj = _scannerModelRep.get({})

        modeltype_metric_obj = _modelTypeMetricRep.get({'model_type': model_type_obj, 'name': modeltype_metr})
        if not modeltype_metric_obj:
            modeltype_metric_obj = _modelTypeMetricRep.add({'model_type': model_type_obj, 'name': modeltype_metr})
        else:
            modeltype_metric_obj = modeltype_metric_obj[0]

        model_metric_value_obj = _modelMetricValueRep.get({'model': model_obj, 'metric': modeltype_metric_obj})
        if not model_metric_value_obj:
            _modelMetricValueRep.add({'model': model_obj, 'metric': modeltype_metric_obj, 'value': value})
        else:
            _modelMetricValueRep.update({'model': model_obj, 'metric': modeltype_metric_obj}, {'value': value})

        scan_metric_obj = _scanMetricRep.get({'name': scan_metric})
        if not scan_metric_obj:
            scan_metric_obj = _scanMetricRep.add({'scanner_model': scanner_model_obj[0], 'name': scan_metric})
        else:
            scan_metric_obj = scan_metric_obj[0]

        comp_rule_metr_obj = _compRuleMetricRep.get({'model': model_obj,
                                                     'model_metric': modeltype_metric_obj,
                                                     'scan_metric': scan_metric_obj})
        if not comp_rule_metr_obj:
            comp_rule_metr_obj = _compRuleMetricRep.add({'model': model_obj,
                                                         'model_metric': modeltype_metric_obj,
                                                         'scan_metric': scan_metric_obj,
                                                         'rule': product_obj.default_comparison_rule})
        comp_rule_metr_obj = _compRuleMetricRep.update({'model': model_obj,
                                                        'model_metric': modeltype_metric_obj,
                                                        'scan_metric': scan_metric_obj},
                                                       {'f1': f1, 'shift': shift, 'f2': f2})

        return comp_rule_metr_obj

    @classmethod
    def update_product(cls, product_id, product_data):
        _graph = data_connection.get_graph()

        if 'files' in product_data:
            filecodestring = product_data['files'][0]['src']
            data = base64.b64decode(filecodestring.split(',')[1])
            file = tempfile.NamedTemporaryFile()
            file.write(data)
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
                'size_metric',
            )
            table_creator = functoolz.compose(
                lambda tbl: petl.convert(tbl, float_columns, float),
                lambda tbl: petl.convert(tbl, str_columns, 'strip'),
                partial(petl.setheader, header=str_columns + float_columns),
                partial(petl.fromcsv, delimiter=','),
            )
            table = table_creator(file.name)
            for i in table:
                print(i)
            #
            # product_obj = _productRep.get({'@rid': id})[0]
            # foot_types = _graph.element_from_link(product_obj.default_comparison_rule).model_types
            # model_type_objects = []
            # for t in foot_types:
            #     model_type_objects.append(_graph.element_from_link(t))
            # next(reader)
            # for i in reader:
            #     count = 0
            #     for foot_type in foot_types:
            #         size_obj = _sizeRep.get({'model_types': model_type_objects, 'string_value': i[0].strip()})
            #         if not size_obj:
            #             size_obj = _sizeRep.add({'model_types': model_type_objects, 'string_value': i[0].strip()})
            #         else:
            #             size_obj = size_obj[0]
            #         add_comp_rule_metric(
            #             i[1].strip(),
            #             i[2].strip(),
            #             i[3].strip(),
            #             i[4 + count].strip(),
            #             i[5 + count].strip(),
            #             i[6 + count].strip(),
            #             product_obj,
            #             foot_type,
            #             size_obj
            #         )
            #         count += 3

        data_dict = product_data
        data_dict['brand'] = OrientRecordLink(product_data['brand'])
        data_dict['default_comparison_rule'] = OrientRecordLink(product_data['default_comparison_rule'])

        product_obj = _productRep.get({'uuid': product_id})
        if not product_obj:
            product_obj = _productRep.update({'@rid': product_id}, data_dict)
        else:
            product_obj = _productRep.update({'uuid': product_id}, data_dict)
        if product_obj:
            product_obj = product_obj[0]
        print(product_obj)
        return {'@rid': product_obj._id, 'name': product_obj.name}
