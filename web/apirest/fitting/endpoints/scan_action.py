import os
from apirest.fitting.serializers import scan
from apirest.restplus import api
from data.repositories import ScannerRepository
from data.repositories import ScanRepository
from data.repositories import UserRepository
from data.repositories import ModelTypeRepository
from datetime import datetime
from flask import request
from flask import abort
from flask_restplus import Resource

ns = api.namespace('fitting/scans/', description='Operations related to Scan')

_scannerRep = ScannerRepository()
_scanRep = ScanRepository()
_userRep = UserRepository()
_modelTypeRep = ModelTypeRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:id>')
class Scans(Resource):
    @api.marshal_with(scan)
    def get(self):
        """
        Returns a scans list.
        """
        print('get scans')
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None
        print('get scans2')
        print(request_data)
        scan_obj = _scanRep.get({})
        return (scan_obj[page_start:page_end], 200, {'X-Total-Count': len(scan_obj)}) if scan_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(scan)
    def post(self):
        """
        Api method to create scan.
        """
        user_obj = _userRep.get({'@rid': request.json['user']})
        if not user_obj:
            abort(400, msg_object_does_not_exist.format('User', request.json['user']))

        scanner_obj = _scannerRep.get({'@rid': request.json['scanner']})
        if not scanner_obj:
            abort(400, msg_object_does_not_exist.format('Scanner', request.json['scanner']))

        model_type_obj = _modelTypeRep.get({'@rid': request.json['model_type']})
        if not model_type_obj:
            abort(400, msg_object_does_not_exist.format('Model type', request.json['model_type']))

        data_dict = request.json
        data_dict['user'] = user_obj[0]
        data_dict['scanner'] = scanner_obj[0]
        data_dict['model_type'] = model_type_obj[0]
        scanner_obj = _scannerRep.add(data_dict, result_JSON=True)
        return scanner_obj

    @api.expect(scan)
    def put(self, id):
        """
        Api method to update scan.
        """
        scan_obj = _scanRep.update({'@rid': id}, request.json)[0]
        return {'@rid': scan_obj._id, 'name': scan_obj.name}, 201

    @api.response(204, 'Scan successfully deleted.')
    @api.marshal_with(scan)
    def delete(self, id):
        """
        Api method to delete scan.
        """
        _scanRep.delete({'@rid': id})
        return None, 204


def str2bool(in_str):
    return in_str in ['true', 'True', 'yes']


def update_scan(user, scanner, scan_id, scan_type, scan_path):
    scan = _scanRep.get(dict(user=user, model_type=scan_type, scan_id=scan_id))
    if not scan:
        scan = _scanRep.add(dict(user=user, model_type=scan_type, scan_id=scan_id))

    scan.scan_id = scan_id
    scan.scanner = scanner
    foot_attachment_content = upload(scan_path)
    attachment_name = os.path.sep.join(
        [
            'Scan',
            scan.user.uuid,
            '{}-{}-{}'.format(datetime.now().year, datetime.now().month, datetime.now().day),
            '{}.{}'.format(scan_type, STL_EXTENSION)
        ]
    )
    # attachment_name = gen_file_name(scan, '{}.{}'.format(scan_type, STL_EXTENSION))
    attachment_path = create_file(attachment_name)
    Path(attachment_path).write_bytes(foot_attachment_content)

    scan.attachment = attachment_name
    scan.save()

    ScanAttribute.objects.filter(scan=scan).delete()

    try:
        update_scan_attributes(user.base_url, scan, scan_type)
    except requests.HTTPError:
        logger.debug('HTTPError')
        traceback.print_exc(file=sys.stdout)
    if scan.attachment:
        create_scan_visualization(scan)

    return scan


def update_foot_scans(user, scanner, scan_id, scan_type):
    try:
        left_scan = update_scan(user, scanner, scan_id, scan_type, '{}{}/{}/model_l.stl'.format(user.base_url, scanner, scan_id))
    except requests.HTTPError:
        left_scan = None
    try:
        right_scan = update_scan(user, scanner, scan_id, scan_type, '{}{}/{}/model_r.stl'.format(user.base_url, scanner, scan_id))
    except requests.HTTPError:
        right_scan = None
    scans = []
    if left_scan is not None:
        scans.append(left_scan)
    if right_scan is not None:
        scans.append(right_scan)
    return scans


@ns.route('/<string:uuid>/get_metrics')
@api.response(404, 'Scan not found.')
class ScanItem(Resource):
    def put(self, uuid):
        """
        Returns a .
        """
        request_data = dict(request.args)
        user_uuid = request_data.get('user')
        scanner = request_data.get('scanner')
        scan_id = request_data.get('scan')
        scan_type = request_data.get('type').upper()
        is_scan_default = str2bool(request_data.get('is_default', 'false'))
        brand_id = request_data.get('brand', None)

        user = _userRep.get(dict(uuid=user_uuid)).first()
        if not user:
            user = _userRep.add(dict(uuid=user_uuid))

        scans = update_foot_scans(user[0], scanner, scan_id, scan_type)
        if len(scans) == 0:
            return HttpResponseBadRequest()
        try:
            for scan in scans:
                products = Product.objects.filter(brand_id=int(brand_id)) if brand_id else Product.objects.all()
                for product in products:
                    compare_by_metrics(scan, product)
        except Exception as e:
            logger.error(f'scan {scan_id} desn`t compare')
            traceback.print_exc(file=sys.stdout)
        products = Product.objects.filter(brand_id=int(brand_id)) if brand_id else Product.objects.all()
        VisualisationThread(scans[0], scans[1], products).start()

        if is_scan_default or not user.default_scans.all().exists():
            for scan in scans:
                set_default_scan(user, scan)

        return HttpResponse(
            json.dumps([str(scan) for scan in scans])
        )
