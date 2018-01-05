from flask_restplus import fields
from apirest.restplus import api
from data.models import User

fitting_user = api.model('User', {
    'id': fields.String(readOnly=True, description='Users id', attribute='_id'),
    'uuid': fields.String(required=True, description='Users uuid'),
    'base_url': fields.String(required=True, description='Users base url'),
    # 'size': fields.String(required=False, description='Size'),
})

model_type = api.model('Model type', {
    'id': fields.String(required=False, readOnly=True, description='Model type id', attribute='_id'),
    'name': fields.String(required=True, description='Model type name'),
})

size = api.model('Size', {
    'id': fields.String(required=False, readOnly=True, description='Size id', attribute='_id'),
    'model_types': fields.List(fields.String, description='name', required=True),
    'string_value': fields.String(required=True),
})

user_size = api.model('User size', {
    'user': fields.Nested(fitting_user),
    'size': fields.Nested(size),
})

scan_metric = api.model('Scan metric', {
    'id': fields.String(required=False, readOnly=True, description='Scan metric id', attribute='_id'),
    'scanner_model': fields.String(required=True, description='Scanner model'),
    'name': fields.String(required=True, description='Scan metric name'),
})

scan = api.model('Scan', {
    'id': fields.String(required=False, description='Id', attribute='_id'),
    'user': fields.String(required=True, description='User'),
    'scanner': fields.String(required=True, description='Scanner'),
    'model_type': fields.String(required=True, description='Model type'),
    'is_default': fields.Boolean(required=True, description='Is default'),
    'creation_time': fields.DateTime(description='Scan creation time'),
    'scan_id': fields.String(required=True, description='Scan id'),
    'num_id': fields.Integer(required=True, description='Scan num id'),
    'name': fields.String(required=True, description='Scan name'),
    'sex': fields.String(required=True, description='Scan sex'),
    'stl_path': fields.String(required=True, description='Scan stl path'),
    'img_path': fields.String(required=True, description='Scan img path'),
    # 'metric': fields.List(fields.Nested(scan_metric)),
    # 'metric': fields.String(required=True, description='Scan metric'),
})

profile_user = api.model('Profile', {
    'uuid': fields.String(required=True, description='Users uuid'),
    'scans': fields.List(fields.Nested(scan)),
})

user_scans = api.inherit('User scans', scan, {
    'scanner': fields.String(required=True, description='Scanner'),
    'creation_time': fields.DateTime(description='Scan creation time')
})

brand = api.model('Brand', {
    'id': fields.String(required=False, description='Id', attribute='_id'),
    'uuid': fields.String(required=True, description='Users uuid'),
    'name': fields.String(required=True, description='Name'),
})

comparison_rule = api.model('Comparison rule', {
    'id': fields.String(required=False, readOnly=True, description='Comparison rule id', attribute='_id'),
    'model_types': fields.List(fields.String, description='model_types', required=True),
    'scanner_model': fields.String(required=True, description='Scanner model'),
    'name': fields.String(required=True, description='Name'),
})

product = api.model('Product', {
    'id': fields.String(required=False, readOnly=True, description='Id', attribute='_id'),
    'uuid': fields.String(required=True, description='Product uuid'),
    'brand': fields.String(required=True, description='Brand'),
    'sku': fields.String(required=True, description='SKU'),
    'name': fields.String(required=True, description='Name'),
    'default_comparison_rule': fields.String(required=True, description='Comparison rule')
})

model = api.model('Model', {
    'id': fields.String(description='Id', attribute='_id'),
    'product': fields.String(required=True, description='Product'),
    'model_type': fields.String(required=True, description='Model type'),
    'size': fields.String(required=True, description='Size'),
    'name': fields.String(required=True, description='Model name'),
    'stl_path': fields.String(required=False, description='Model stl path'),
})

model_type_metric = api.model('Model type metric', {
    'id': fields.String(required=False, readOnly=True, description='Id', attribute='_id'),
    'model_type': fields.String(required=True, description='Model type'),
    'name': fields.String(required=True, description='Model metric name'),
})

model_metric_value = api.model('Model metric value', {
    'id': fields.String(required=False, readOnly=True, description='Model metric value id', attribute='_id'),
    'model': fields.String(required=True, description='Model'),
    'metric': fields.String(required=True, description='Metric'),
    'value': fields.String(required=True, description='Value'),
})

scanner_model = api.model('Scanner models', {
    'id': fields.String(required=False, readOnly=True, description='Scanner model id', attribute='_id'),
    'name': fields.String(required=True, description='Scanner model name'),
})

scanner = api.model('Scanner', {
    'id': fields.String(description='Id', attribute='_id'),
    'model': fields.String(required=True, description='Scanner model'),
    'name': fields.String(required=True, description='Scanner name'),
})

comparison_result = api.model('Comparison result', {
    'id': fields.String(description='Id', attribute='_id'),
    'model_type': fields.String(required=True, description='Model type'),
    'scan': fields.String(required=True, description='Scan'),
    'size': fields.String(required=True, description='Size'),
    'creation_time': fields.DateTime(description='Comparison time'),
    'value': fields.Float(required=True, description='Value'),
})

comparison_rule_metric = api.model('Comparison rule metric', {
    'id': fields.String(required=False, readOnly=True, description='Comparison rule metric id', attribute='_id'),
    'rule': fields.String(required=True, description='Comparison rule'),
    'model': fields.String(required=True, description='Model'),
    'model_metric': fields.String(required=True, description='Model metric'),
    'scan_metric': fields.String(required=True, description='Scan metric'),
    'f1': fields.Float(required=True, description='f1'),
    'shift': fields.Float(required=True, description='Shift'),
    'f2': fields.Float(required=True, description='f2'),
})
