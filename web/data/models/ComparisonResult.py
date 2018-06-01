import datetime
from pyorient.ogm.property import Float
from pyorient.ogm.property import Link
from pyorient.ogm.property import DateTime
from .BaseModel import BaseNode, BaseModel
from .Scan import Scan
from .Model import Model


class ComparisonResult(BaseNode, BaseModel):
    element_plural = 'comparison_result'
    model = Link(mandatory=True, nullable=False, linked_to=Model)
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    creation_time = DateTime(mandatory=True, nullable=False, default=datetime.datetime.utcnow())
    value = Float()
