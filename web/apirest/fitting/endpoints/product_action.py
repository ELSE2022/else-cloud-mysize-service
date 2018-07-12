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
from data.models import Model
from data.models import ModelMetricValue
from data.models import ComparisonResult
from data.models import CompareVisualization
from data.models import ComparisonRuleMetric
from flask import request
from flask import Response
from flask import abort
from flask_restplus import Resource
from orientdb_data_layer import data_connection
from services.product_actions import ProductActionsService

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


@ns.route('', )
class Products(Resource, ListModelMixin):
    model = Product
    serializer = product
    filter_field = 'uuid'

    def get(self):
        return super().get()

    @api.expect(product)
    def post(self):
        """
        Api method to create product.
        """
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


@ns.route('/<string:id>')
@api.response(404, 'Product not found.')
class ProductGetMetricsItem(Resource):
    @api.response(204, 'Product successfully deleted.')
    @api.marshal_with(product)
    def delete(self, id):
        """
        Api method to delete product.
        """
        product_obj = Product.get(id)
        if product_obj:
            for m in Model.query_set.filter_by(product=id):
                for RelativeClass in [ModelMetricValue, CompareVisualization, ComparisonResult, ComparisonRuleMetric]:
                    for x in RelativeClass.query_set.filter_by(model=m._id):
                        RelativeClass.delete(x._id)
                Model.delete(m._id)
            Product.delete(product_obj._id)
        return None, 200

    @api.expect(product)
    def put(self, id):
        """
        Api method to update product.
        """
        return ProductActionsService.update_product(id, request.json), 201


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
            size_obj = _sizeRep.get({'@rid': m.size})
            if size_obj:
                size_obj = size_obj[0]
                right_model_obj = _modelRep.get(
                    {'product': product_obj, 'model_type': model_type_r_obj, 'size': size_obj})
                for rule_metric in comp_rule_metric:
                    model_metric_value_obj = _modelMetricValueRep.get({'model': m, 'metric': rule_metric.model_metric})
                    rule_metric_r = _compRuleMetricRep.get_by_tree({
                        'rule': product_obj.default_comparison_rule,
                        'model': right_model_obj[0],
                        'model_metric': {
                            'name': _graph.element_from_link(rule_metric.model_metric).name,
                            'model_type': model_type_r_obj
                        },
                        'scan_metric': rule_metric.scan_metric
                    })
                    rule_metric_r = rule_metric_r[0]

                    data.append(
                        "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(_graph.element_from_link(m.size).string_value,
                                                                          _graph.element_from_link(
                                                                              rule_metric.model_metric).name,
                                                                          _graph.element_from_link(
                                                                              rule_metric.scan_metric).name,
                                                                          model_metric_value_obj[0].value,
                                                                          rule_metric.f1, rule_metric.shift,
                                                                          rule_metric.f2,
                                                                          rule_metric_r.f1, rule_metric_r.shift,
                                                                          rule_metric_r.f2))

        return Response(data,
                        mimetype='text/csv',
                        headers={"Content-disposition": "attachment; filename=Footcsv.csv"}
                        )
