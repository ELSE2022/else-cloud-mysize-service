from functools import partial
from itertools import starmap
from operator import methodcaller, itemgetter
from toolz import dicttoolz, itertoolz, functoolz
import tempfile

import petl
from orientdb_data_layer import data_connection
from pathlib import Path
import requests
from datetime import datetime
import os

from data.repositories import ScannerRepository
from data.repositories import ScanRepository
from data.repositories import UserRepository
from data.repositories import ModelTypeRepository
from data.repositories import ScanMetricValueRepository
from data.repositories import ScanMetricRepository
from data.repositories import ProductRepository
from data.repositories import ScannerModelRepository

from .utils.files import create_file


_scannerRep = ScannerRepository()
_scannerModelRep = ScannerModelRepository()
_scanMetricRep = ScanMetricRepository()
_scanMetricValueRep = ScanMetricValueRepository()
_scanRep = ScanRepository()
_productRep = ProductRepository()
_userRep = UserRepository()
_modelTypeRep = ModelTypeRepository()


msg_object_does_not_exist = '{} object with id "{}" not found'
attribute_urls_type = {
    'LEFT_FOOT': 'left',
    'RIGHT_FOOT': 'right',
}
scan_type_dict = {
    'FOOT': [{'name': 'LEFT_FOOT', 'stl_name': 'model_l.stl'},
             {'name': 'RIGHT_FOOT', 'stl_name': 'model_r.stl'}]
}


class ScanActionService:

    @classmethod
    def upload(cls, url):
        request = requests.get(
            url=url,
        )
        request.raise_for_status()
        return request.content

    @classmethod
    def procces_metrics(cls, scanner_model, metric_name):
        return itertoolz.first(_scanMetricRep.get(dict(name=metric_name, scanner_model=scanner_model)))

    @classmethod
    def create_scan_metric_value(cls, scan, value, metric):
        results = _scanMetricValueRep.update(dict(scan=scan, metric=metric), dict(value=value))
        if not results:
            results = _scanMetricValueRep.add(dict(scan=scan, metric=metric, value=value))

        return results

    @classmethod
    def update_scan_attributes(cls, scan, scan_type):
        _graph = data_connection.get_graph()
        scanner_obj = _graph.element_from_link(scan.scanner)
        path_to_csv = '{}{}/{}/{}_{}_mes.csv'.format(scanner_obj.base_url, scanner_obj.name, scan.scan_id, scan.scan_id,
                                                     attribute_urls_type[scan_type.name])
        request = requests.get(path_to_csv)
        request.raise_for_status()
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(request.content)
        file.close()
        init_table = petl.fromcsv(file.name, delimiter=';')
        table = init_table.skip(1) if 'DOMESCAN' in init_table.header() else init_table
        print(list(functoolz.pipe(
            itertoolz.first(table.dicts()),
            partial(dicttoolz.itemmap, reversed),
            partial(dicttoolz.valmap, partial(cls.procces_metrics, scanner_obj.model)),
            partial(filter, itemgetter(1)),
            methodcaller('items'),
            partial(starmap, partial(cls.create_scan_metric_value, scan),),
        )))

    @classmethod
    def update_user_scan(cls, user, scanner, scan_id, scan_model_type, is_scan_default, scan_path):
        """
        Update scan data

        Parameters
        ----------
        user :  web.data.models.User.User
            User whose scan will be updated
        scanner : web.data.models.Scanner.Scanner
            Scanner that has been set in request_data
        scan_id : str or None
            Id of last scan
        scan_model_type : str
            Name of a scan type that has been set in request_data
        is_scan_default : bool
            Boolean param that depends on request args
        scan_path : str
            String param that depends on scanner base_url and name, scan_id and stl name of scan_type

        Returns
        -------
        Scan: web.data.models.Scan.Scan
            Updated scan object
        """
        scan_type = _modelTypeRep.get({'name': scan_model_type})
        if not scan_type:
            scan_type = _modelTypeRep.add(dict(name=scan_model_type))
        else:
            scan_type = scan_type[0]

        foot_attachment_content = cls.upload(scan_path)
        attachment_name = os.path.sep.join(
            [
                'Scan',
                user.uuid,
                '{}-{}-{}'.format(datetime.now().year, datetime.now().month, datetime.now().day),
                '{}.{}'.format(scan_type.name, 'stl')
            ]
        )

        attachment_path = create_file(attachment_name)
        Path(attachment_path).write_bytes(foot_attachment_content)
        scan = _scanRep.get(dict(user=user, model_type=scan_type, scan_id=scan_id))
        if not scan:
            scan = _scanRep.add(dict(user=user, model_type=scan_type, scan_id=scan_id, scanner=scanner, stl_path=attachment_name, creation_time=datetime.now(), is_default=is_scan_default))
        else:
            scan = _scanRep.update(dict(user=user, model_type=scan_type, scan_id=scan_id), dict(stl_path=attachment_name, is_default=is_scan_default))[0]
        if is_scan_default:
            _scanRep.update({'user': user}, {'is_default': False})
            _scanRep.update({'user': user, 'scan_id': scan_id}, {'is_default': True})

        _scanMetricValueRep.delete(dict(scan=scan))

        try:
            cls.update_scan_attributes(scan, scan_type)
        except requests.HTTPError:
            print('HTTPError')
        return scan