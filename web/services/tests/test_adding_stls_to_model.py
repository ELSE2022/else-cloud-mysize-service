import os
import unittest
import base64
import shutil
from pathlib import Path
from data.repositories import (
    BrandRepository,
    ModelRepository,
    ModelTypeRepository,
    ScannerModelRepository,
    ComparisonRuleRepository,
    ProductRepository,
    SizeRepository,
)
from services.db_connector_service import database_update_service
from data.tests import settings
from services.model_actions import add_stl_to_models_service


class TestRepositoryDeleteMethod(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database_update_service(settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD, True)
        cls.left_type = ModelTypeRepository().add(dict(name='LEFT_FOOT'))
        cls.right_type = ModelTypeRepository().add(dict(name='RIGHT_FOOT'))
        cls.brand = BrandRepository().add(dict(uuid='test_uuid', name='test_name'))
        cls.scanner_model = ScannerModelRepository().add(dict(name='test_scanner_model'))
        cls.cmp_rule = ComparisonRuleRepository().add(dict(
            scanner_model=cls.scanner_model,
            model_types=[cls.left_type, cls.right_type]
        ))
        cls.size = SizeRepository().add(dict(
            model_types=[cls.left_type, cls.right_type],
            string_value='42',
            order=1,
        ))
        cls.product = ProductRepository().add(dict(
            uuid='test_product',
            sku='test_product',
            name='test_sku',
            brand=cls.brand,
            default_comparison_rule=cls.cmp_rule,
        ))

    def setUp(self):
        self.left_model = ModelRepository().add(dict(
            product=self.product,
            size=self.size,
            model_type=self.left_type,
        ))
        self.right_model = ModelRepository().add(dict(
            product=self.product,
            size=self.size,
            model_type=self.right_type,
        ))

    def tearDown(self):
        path = Path(settings.MEDIA_ROOT.strip('/').split('/')[0])
        shutil.rmtree(path)

    def test_stl_path(self):
        content = b'test_content'
        files = [
            dict(title='42-LEFT_FOOT.stl', src='type:,' + base64.b64encode(content).decode()),
            dict(title='42-RIGHT_FOOT.stl', src='type:,' + base64.b64encode(content).decode()),
        ]
        add_stl_to_models_service(self.product, files)

        expected_left_path = os.path.sep.join(
            [
                settings.MEDIA_ROOT.strip('/'),
                'Last',
                self.product.uuid,
                '42-LEFT_FOOT.stl',
            ]
        )
        expected_right_path = os.path.sep.join(
            [
                settings.MEDIA_ROOT.strip('/'),
                'Last',
                self.product.uuid,
                '42-RIGHT_FOOT.stl',
            ]
        )
        self.assertEqual(ModelRepository().get({'@rid': self.left_model._id})[0].stl_path, expected_left_path)
        self.assertEqual(ModelRepository().get({'@rid': self.right_model._id})[0].stl_path, expected_right_path)

    def test_stl_content(self):
        content = b'test_content'
        files = [
            dict(title='42-LEFT_FOOT.stl', src='type:,' + base64.b64encode(content).decode()),
            dict(title='42-RIGHT_FOOT.stl', src='type:,' + base64.b64encode(content).decode()),
        ]
        add_stl_to_models_service(self.product, files)

        left_content = Path(ModelRepository().get({'@rid': self.left_model._id})[0].stl_path).read_bytes()
        right_content = Path(ModelRepository().get({'@rid': self.right_model._id})[0].stl_path).read_bytes()

        self.assertEqual(left_content, content)
        self.assertEqual(right_content, content)
