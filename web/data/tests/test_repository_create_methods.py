import unittest

from data.models import ScanMetric, ScannerModel
from data.repositories.ScannerModelRepository import ScannerModelRepository
from data.repositories.ScanMetricRepository import ScanMetricRepository
from services.db_connector_service import database_update_service
from data.tests import settings


class TestRepositoryCreateMethod(unittest.TestCase):

    def setUp(self):
        database_update_service(settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD, True)

    def test_create_model(self):
        scanner_model = ScannerModelRepository().add(dict(name='Test'))

        self.assertEqual(ScannerModel.query_set.count(), 1)
        self.assertIsNotNone(ScannerModel.query_set.first())
        self.assertIsInstance(ScannerModel.query_set.one(), ScannerModel)
        self.assertEqual(ScannerModel.query_set.one()._id, scanner_model._id)

    def test_create_soft_delete_model(self):
        scanner_model = ScannerModelRepository().add(dict(name='Test'))
        scan_metric = ScanMetricRepository().add(dict(scanner_model=scanner_model, name='test'))

        self.assertEqual(ScanMetric.query_set.count(), 1)
        self.assertIsNotNone(ScanMetric.query_set.first())
        self.assertIsInstance(ScanMetric.query_set.one(), ScanMetric)
        self.assertEqual(ScanMetric.query_set.one()._id, scan_metric._id)
