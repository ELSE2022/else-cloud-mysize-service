import logging
import operator
from flask import Blueprint, jsonify, request, abort
from ..authentication import requires_auth
from data.repositories import ProductRepository, UserRepository, UserSizeRepository, ScanRepository, ComparisonRuleMetricRepository, ScanMetricValueRepository, ModelMetricValueRepository
from data.repositories import ComparisonResultRepository
from data.repositories import SizeRepository
from data.repositories import ModelRepository
from orientdb_data_layer import data_connection
from calculations.fitting_algorithms.get_metrics_by_sizes import get_metrics_by_sizes

from data.models import ComparisonRule, Size, Model, \
    ComparisonResult, ComparisonRuleMetric, ScanMetricValue, \
    ModelMetricValue, ModelTypeMetric, ScanMetric

logger = logging.getLogger('rest_api_demo')
_productRep = ProductRepository()
_userRep = UserRepository()
_userSizeRep = UserSizeRepository()
_sizeRep = SizeRepository()
_scanRep = ScanRepository()
_compRuleMetricRep = ComparisonRuleMetricRepository()
_scanMetrValueRep = ScanMetricValueRepository()
_modelMetrValueRep = ModelMetricValueRepository()
_comparisonResRep = ComparisonResultRepository()
_modelResRep = ModelRepository()


def get_compare_result(scan, lasts):
    """
    Calculate result for scan and models

    Parameters
    ----------
    scan: data.models.Scan.Scan
        User scan
    lasts: data.models.Model.Model query
        Models of product

    Returns
    -------
    dict
        Calculations results
    """

    scan_data = []
    lasts_data = []
    for last in lasts:
        lasts_data.append((last, [], []))
    scan_metric_values = ScanMetricValue.query_set.filter_by(scan=scan).all()
    logger.debug('scan_metric_values')
    logger.debug(scan_metric_values)
    for scan_metric_value in scan_metric_values:
        for last_data in lasts_data:
            comparision_rule_metric = ComparisonRuleMetric.query_set.filter_by(
                scan_metric=scan_metric_value.metric,
                model=last_data[0],
            ).first()
            logger.debug(ComparisonRuleMetric.query_set.filter_by(
                scan_metric=scan_metric_value.metric,
                model=last_data[0],
            ))
            logger.debug('comparision_rule_metric')
            logger.debug(comparision_rule_metric)
            if comparision_rule_metric:
                last_metric = ModelMetricValue.query_set.filter_by(
                    metric=comparision_rule_metric.model_metric,
                    model=last_data[0],
                ).first()
                logger.debug(last_metric)
                last_data[1].append(float(last_metric.value))
                last_data[2].append((comparision_rule_metric.f1, comparision_rule_metric.shift, comparision_rule_metric.f2))
            else:
                break
        else:
            scan_data.append(float(scan_metric_value.value))
    logger.debug(scan)
    logger.debug(scan.is_default)
    logger.debug('scan_data')
    logger.debug(scan_data)
    return get_metrics_by_sizes(scan_data, lasts_data)


def get_foot_best_size(product, scans):
    """
    Calculate comparision results for each model for product and scans

    Parameters
    ----------
    product: data.models.Product.Product
        Entity of product model
    scans: data.models.Scan.Scan query
        Query which describe scans

    Returns
    -------
    comparison_results: dict
    """
    comparison_results = []
    for scan in scans:
        lasts = Model.query_set.filter_by(product=product, model_type=scan.model_type)

        results = get_compare_result(scan, lasts)
        for res in results:
            created = ComparisonResult.objects.create(**{'scan': scan,
                                                         'model': res[0],
                                                         'value': res[1]})
            comparison_results.append(created)

    return comparison_results


def generate_result(data, user_size=None):
    sizes = []
    avg_result = []
    count_typ = 0
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
