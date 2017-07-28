import logging
from flask import Blueprint, jsonify, request, abort
from ..authentication import requires_auth
from data.repositories import ProductRepository, UserRepository, ScanRepository, ModelRepository, ComparisonRuleMetricRepository, ScanMetricValueRepository, ModelMetricValueRepository
from data import data_connection
from calculations.fitting_algorithms.get_metrics_by_sizes import get_metrics_by_sizes

logger = logging.getLogger(__name__)
_productRep = ProductRepository()
_userRep = UserRepository()
_scanRep = ScanRepository()
_modelRep = ModelRepository()
_compRuleMetricRep = ComparisonRuleMetricRepository()
_scanMetrValueRep = ScanMetricValueRepository()
_modelMetrValueRep = ModelMetricValueRepository()


def get_foot_best_size(product, model_types, scans):
    _graph = data_connection.get_graph()
    rule = _graph.element_from_link(product.default_comparison_rule)

    all_results = {}

    for ty in model_types:
        references = [dict(scan=_graph.get_element(ref['scan']), model=_graph.get_element(ref['model']))
                      for ref in _compRuleMetricRep.get_distinct_reference_ids(rule.name, product.uuid, ty)]

        scan = [scan for scan in scans if str(scan.model_type) == ty._id]
        if len(references) > 0 and len(scan) > 0:
            scan = scan[0]
            scan_data = [float(_scanMetrValueRep.get(dict(scan=scan, metric=ref['scan']))[0].value) for ref in references]

            lasts_data = []
            config = _compRuleMetricRep.get_config_by_product(rule.name, product.uuid, ty)
            values = _modelMetrValueRep.get_values_for_comparison(_graph.element_from_link(product.default_comparison_rule).name, product.uuid, ty)

            last_values = []
            last_ranges = []
            curr_size = ''
            for val in zip(values, config):
                if curr_size == '':
                    curr_size = val[0]['size']
                elif val[0]['size'] != curr_size:
                    lasts_data.append((curr_size, last_values, last_ranges))
                    last_values = []
                    last_ranges = []
                    curr_size = val[0]['size']
                last_values.append(float(val[0]['value']))
                last_ranges.append((val[1]['f1'], val[1]['shift'], val[1]['f2']))
            lasts_data.append((curr_size, last_values, last_ranges))

            all_results[ty.name] = get_metrics_by_sizes(scan_data, lasts_data)

    return all_results

best_size_action = Blueprint('best_size_action', __name__)


@best_size_action.route('/fitting/best_size')
@requires_auth
def best_size():
    _graph = data_connection.get_graph()

    product_uuid = request.args.get('product_id')

    product = _productRep.get(dict(uuid=product_uuid))
    if len(product) == 0:
        abort(404, 'product not found')
    else:
        product = product[0]

    user_uuid = request.args.get('user')
    user = _userRep.get(dict(uuid=user_uuid))
    if len(user) == 0:
        abort(404, 'user not found')
    else:
        user = user[0]

    model_types = _graph.elements_from_links(_graph.element_from_link(product.default_comparison_rule).model_types)

    scans = []
    for ty in model_types:
        scans += _scanRep.get(dict(user=user, is_default=True, model_type=ty))

    return jsonify(get_foot_best_size(product, model_types, scans))
