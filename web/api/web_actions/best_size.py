import logging
from flask import Blueprint, jsonify, request, abort
from ..authentication import requires_auth
from data.repositories import ProductRepository, UserRepository, UserSizeRepository, ScanRepository, ComparisonRuleMetricRepository, ScanMetricValueRepository, ModelMetricValueRepository
from data.repositories import ComparisonResultRepository
from data.repositories import SizeRepository
from orientdb_data_layer import data_connection
from calculations.fitting_algorithms.get_metrics_by_sizes import get_metrics_by_sizes

logger = logging.getLogger(__name__)
_productRep = ProductRepository()
_userRep = UserRepository()
_userSizeRep = UserSizeRepository()
_sizeRep = SizeRepository()
_scanRep = ScanRepository()
_compRuleMetricRep = ComparisonRuleMetricRepository()
_scanMetrValueRep = ScanMetricValueRepository()
_modelMetrValueRep = ModelMetricValueRepository()
_comparisonResRep = ComparisonResultRepository()


def get_foot_best_size(product, model_types, scans):
    _graph = data_connection.get_graph()
    rule = _graph.element_from_link(product.default_comparison_rule)
    print('get foot best size')
    all_results = {}
    comparison_results = []
    print(model_types)
    for ty in model_types:
        references = [dict(scan=_graph.get_element(ref['scan']), model=_graph.get_element(ref['model']))
                      for ref in _compRuleMetricRep.get_distinct_reference_ids(rule.name, product.uuid, ty)]

        scan = [scan for scan in scans if str(scan.model_type) == ty._id]
        print('qqqqs')
        print(scans)
        if len(references) > 0 and len(scan) > 0:
            print('ssss')
            scan = scan[0]
            scan_data = [float(_scanMetrValueRep.get(dict(scan=scan, metric=ref['scan']))[0].value) for ref in references]
            print(scan_data)
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
            metrics = get_metrics_by_sizes(scan_data, lasts_data)
            all_results[ty.name] = metrics
            for res in metrics:
                size_obj = _sizeRep.get({'string_value': res[0]})
                comparison_results.append(_comparisonResRep.add({'scan': scan,
                                                                 'model_type': ty,
                                                                 'size': size_obj[0],
                                                                 'value': res[1]}))
            print(all_results[ty.name])

    return comparison_results


def generate_result(data, user_size=None):
    sizes = []
    avg_result = []
    count_typ = 0
    print(data)
    for typ in data:
        for size in data[typ]:
            if size[0] not in sizes:
                sizes.append(size[0])
                avg_result.append(size[1])
            else:
                idx = sizes.index(size[0])
                avg_result[idx] += size[1]
        count_typ += 1
    avg_result = [val / count_typ for val in avg_result]

    max_val = max(avg_result)
    max_idx = avg_result.index(max_val)

    def result(i):
        if i < len(avg_result):
            return {
            'score': round(avg_result[i], 2),
            'output_model': '',
            'size': sizes[i],
            'size_type': 'FOOT'
            }

    if user_size is None:
        return {
            'prev_best_size': result(max_idx - 1),
            'best_size': result(max_idx),
            'next_best_size': result(max_idx + 1),
        }
    else:
        return {
            'best_style': result(sizes.index(user_size.string_value))
        }



best_size_action = Blueprint('best_size_action', __name__)


@best_size_action.route('/fitting/best_size')
@requires_auth
def best_size():
    _graph = data_connection.get_graph()

    product_uuid = request.args.get('product')

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

    result = get_foot_best_size(product, model_types, scans)

    return jsonify(generate_result(result))

best_style_action = Blueprint('best_style_action', __name__)


@best_style_action.route('/fitting/best_style')
@requires_auth
def get_best_size_metric_by_size():
    _graph = data_connection.get_graph()

    product_uuid = request.args.get('product')

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

    user_size = _userSizeRep.get(dict(user=user))

    size = None
    for s in user_size:
        _size = _graph.element_from_link(s.size)
        if _graph.elements_from_links(_size.model_types) == model_types:
            size = _size
    if size is None:
        abort(404, 'user\'s size not found')

    scans = []
    for ty in model_types:
        scans += _scanRep.get(dict(user=user, is_default=True, model_type=ty))

    result = get_foot_best_size(product, model_types, scans)

    return jsonify(generate_result(result, size))
