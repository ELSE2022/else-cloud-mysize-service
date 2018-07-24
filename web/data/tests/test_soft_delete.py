import unittest
from data.models.ScanMetric import ScanMetric
from data.models.ScannerModel import ScannerModel
from services.db_connector_service import database_update_service
from data.tests import settings


class TestSoftDelete(unittest.TestCase):

    def setUp(self):
        database_update_service(settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD, True)
        scanner_model = ScannerModel.add(dict(name='Test model'))
        self.scan_metric = ScanMetric.add(dict(scanner_model=scanner_model, name='Test metric'))

    def test_query_model(self):
        metrics_count = ScanMetric.query_set.count()
        self.assertEqual(metrics_count, 1)

    def test_delete_model(self):
        ScanMetric.delete(self.scan_metric._id)
        self.assertEqual(ScanMetric.query_set.count(), 0)
        self.assertEqual(ScanMetric.objects.query().count(), 1)
