import unittest

from data.models import ScanMetric, ScannerModel
from data.repositories.ScannerModelRepository import ScannerModelRepository
from data.repositories.ScanMetricRepository import ScanMetricRepository
from services.db_connector_service import database_update_service
from data.tests import settings


class TestRepositoryUpdateMethod(unittest.TestCase):

    def setUp(self):
        database_update_service(settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD, True)
        self.scanner_model = ScannerModel.add(dict(name='Test'))
        self.scan_metric = ScanMetric.add(dict(scanner_model=self.scanner_model, name='test'))

    def test_update_model(self):
        scanner_models = ScannerModelRepository().update(dict(name='Test'), dict(name='Updated'))
        scanner_model_query = ScannerModel.query_set.filter_by(name='Updated')

        self.assertEqual(len(scanner_models), 1)
        self.assertIsInstance(scanner_models[0], ScannerModel)
        self.assertEqual(scanner_models[0]._id, self.scanner_model._id)
        self.assertEqual(scanner_models[0].name, 'Updated')

        self.assertEqual(scanner_model_query.count(), 1)
        self.assertEqual(scanner_model_query.one()._id, self.scanner_model._id)
        self.assertEqual(scanner_model_query.one().name, 'Updated')

    def test_update_soft_delete_model(self):
        scan_metrics = ScanMetricRepository().update(dict(name='test'), dict(name='Updated'))
        scan_metrics_query = ScanMetric.query_set.filter_by(name='Updated')

        self.assertEqual(len(scan_metrics), 1)
        self.assertIsInstance(scan_metrics[0], ScanMetric)
        self.assertEqual(scan_metrics[0]._id, self.scan_metric._id)
        self.assertEqual(scan_metrics[0].name, 'Updated')

        self.assertEqual(scan_metrics_query.count(), 1)
        self.assertEqual(scan_metrics_query.one()._id, self.scan_metric._id)
        self.assertEqual(scan_metrics_query.one().name, 'Updated')
