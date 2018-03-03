from settings import SCANNER_STORAGE_BASE_URL
from settings import DEFAULT_STORAGE_LOGIN
from settings import DEFAULT_STORAGE_PASSWORD
from pyorient.ogm.property import String, Link
from .BaseModel import BaseNode, BaseModel
from .ScannerModel import ScannerModel


class Scanner(BaseNode, BaseModel):
    element_plural = 'scanners'
    model = Link(mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
    base_url = String(default=SCANNER_STORAGE_BASE_URL)
    login = String(default=DEFAULT_STORAGE_LOGIN)
    password = String(default=DEFAULT_STORAGE_PASSWORD)

    @classmethod
    def add(cls, prop_dict, result_as_json=False):
        prop_dict['base_url'] = 'https://{}:{}@avatar3d.ibv.org:8443/webdev/{}/'.format(prop_dict.get('login'),
                                                                                        prop_dict.get('password'),
                                                                                        prop_dict.get('login').upper())
        return super().add(prop_dict, result_as_json)
