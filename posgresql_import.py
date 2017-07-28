import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from collections import namedtuple

from data.repositories import UserRepository
from data.repositories import BrandRepository
from data.repositories import ProductRepository
from data.repositories import ModelTypeRepository
from data.repositories import ModelRepository
from data.repositories import SizeRepository
from data.repositories import ModelTypeMetricRepository
from data.repositories import ModelMetricValueRepository
from data.repositories import ScannerModelRepository
from data.repositories import ScannerRepository
from data.repositories import ScanMetricRepository
from data.repositories import ComparisonRuleRepository
from data.repositories import ComparisonRuleMetricRepository
from data.repositories import ScanRepository
from data.repositories import ScanMetricValueRepository
from data.repositories import UserSizeRepository


def import_sql(connectionstring):

    engine = sqlalchemy.create_engine(connectionstring)
    session = scoped_session(sessionmaker(bind=engine))
    s = session()

    def call_sql(sql_text):
        result = s.execute(sql_text)

        Record = namedtuple('Record', result.keys())
        return [Record(*r) for r in result.fetchall()]

    print("Import data from {0}".format(connectionstring))

    # Populate ScannerModel
    print("Import ScannerModel")
    _rep = ScannerModelRepository()
    scanner_model = _rep.get(dict(name='IBV'))
    if len(scanner_model) == 0:
        scanner_model = _rep.add(dict(name='IBV'))
    else:
        scanner_model = scanner_model[0]

    # Populate model types'
    print("Import ModelType")
    _rep = ModelTypeRepository()
    left_foot = _rep.get(dict(name='LEFT_FOOT'))
    right_foot = _rep.get(dict(name='RIGHT_FOOT'))
    if len(left_foot) == 0 and len(right_foot) == 0:
        left_foot = _rep.add(dict(name='LEFT_FOOT'))
        right_foot = _rep.add(dict(name='RIGHT_FOOT'))
    else:
        left_foot = left_foot[0]
        right_foot = right_foot[0]

    foot_types = [left_foot, right_foot]

    # Populate Comparison Rule
    print("Import ComparisonRule")
    _rep = ComparisonRuleRepository()
    comp_rule = _rep.get(dict(name='FOOT', model_types=foot_types, scanner_model=scanner_model))
    if len(comp_rule) == 0:
        comp_rule = _rep.add(dict(name='FOOT', model_types=foot_types, scanner_model=scanner_model))
    else:
        comp_rule = comp_rule[0]

    # Populate Brand (FAKE)
    print("Import Brand")
    _rep = BrandRepository()
    brand = None
    if len(_rep.get(dict(uuid='860f5cd9-0edf-41dd-acb9-c162e95fa6c7'))) == 0:
        brand = _rep.add(dict(uuid='860f5cd9-0edf-41dd-acb9-c162e95fa6c7', name='Initial BRAND (data export)'))
    else:
        brand = _rep.get(dict(uuid='860f5cd9-0edf-41dd-acb9-c162e95fa6c7'))[0]

    # Populate Product
    print("Import Product")
    _rep = ProductRepository()
    for r in call_sql("SELECT *\
                FROM fitting_product\
                where uuid in ('X004-128-C1825', 'X004-994-C723', 'X001-081-C351R', 'X001-894-C443R', 'X001-776-C510R', 'X001-286-C3001R') "):
        if len(_rep.get(dict(uuid=r.uuid))) == 0:
            _rep.add(dict(uuid=r.uuid, brand=brand, default_comparison_rule=comp_rule))

    # Repositories links

    _productRep = ProductRepository()
    _modelRep = ModelRepository()
    _sizeRep = SizeRepository()
    _metricRep = ModelTypeMetricRepository()
    _metricValRep = ModelMetricValueRepository()
    _scanMetricRep = ScanMetricRepository()
    _compRuleMetricRep = ComparisonRuleMetricRepository()
    _userRep = UserRepository()
    _scannerRep = ScannerRepository()
    _scanRep = ScanRepository()
    _scanMetricValueRep = ScanMetricValueRepository()
    _userSizeRep = UserSizeRepository()

    # Populate sizes, models, model metrics
    data = call_sql("SELECT product.uuid as product_uuid, last.id as model, last_attr.name as attribute, last_attr.scan_attribute_name as scan_attribute, last_attr.value as value, last.model_type as model_type, size.value as size_value, size.numeric_value as size_order, last_attr.left_limit_value as f1, last_attr.best_value as shift, last_attr.right_limit_value as f2\
                        FROM fitting_lastattribute as last_attr\
                        left outer join fitting_last as last\
                        on last.id = last_attr.last_id\
                        left outer join fitting_product as product\
                        on product.id = last.product_id\
                        left outer join fitting_size as size\
                        on size.id = last.size_id\
                        where product.uuid in ('X004-128-C1825', 'X004-994-C723', 'X001-081-C351R', 'X001-894-C443R', 'X001-776-C510R', 'X001-286-C3001R')")
    i = 0
    l = len(data)

    for r in data:
        product = _productRep.get(dict(uuid=r.product_uuid))
        if len(product) != 0:
            product = product[0]
            size = _sizeRep.get(dict(string_value=r.size_value, order=r.size_order, model_types=foot_types))
            if len(size) == 0:
                size = _sizeRep.add(dict(string_value=r.size_value, order=r.size_order, model_types=foot_types))
            else:
                size = size[0]
            model = _modelRep.get(
                dict(product=product, model_type=left_foot if r.model_type == 'LEFT_FOOT' else right_foot,
                     size=size, name=r.model))
            if len(model) == 0:
                model = _modelRep.add(
                    dict(product=product, model_type=left_foot if r.model_type == 'LEFT_FOOT' else right_foot,
                         size=size, name=r.model))
            else:
                model = model[0]
            metric = _metricRep.get(dict(model_type=model.model_type, name=r.attribute))
            if len(metric) == 0:
                metric = _metricRep.add(dict(model_type=model.model_type, name=r.attribute))
            else:
                metric = metric[0]
            metric_value = _metricValRep.get(dict(model=model, metric=metric, value=r.value))
            if len(metric_value) == 0:
                metric_value = _metricValRep.add(dict(model=model, metric=metric, value=r.value))
            else:
                metric_value = metric_value[0]

            # Scan metrics
            scan_metric = _scanMetricRep.get(dict(scanner_model=scanner_model, name=r.scan_attribute))
            if len(scan_metric) == 0:
                scan_metric = _scanMetricRep.add(dict(scanner_model=scanner_model, name=r.scan_attribute))
            else:
                scan_metric = scan_metric[0]

            # Comparison Rule metric
            rule_metric = _compRuleMetricRep.get(dict(rule=comp_rule,
                                                      model=model,
                                                      model_metric=metric,
                                                      scan_metric=scan_metric,
                                                      f1=r.f1,
                                                      shift=r.shift,
                                                      f2=r.f2
                                                      ))
            if len(rule_metric) == 0:
                rule_metric = _compRuleMetricRep.add(dict(rule=comp_rule,
                                                          model=model,
                                                          model_metric=metric,
                                                          scan_metric=scan_metric,
                                                          f1=r.f1,
                                                          shift=r.shift,
                                                          f2=r.f2
                                                          ))
            else:
                rule_metric = rule_metric[0]

        i += 1
        print("Import Product, Size, Model, ModelMetric, ModelMetricValue: {0}/{1}".format(i, l))

    #Scans import
    data = call_sql("SELECT users.id as user_id, users.uuid as user_uuid, users.base_url as user_url, scan.id as scan_num_id, scan.scan_id, scan.scanner, scan.created_date, scan.attachment, scan.model_type, attr.name, attr.value\
                        FROM fitting_scan as scan\
                        left outer join fitting_scanattribute as attr\
                        on attr.scan_id = scan.id\
                        left outer join fitting_user as users\
                        on users.id = scan.user_id")
    i = 0
    l = len(data)

    for r in data:

        user = _userRep.get(dict(uuid=r.user_uuid, num_id=r.user_id, base_url=r.user_url))
        if len(user) == 0:
            user = _userRep.add(dict(uuid=r.user_uuid, num_id=r.user_id, base_url=r.user_url))
        else:
            user = user[0]

        scanner = _scannerRep.get(dict(name=r.scanner, model=scanner_model))
        if len(scanner) == 0:
            scanner = _scannerRep.add(dict(name=r.scanner, model=scanner_model))
        else:
            scanner = scanner[0]

        scan = _scanRep.get(dict(num_id=r.scan_num_id, user=user, scanner=scanner, model_type=left_foot if r.model_type == 'LEFT_FOOT' else right_foot,
                                 creation_time=r.created_date, scan_id=r.scan_id, stl_path=r.attachment))
        if len(scan) == 0:
            scan = _scanRep.add(
                dict(num_id=r.scan_num_id, user=user, scanner=scanner, model_type=left_foot if r.model_type == 'LEFT_FOOT' else right_foot,
                     creation_time=r.created_date, scan_id=r.scan_id, stl_path=r.attachment))
        else:
            scan = scan[0]

        if r.name == 'Name':
            _scanRep.update(
                dict(user=user, scanner=scanner, model_type=left_foot if r.model_type == 'LEFT_FOOT' else right_foot,
                     creation_time=r.created_date, scan_id=r.scan_id, stl_path=r.attachment), dict(name=r.value))
        elif r.name == 'Sex':
            _scanRep.update(
                dict(user=user, scanner=scanner, model_type=left_foot if r.model_type == 'LEFT_FOOT' else right_foot,
                     creation_time=r.created_date, scan_id=r.scan_id, stl_path=r.attachment), dict(sex=r.value))
        elif r.name == 'scan_image':
            _scanRep.update(
                dict(user=user, scanner=scanner, model_type=left_foot if r.model_type == 'LEFT_FOOT' else right_foot,
                     creation_time=r.created_date, scan_id=r.scan_id, stl_path=r.attachment), dict(img_path=r.value))
        else:
            scan_metric = _scanMetricRep.get(dict(scanner_model=scanner_model, name=r.name))
            if len(scan_metric) == 0:
                scan_metric = _scanMetricRep.add(dict(scanner_model=scanner_model, name=r.name))
            else:
                scan_metric = scan_metric[0]

            scan_metric_value = _scanMetricValueRep.get(dict(scan=scan, metric=scan_metric, value=r.value))
            if len(scan_metric_value) == 0:
                scan_metric_value = _scanMetricValueRep.add(dict(scan=scan, metric=scan_metric, value=r.value))
            else:
                scan_metric_value = scan_metric_value[0]

        i += 1
        print("Import Scan, User, ScanMetricValue: {0}/{1}".format(i, l))

    # Default scans import
    print("Populating default scans")
    data = call_sql("SELECT * FROM fitting_user_default_scans")
    for r in data:
        _scanRep.update(dict(num_id=r.scan_id), dict(is_default=True))

    # User sizes import
    print("Populating user sizes")
    data = call_sql("SELECT usizes.user_id as user_id, sizes.numeric_value as size_order, sizes.value as size_value\
                        FROM fitting_user_sizes as usizes\
                        left outer join fitting_size as sizes\
                        on sizes.id = usizes.size_id")
    for r in data:

        user = _userRep.get(dict(num_id=r.user_id))
        if len(user) > 0:
            user = user[0]
            size = _sizeRep.get(dict(string_value=r.size_value, order=r.size_order, model_types=foot_types))
            if len(size) == 0:
                size = _sizeRep.add(dict(string_value=r.size_value, order=r.size_order, model_types=foot_types))
            else:
                size = size[0]
            _userSizeRep.add(dict(user=user, size=size, creation_time=datetime.datetime.now()))


    print('Import Ended')
