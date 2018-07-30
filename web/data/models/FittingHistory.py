from pyorient.ogm.property import String, DateTime, Link, Float

from .User import User
from .Scan import Scan
from .Brand import Brand
from .BaseModel import SoftDeleteModel
from .Model import Model
from .Size import Size

# from .Scan import Scan

BEST_STYLE = 'best_style'
BEST_SIZE = 'best_size'

OPERATION_TYPES = (
    (BEST_STYLE, 'best_style'),
    (BEST_SIZE, 'best_size')
)


class FittingHistory(SoftDeleteModel):
    element_plural = 'fitting_history'
    creation_time = DateTime(mandatory=True)
    operation_type = String(unique=False, mandatory=True, nullable=False)
    # comparison_result = Link(mandatory=True, nullable=True, linked_to=ComparisonResult)
    brand = Link(mandatory=True, nullable=False, linked_to=Brand)
    model = Link(mandatory=True, nullable=False, linked_to=Model)
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    user = Link(mandatory=True, nullable=False, linked_to=User)
    recommended_size_value = Link(mandatory=True, nullable=False, linked_to=Size)
    fitting_factor_value = Float()

    def __str__(self):
        return f'<Fitting History: {self.id}>'
