import logging
from flask import Blueprint, jsonify, request, abort
from ..authentication import requires_auth
from data.repositories import ProductRepository, ComparisonRuleRepository, ComparisonRuleMetricRepository, UserRepository, ScanRepository, ScanMetricRepository
from .best_scan import get_best_foot_scan, extract_calculation_attributes
from orientdb_data_layer import data_connection
from calculations.fitting_algorithms import metrics_comparison_config

logger = logging.getLogger(__name__)
_productRep = ProductRepository()
_compRuleRep = ComparisonRuleRepository()
_compRuleMetricRep = ComparisonRuleMetricRepository()
_scanRep = ScanRepository()
_scanMetricRep = ScanMetricRepository()
_userRep = UserRepository()


def get_foot_metrics_config(product, comparison_rule):
    _graph = data_connection.get_graph()

    scanner_model = _graph.element_from_link(comparison_rule.scanner_model)
    scan_metrics = _scanMetricRep.get(dict(scanner_model=scanner_model))

    model_types = ','.join([str(mod) for mod in comparison_rule.model_types])

    user_sizes = _productRep.sql_command("select user.uuid as user_uuid, size.string_value as size from usersize\
                                          where user.uuid in\
                                                (select from (select uuid, count(scan_id) as scans\
                                                  from (select user.uuid as uuid, scan_id, count(distinct(@rid)) as scans\
                                                  from scan where model_type in [{0}] group by user.uuid, scan_id) where scans = 2 group by uuid) where scans > 2)".format(model_types), result_as_dict=True)

    best_scans = [(user['size'], get_best_foot_scan(_userRep.get(dict(uuid=user['user_uuid']))[0], scanner_model)[0]) for user in user_sizes]

    scans_by_size = {}
    for scan in best_scans:

        size = float(scan[0])

        if not size in scans_by_size:
            scans_by_size[size] = {}
            scans_by_size[size][scan[1]] = {}

        scans = _scanRep.get(dict(scan_id=scan[1]))
        if len(scans) == 2:
            for sc in scans:
                if _graph.element_from_link(sc.model_type).name == 'LEFT_FOOT':
                    scans_by_size[size][scan[1]]['LEFT'] = extract_calculation_attributes(sc, scan_metrics)
                elif _graph.element_from_link(sc.model_type).name == 'RIGHT_FOOT':
                    scans_by_size[size][scan[1]]['RIGHT'] = extract_calculation_attributes(sc, scan_metrics)

    lasts_data = _productRep.sql_command("select model.size.string_value as size, metric.name as name, value\
                                          from modelmetricvalue where model.product = {0} and model.model_type.name = 'LEFT_FOOT'\
                                          order by size, name".format(product._id),result_as_dict=True)

    lasts_by_size = {}

    for last in lasts_data:
        size = float(last['size'])

        if size not in lasts_by_size:
            lasts_by_size[size] = {}

        lasts_by_size[size][last['name']] = float(last['value'])

    references = {}
    for ref in _productRep.sql_command("select distinct(scan_metric.name) as scan, distinct(model_metric.name) as model\
                                        from comparisonrulemetric where rule = {0}".format(comparison_rule._id),result_as_dict=True):
        references[ref['scan']] = ref['model']

    return metrics_comparison_config.generate_config(references, scans_by_size, lasts_by_size)

generate_comparison_config_action = Blueprint('generate_comparison_config_action', __name__)


@generate_comparison_config_action.route('/fitting/generate_comparison_config')
@requires_auth
def generate_comparison_config():
    product_uuid = request.args.get('product_id')

    product = _productRep.get(dict(uuid=product_uuid))
    if len(product) == 0:
        abort(404, 'product not found')
    else:
        product = product[0]

    comparison_rule = request.args.get('comparison_rule')
    comparison_rule = _compRuleRep.get(dict(name=comparison_rule))
    if len(comparison_rule) == 0:
        abort(404, 'comparison_rule not found')
    else:
        comparison_rule = comparison_rule[0]

    metrics_config = get_foot_metrics_config(product, comparison_rule)
    return jsonify({
        'mode': 'ONLY FOR TESTS!!!!!!',
        'product_uuid': product_uuid,
        'metrics_config': metrics_config
    })
