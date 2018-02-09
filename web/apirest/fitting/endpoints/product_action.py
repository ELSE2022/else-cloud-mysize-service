import base64
import csv

from apirest.fitting.serializers import product
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
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
from data.models import Product
from flask import request
from flask import Response
from flask import abort
from flask_restplus import Resource
from orientdb_data_layer import data_connection
from pyorient import OrientRecordLink

ns = api.namespace('fitting_products', path='/fitting/products', description='Operations related to Product')

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

msg_object_does_not_exist = '{} object with id "{}" not found'


def add_comp_rule_metric(modeltype_metr, scan_metric, value, f1, shift, f2, product_obj, model_type_obj, size_obj):
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


@ns.route('',)
class Products(Resource, ListModelMixin):
    model = Product
    serializer = product

    def get(self):
        return super().get()

    @api.expect(product)
    def post(self):
        """
        Api method to create product.
        """
        print('POST')
        print(request.json)
        brand_obj = _brandRep.get({'@rid': request.json['brand']})
        if not brand_obj:
            abort(400, msg_object_does_not_exist.format('Brand', request.json['brand']))

        rule_obj = _compRuleRep.get({'@rid': request.json['default_comparison_rule']})
        if not rule_obj:
            abort(400, msg_object_does_not_exist.format('ComparisonRule', request.json['default_comparison_rule']))

        data_dict = request.json
        data_dict['brand'] = brand_obj[0]
        data_dict['default_comparison_rule'] = rule_obj[0]
        product_obj = _productRep.add(data_dict, result_JSON=True)
        return product_obj


@ns.route('/<string:uuid>')
@api.response(404, 'Product not found.')
class ProductGetMetricsItem(Resource):
    @api.response(204, 'Product successfully deleted.')
    @api.marshal_with(product)
    def delete(self, uuid):
        """
        Api method to delete product.
        """
        _productRep.delete({'uuid': uuid})
        return None, 204

    @api.expect(product)
    def put(self, uuid):
        """
        Api method to update product.
        """
        _graph = data_connection.get_graph()
        if request.json.get('files'):
            filecodestring = request.json['files'][0]['src']
            data = base64.b64decode(filecodestring.split(',')[1])

            iter_lines = [s.strip().decode('utf-8') for s in data.splitlines()]

            reader = csv.reader(iter_lines, delimiter=',')

            product_obj = _productRep.get({'@rid': uuid})[0]
            foot_types = _graph.element_from_link(product_obj.default_comparison_rule).model_types
            model_type_objects = []
            for t in foot_types:
                model_type_objects.append(_graph.element_from_link(t))
            header = next(reader)
            for i in reader:
                count = 0
                for foot_type in foot_types:
                    size_obj = _sizeRep.get({'model_types': model_type_objects, 'string_value': i[0]})
                    if not size_obj:
                        size_obj = _sizeRep.add({'model_types': model_type_objects, 'string_value': i[0]})
                    else:
                        size_obj = size_obj[0]
                    comp_rule_metric = add_comp_rule_metric(i[1], i[2], i[3], i[4+count], i[5+count], i[6+count],
                                                            product_obj, foot_type, size_obj)
                    count += 3

        data_dict = request.json
        data_dict['brand'] = OrientRecordLink(request.json['brand'])
        data_dict['default_comparison_rule'] = OrientRecordLink(request.json['default_comparison_rule'])

        product_obj = _productRep.get({'uuid': uuid})
        if not product_obj:
            product_obj = _productRep.update({'@rid': uuid}, data_dict)
        else:
            product_obj = _productRep.update({'uuid': uuid}, data_dict)
        if product_obj: product_obj = product_obj[0]
        return {'@rid': product_obj._id, 'name': product_obj.name}, 201


@ns.route('/<string:uuid>/get_metrics')
@api.response(404, 'Product not found.')
class ProductGetMetricsItem(Resource):
    def get(self, uuid):
        """
        Returns a csv file.
        """
        _graph = data_connection.get_graph()

        data = []
        product_obj = _productRep.get({'uuid': uuid})[0]
        model_type_obj = _modelTypeRep.get({'name': 'LEFT_FOOT'})[0]
        model_type_r_obj = _modelTypeRep.get({'name': 'RIGHT_FOOT'})[0]
        model_objects = _modelRep.get({'product': product_obj, 'model_type': model_type_obj})
        for m in model_objects:
            comp_rule_metric = _compRuleMetricRep.get({'rule': product_obj.default_comparison_rule, 'model': m})
            size_obj = _sizeRep.get({'@rid': m.size})[0]
            right_model_obj = _modelRep.get({'product': product_obj, 'model_type': model_type_r_obj, 'size': size_obj})
            for rule_metric in comp_rule_metric:
                model_metric_value_obj = _modelMetricValueRep.get({'model': m, 'metric': rule_metric.model_metric})
                rule_metric_r = _compRuleMetricRep.get_by_tree({'rule': product_obj.default_comparison_rule,
                                                                'model': right_model_obj[0],
                                                                'model_metric': {'name': _graph.element_from_link(rule_metric.model_metric).name, 'model_type': model_type_r_obj},
                                                                'scan_metric': rule_metric.scan_metric})
                rule_metric_r = rule_metric_r[0]

                data.append("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(_graph.element_from_link(m.size).string_value,
                                                                              _graph.element_from_link(rule_metric.model_metric).name,
                                                                              _graph.element_from_link(rule_metric.scan_metric).name,
                                                                              model_metric_value_obj[0].value,
                                                                              rule_metric.f1, rule_metric.shift, rule_metric.f2,
                                                                              rule_metric_r.f1, rule_metric_r.shift, rule_metric_r.f2))

        return Response(data,
                        mimetype='text/csv',
                        headers={"Content-disposition": "attachment; filename=Footcsv.csv"}
                        )
