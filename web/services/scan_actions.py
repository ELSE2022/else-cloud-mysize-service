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

from services.csv_parser_service import CSVParserService


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
    """
    Service for actions with scan model

    Methods
    -------
    upload(cls, url)
        Upload file by url
    create_scan_metric_value(cls, scan, value, metric)
        Create entity of ScanMetricValue model
    update_scan_attributes(cls, scan, scan_type)
        Update metrics for scan
    update_user_scan(cls, user, scanner, scan_id, scan_model_type, is_scan_default, scan_path)
        Update user scans

    """

    @classmethod
    def upload(cls, url):
        """
        Upload file by urls and return file content

        Parameters
        ----------
        url: str
            Destination url

        Returns
        -------
        request.constent: bytes
            Binary response
        """
        request = requests.get(
            url=url,
        )
        request.raise_for_status()
        return request.content

    @classmethod
    def create_scan_metric_value(cls, scan, value, metric):
        """
        Create entity of ScanMetricValue model for given metric with value

        Parameters
        ----------
        scan: data.models.Scan.Scan
            Scan object
        value: str
            Value of scan metric
        metric: data.models.ScanMetric.ScanMetric
            ScanMetric object

        Returns
        -------
        results: data.models.ScanMetricValue.ScanMetricValue
            created scan metric value object
        """
        results = _scanMetricValueRep.update(dict(scan=scan, metric=metric), dict(value=value))
        if not results:
            results = _scanMetricValueRep.add(dict(scan=scan, metric=metric, value=value))

        return results

    @classmethod
    def update_scan_attributes(cls, scan, scan_type):
        """
        Update scan metric

        Parameters
        ----------
        scan: data.models.Scan.Scan
            Scan object
        scan_type: data.models.ModelType.ModelType

        Returns
        -------
        None
        """
        _graph = data_connection.get_graph()
        scanner_obj = _graph.element_from_link(scan.scanner)
        path_to_csv = '{}{}/{}/{}_{}_mes.csv'.format(
            scanner_obj.base_url,
            scanner_obj.name,
            scan.scan_id, scan.scan_id,
            attribute_urls_type[scan_type.name]
        )

        parsed_csv = CSVParserService.parse_scan_csv(cls.upload(path_to_csv), scan)
        for row in parsed_csv:
            cls.create_scan_metric_value(scan, *row)

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