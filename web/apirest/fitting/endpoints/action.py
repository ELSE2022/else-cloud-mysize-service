import operator
from collections import defaultdict

from api.web_actions.best_size import get_foot_best_size
from api.web_actions.best_size import generate_result
from apirest.fitting.serializers import fitting_user
from apirest.fitting.serializers import profile_user
from apirest.fitting.serializers import scan_metric
from apirest.fitting.serializers import size
from apirest.fitting.serializers import user_scans
from apirest.fitting.serializers import user_size
from apirest.fitting.endpoints.product_action import msg_object_does_not_exist
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
from apirest.restplus import auth_required
# from api.web_actions.get_user_profile import get_user
from data.repositories import UserRepository
from data.repositories import ScanRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import UserSizeRepository
from data.repositories import ScanMetricRepository
from data.repositories import ScanMetricValueRepository
from data.repositories import ProductRepository
from data.repositories import ComparisonResultRepository
from data.models import User, Model, Size as _Size, ComparisonResult, Scan, Product, UserSize
from datetime import datetime
from flask import request
from flask import abort
from flask_restplus import Resource
from flask_restplus import reqparse
from orientdb_data_layer import data_connection
from pyorient import OrientRecordLink

from settings import SCANNER_STORAGE_BASE_URL

import logging

logger = logging.getLogger('rest_api_demo')
    
ns = api.namespace('fitting_users', path='/fitting/users', description='Operations related to User')

_userRep = UserRepository()
_scanRep = ScanRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_userSizeRep = UserSizeRepository()
_scanMetricRep = ScanMetricRepository()
_scanMetricValueRep = ScanMetricValueRepository()
_productRep = ProductRepository()
_comparisonResRep = ComparisonResultRepository()

default_size_arguments = reqparse.RequestParser()
default_size_arguments.add_argument('type', type=str, required=False)

best_style_arguments = reqparse.RequestParser()
best_style_arguments.add_argument('size', type=str, required=False)

default_scan_arguments = reqparse.RequestParser()
default_scan_arguments.add_argument('scan', type=str, required=True)


def get_user(user_uuid):
    if user_uuid is None:
        abort(400, 'Request malformed: \'user\' argument not passed')
    user = _userRep.get({
        'uuid': user_uuid,
    })
    if len(user) == 0:
        abort(404, 'User not found')
    if len(user) > 1:
        abort(400, 'Too many ({}) users with '
            'the same user_uuid: {}'.format(len(user), user_uuid))
    return user[0]


def get_objects(graph, user_uuid, product_uuid):
    user_obj = User.query_set.filter_by(uuid=user_uuid).first()
    if not user_obj:
        abort(400, msg_object_does_not_exist.format('User', user_uuid))

    product_obj = Product.query_set.filter_by(uuid=product_uuid).first()
    if not product_obj:
        abort(400, msg_object_does_not_exist.format('Product', product_uuid))

    model_types = graph.elements_from_links(
        graph.element_from_link(product_obj.default_comparison_rule).model_types)

    scans = Scan.query_set.filter_by(user=user_obj)
    if not scans:
        abort(400, 'User with uuid {} does not have any scans'.format(user_uuid))
    return user_obj, product_obj, model_types, scans


@ns.route('',)
class Users(Resource, ListModelMixin):
    model = User
    serializer = fitting_user

    def get(self):
        return super().get()

    @api.expect(fitting_user)
    @api.marshal_with(fitting_user)
    def post(self):
        """
        Api method to create user.
        """
        user_uuid = request.json.get('uuid')
        base_url = request.json.get('base_url', SCANNER_STORAGE_BASE_URL)
        size_value = request.json.get('size')
        user_obj = _userRep.get({'uuid': user_uuid})
        if not user_obj:
            user_obj = _userRep.add({'uuid': user_uuid, 'base_url': base_url}, result_JSON=False)
        else: user_obj = user_obj[0]
        if size_value:
            left_foot = _modelTypeRep.get(dict(name='LEFT_FOOT'))
            right_foot = _modelTypeRep.get(dict(name='RIGHT_FOOT'))
            if len(left_foot) == 0 and len(right_foot) == 0:
                left_foot = _modelTypeRep.add(dict(name='LEFT_FOOT'))
                right_foot = _modelTypeRep.add(dict(name='RIGHT_FOOT'))
            else:
                left_foot = left_foot[0]
                right_foot = right_foot[0]

            foot_types = [left_foot, right_foot]

            size_obj = _sizeRep.get({'string_value': size_value, 'model_types': foot_types})
            if not size_obj:
                size_obj = _sizeRep.add(dict(string_value=size_value, model_types=foot_types))
            else: size_obj = size_obj[0]
            for mt in foot_types:
                _userSizeRep.add({'user': user_obj, 'model_type': mt, 'size': size_obj, 'creation_time': str(datetime.now())})

        return user_obj


