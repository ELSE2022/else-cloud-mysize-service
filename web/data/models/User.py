from settings import SCANNER_STORAGE_BASE_URL
from pyorient.ogm.property import String, Integer, LinkSet
from .BaseModel import BaseNode, BaseModel
from .Scan import Scan


class User(BaseNode, BaseModel):
    element_plural = 'users'
    uuid = String(unique=True, mandatory=True, nullable=False)
    num_id = Integer()
    base_url = String(default=SCANNER_STORAGE_BASE_URL)

    def __str__(self):
        return f'<User: {self.uuid}>'

    def get_default_scans(self, model_types=[]):
        return Scan.query_set.filter_by(user=self, is_default=True)

    def get_scans(self, model_types=[]):
        return Scan.query_set.filter_by(user=self)
