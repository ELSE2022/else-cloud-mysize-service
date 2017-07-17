import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from collections import namedtuple

from data.repositories import UserRepository
from data.repositories import BrandRepository
from data.repositories import ProductRepository
from data.repositories import ModelTypeRepository
from data.repositories import ModelRepository
from data.repositories import SizeRepository
from data.repositories import ModelMetricRepository
from data.repositories import ModelMetricValueRepository


def import_sql(connectionstring):

    engine = sqlalchemy.create_engine(connectionstring)
    session = scoped_session(sessionmaker(bind=engine))
    s = session()

    def call_sql(sql_text):
        result = s.execute(sql_text)

        Record = namedtuple('Record', result.keys())
        return [Record(*r) for r in result.fetchall()]

    # Populate User
    _rep = UserRepository()
    for r in call_sql('SELECT * FROM fitting_user'):
        if len(_rep.get(dict(uuid=r.uuid))) == 0:
            _rep.add(dict(uuid=r.uuid, base_url=r.base_url))

    # Populate Brand (FAKE)
    _rep = BrandRepository()
    brand = None
    if len(_rep.get(dict(uuid='860f5cd9-0edf-41dd-acb9-c162e95fa6c7'))) == 0:
        brand = _rep.add(dict(uuid='860f5cd9-0edf-41dd-acb9-c162e95fa6c7', name='Initial BRAND (data export)'))
    else:
        brand = _rep.get(dict(uuid='860f5cd9-0edf-41dd-acb9-c162e95fa6c7'))[0]

    # Populate Product
    _rep = ProductRepository()
    for r in call_sql('SELECT * FROM fitting_product'):
        if len(_rep.get(dict(uuid=r.uuid))) == 0:
            _rep.add(dict(uuid=r.uuid, brand=brand))

    # Populate model types
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

    # Populate sizes, models, model metrics
    _productRep = ProductRepository()
    _modelRep = ModelRepository()
    _sizeRep = SizeRepository()
    _metricRep = ModelMetricRepository()
    _metricValRep = ModelMetricValueRepository()

    for r in call_sql('SELECT product.uuid as product_uuid, last.id as model, last_attr."name" as attribute, last_attr.value as value, last.model_type as model_type, size.value as size_value, size.numeric_value as size_order\
                        FROM fitting_lastattribute as last_attr\
                        left outer join fitting_last as last\
                        on last.id = last_attr.last_id\
                        left outer join fitting_product as product\
                        on product.id = last.product_id\
                        left outer join fitting_size as size\
                        on size.id = last.size_id'):
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
            metric = _metricRep.get(dict(product=product, name=r.attribute))
            if len(metric) == 0:
                metric = _metricRep.add(dict(product=product, name=r.attribute))
            else:
                metric = metric[0]
            metric_value = _metricValRep.get(dict(model=model, metric=metric))
            if len(metric_value) == 0:
                metric_value = _metricValRep.add(dict(model=model, metric=metric, value=r.value))

    print('Import Ended')