@ns.route('/<string:uuid>')
@api.response(404, 'User not found.')
class UserItem(Resource):
    @api.expect(fitting_user)
    def put(self, uuid):
        """
        Api method to update user.
        """
        user_obj = _userRep.update({'uuid': uuid}, request.json)[0]
        return {'@rid': user_obj._id, 'uuid': user_obj.uuid}, 201

    @api.response(204, 'User successfully deleted.')
    @api.marshal_with(fitting_user)
    def delete(self, uuid):
        """
        Api method to delete user.
        """
        _userRep.delete({'uuid': uuid})
        return None, 204

    @api.marshal_with(fitting_user)
    def get(self, uuid):
        """
        Returns a user object.
        """
        user = _userRep.get({'uuid': uuid})
        return user[0] if user else (None, 404)


@ns.route('/<string:uuid>/profile')
class UserProfile(Resource):
    @api.marshal_with(scan_metric)
    @api.expect(default_scan_arguments)
    def get(self, uuid):
        """
        Api method to get user profile.
        """
        _graph = data_connection.get_graph()

        user = get_user(uuid)
        scans = _scanRep.get({'user': user, 'scan_id': request.args.get('scan')})
        if not scans:
            return abort(400, msg_object_does_not_exist.format('Scans', request.args.get('scan')))
        # for sc in scans:
        #     scans_with_metrics = sc._props
        #     scans_with_metrics['metric'] = []
        #     metric_value = _scanMetricValueRep.get({
        #         'scan': sc,
        #     })
        #     for mv in metric_value:
        #         metric = _graph.element_from_link(mv.metric)
        #         metric_with_value = metric._props
        #         metric_with_value['value'] = mv.value
        #         scans_with_metrics['metric'].append(metric_with_value)
        #
        #     scans_list.append(scans_with_metrics)

        # sc_mt = _scanMetricValueRep.sql_command("SELECT scan.uuid as scan, metric, value FROM scanmetricvalue GROUP BY metric", result_as_dict=True)
        # print(sc_mt)
        # print(len(sc_mt))
        all_res_metric = []
        all_metrics = _scanMetricRep.get({'scanner_model': _graph.element_from_link(scans[0].scanner).model})
        for metric in all_metrics:
            res_metric = metric._props
            metric_value = _scanMetricValueRep.get_by_tree({
                'metric': metric,
                'scan': {'user': user, 'scan_id': request.args.get('scan')},
            })
            res_metric['values'] = metric_value
            all_res_metric.append(res_metric)

        return all_res_metric


@ns.route('/<string:uuid>/scans')
class Scans(Resource):
    @api.marshal_with(user_scans)
    def get(self, uuid):
        """
        Api method to get user scans.
        """
        # scans_list = []
        # user = _userRep.get({'uuid': uuid})
        scans = _scanRep.get_by_tree({'user': {'uuid': uuid}})
        # for sc in scans:
        #     metric = _scanMetricValueRep.get({
        #         'scan': sc,
        #     })
        #     scans_with_metrics = sc._props
        #     scans_with_metrics['metric'] = metric
        #     scans_list.append(scans_with_metrics)
        return scans


@ns.route('/<string:uuid>/scans/set_default')
class DefaultScan(Resource):
    @api.expect(default_scan_arguments)
    @api.marshal_with(user_scans)
    def post(self, uuid):
        """
        Api method to set default user scan.
        """
        scan_id = request.args.get('scan')
        user = get_user(uuid)
        scans = _scanRep.update({'user': user}, {'is_default': False})
        scans = _scanRep.update({'user': user, 'scan_id': scan_id}, {'is_default': True})

        return scans


