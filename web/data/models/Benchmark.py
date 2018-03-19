from pyorient.ogm.property import Link
from .BaseModel import BaseNode, BaseModel
from .Product import Product
from .Size import Size
from .Scan import Scan
from .User import User


class Benchmark(BaseNode, BaseModel):
    element_plural = 'benchmarks'
    product = Link(mandatory=True, nullable=False, linked_to=Product)
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    size = Link(mandatory=True, nullable=False, linked_to=Size)
    user = Link(mandatory=True, nullable=False, linked_to=User)
