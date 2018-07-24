import unittest

from data.models import ScanMetric, ScannerModel
from data.repositories.ScannerModelRepository import ScannerModelRepository
from data.repositories.ScanMetricRepository import ScanMetricRepository
from services.db_connector_service import database_update_service
from data.tests import settings


class TestRepositoryDeleteMethod(unittest.TestCase):

    def setUp(self):
        database_update_service(settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD, True)
        self.scanner_model = ScannerModel.add(dict(name='Test'))
        self.scan_metric = ScanMetric.add(dict(scanner_model=self.scanner_model, name='test'))

    def test_delete_model(self):
        ScannerModelRepository().delete(dict(name='Test'))

        self.assertEqual(ScannerModel.query_set.count(), 0)
        self.assertIsNone(ScannerModel.query_set.first())

    def test_delete_soft_delete_model(self):
        ScanMetricRepository().delete(dict(scanner_model=self.scanner_model, name='test'))

        self.assertEqual(ScanMetric.query_set.count(), 0)
        self.assertEqual(ScanMetric.objects.query().count(), 1)
        self.assertIsNone(ScanMetric.query_set.first())