@ns.route('/<string:uuid>/size')
class Size(Resource):
    @api.marshal_with(size)
    @api.expect(default_size_arguments)
    def get(self, uuid):
        """
        Api method to get default user size
        """
        _graph = data_connection.get_graph()
        user_obj = get_user(uuid)

        model_type = request.args.get('type', 'LEFT_FOOT')
        model_type_obj = _modelTypeRep.get(dict(name=model_type))
        if not model_type_obj:
            abort(400)
        user_size_obj = _userSizeRep.get_by_tree(dict(user=user_obj, model_type=model_type_obj[0]))
        if not user_size_obj:
            return abort(400, 'User doesn\'t have default size')
        return _graph.element_from_link(user_size_obj[0].size)

    @api.expect(size)
    @api.marshal_with(user_size)
    def post(self, uuid):
        """
        Api method to set default user size.
        """
        model_type_objects = []
        user = get_user(uuid)
        print(request.json)
        for mt in request.json['model_types']:
            model_type_obj = _modelTypeRep.get({'name': mt})
            if not model_type_obj:
                abort(400)
            else: model_type_obj = model_type_obj[0]
            model_type_objects.append(model_type_obj._id)

            size_object = _sizeRep.sql_command("select @rid as _id, string_value, model_types from size where {0} IN model_types AND string_value={1}".format(model_type_obj._id, request.json['string_value']), result_as_dict=True)
            user_size_rep = _userSizeRep.get({
                'user': user,
                'size': size_object[0].get('_id'),
                'model_type': model_type_obj._id,
            })
            if not user_size_rep:
                count_del = _userSizeRep.delete(dict(user=user, model_type=model_type_obj._id))
                user_size_rep = _userSizeRep.add({
                    'user': user,
                    'size': size_object[0].get('_id'),
                    'model_type': model_type_obj._id,
                    'creation_time': str(datetime.now()),
                })
            else:
                user_size_rep = user_size_rep[0]
        return {'user': user, 'size': size_object[0]}


@ns.route('/<string:user_uuid>/products/<string:product_uuid>/best_size')
class BestSize(Resource):
    def get(self, user_uuid, product_uuid):
        """
        Api method to get best user size.
        """
        _graph = data_connection.get_graph()
        # _comparisonResRep.delete({})

        user_obj, product_obj, model_types, scans = get_objects(_graph, user_uuid, product_uuid)
        logger.debug(scans)

        comparison_results = _comparisonResRep.get_by_tree({'scan': dict(user=user_obj, is_default=True),})
        logger.debug(comparison_results)
        if not comparison_results:
            comparison_results = get_foot_best_size(product_obj, model_types, scans)
            logger.debug('generate_result')
        dct = defaultdict(int)
        for x in comparison_results:
            model = Model.query_set.filter_by(**{'@rid': x.model}).first()
            size = _Size.query_set.filter_by(**{'@rid': model.size}).first()
            # logger.debug(size.string_value + ' ' + str(x.value))
            dct[size.string_value] += x.value / len(size.model_types)
            # logger.debug(size.string_value + ' ' + str(x.value))
        max_result = max(dct.items(), key=operator.itemgetter(1))
        logger.debug(max_result[0])
        return {'best_size': {
            'score': round(max_result[1], 2),
            'output_model': '',
            'size': max_result[0],
            'size_type': 'FOOT'
        }}


@ns.route('/<string:user_uuid>/products/<string:product_uuid>/best_style')
class BestStyle(Resource):
    
    @api.expect(best_style_arguments, validate=True)
    def get(self, user_uuid, product_uuid):
        """
        Api method to get best user style.
        """
        logger.debug('best_style')
        _graph = data_connection.get_graph()

        user_obj, product_obj, model_types, scans = get_objects(_graph, user_uuid, product_uuid)

        args = best_style_arguments.parse_args()
        if not args.get('size'):
            user_size_obj = UserSize.query_set.filter_by(user=user_obj)
            print(user_size_obj)
            size_obj = None
            for s in user_size_obj:
                _size = _Size.query_set.filter_by(**{'@rid': s.size}).first()
                if _graph.elements_from_links(_size.model_types) == model_types:
                    size_obj = _size
            if size_obj is None:
                abort(404, 'user\'s size not found')
        else:
            size_obj = _Size.query_set.filter_by(string_value=args.get('size')).first()
        
        results = _comparisonResRep.get_by_tree({'scan': dict(user=user_obj, is_default=True),
                                                            'size': size_obj})
        avg_res = 0
        if not results:
            results = get_foot_best_size(product_obj, model_types, scans)
        for x in results:
            model = Model.query_set.filter_by(**{'@rid': x.model}).first()
            size = _Size.query_set.filter_by(**{'@rid': model.size}).first()
            if size.string_value == size_obj.string_value:
                avg_res += x.value / len(size.model_types)

        return {'best_style': {
            'score': round(avg_res, 2),
            'output_model': '',
            'size': size_obj.string_value,
            'size_type': 'FOOT'
        }}
