import unittest

from data.models import ScanMetric, ScannerModel
from data.repositories.ScannerModelRepository import ScannerModelRepository
from data.repositories.ScanMetricRepository import ScanMetricRepository
from services.db_connector_service import database_update_service
from data.tests import settings


class TestRepositoryGetMethod(unittest.TestCase):

    def setUp(self):
        database_update_service(settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD, True)
        self.scanner_model = ScannerModel.add(dict(name='Test'))
        self.scan_metric = ScanMetric.add(dict(scanner_model=self.scanner_model, name='test'))

    def test_get_model(self):
        scanner_models = ScannerModelRepository().get(dict(name='Test'))

        self.assertEqual(len(scanner_models), 1)
        self.assertIsInstance(scanner_models[0], ScannerModel)
        self.assertEqual(scanner_models[0]._id, self.scanner_model._id)

    def test_get_soft_delete_model(self):
        scan_metrics = ScanMetricRepository().get(dict(name='test'))

        self.assertEqual(len(scan_metrics), 1)
        self.assertIsInstance(scan_metrics[0], ScanMetric)
        self.assertEqual(scan_metrics[0]._id, self.scan_metric._id)

    def test_get_by_tree_model(self):
        scan_metrics = ScanMetricRepository().get_by_tree(dict(name='test', scanner_model=dict(name='Test')))

        self.assertEqual(len(scan_metrics), 1)
        self.assertIsInstance(scan_metrics[0], ScanMetric)
        self.assertEqual(scan_metrics[0]._id, self.scan_metric._id)
