from data.models.Size import Size
from orientdb_data_layer.data import RepositoryBase


class SizeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Size)

    def get_model_types_size(self, model_types, size):
        print(model_types)
        sizes = super(SizeRepository, self).get({'model_types': model_types, 'string_value': size})
        return sizes[0] if sizes else None
