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
    references = [dict(scan=_graph.get_element(ref['scan']), model=_graph.get_element(ref['model'])) for ref in _compRuleMetricRep.get_reference_ids(_graph.element_from_link(product.default_comparison_rule)) if 'model' in ref and 'scan' in ref]

    all_results = {}

    for ty in model_types:
        scan = [scan for scan in scans if str(scan.model_type) == ty._id]
        if len(scan) > 0:
            scan = scan[0]
            scan_data = [float(_scanMetrValueRep.get(dict(scan=scan, metric=ref['scan']))[0].value) for ref in references]

            lasts_data = []
            for size in [_graph.get_element(s['size']) for s in _compRuleMetricRep.get_size_ids(_graph.element_from_link(product.default_comparison_rule))]:
                model = _modelRep.get(dict(product=product, model_type=ty, size=size))

                last_values = []
                last_ranges = []
                if len(model) > 0:
                    model = model[0]
                    for ref in references:
                        rulemetric = _compRuleMetricRep.get(dict(rule=_graph.element_from_link(product.default_comparison_rule),
                                                                 size=size,
                                                                 scan_metric=ref['scan']))
                        rulemetric = [metr for metr in rulemetric if _graph.element_from_link(_graph.element_from_link(metr.model_metric).model_type) == ty][0]
                        last_ranges.append((rulemetric.f1, rulemetric.shift, rulemetric.f2))
                        last_values.append(float(_modelMetrValueRep.get(dict(model=model, metric=_graph.element_from_link(rulemetric.model_metric)))[0].value))
                lasts_data.append((size.string_value, last_values, last_ranges))
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
