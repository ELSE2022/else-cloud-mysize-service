from data.models.Size import Size
from orientdb_data_layer.data import RepositoryBase

from data.utils.string_processor import normalize_string


class DuplicatedSize(Exception):

    def __init__(self, value):
        super().__init__(f'Size with value {value} is exist')


class SizeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Size)

    def get_size_by_value(self, value):
        normalized_val = normalize_string(value)
        sizes = super(SizeRepository, self).get(
            dict(
                processed_value=normalize_string(normalized_val),
            )
        )
        return sizes[0] if sizes else None

    def get_model_types_size(self, model_types, size):
        sizes = super(SizeRepository, self).get(
            dict(
                model_types=model_types,
                processed_value=normalize_string(size)
            )
        )
        return sizes[0] if sizes else None

    def add(self, size_dict, result_JSON= False):
        normalized_val = normalize_string(size_dict.get('string_value'))
        if self.get_size_by_value(normalized_val):
            raise DuplicatedSize(size_dict.get('string_value', ''))
        processed_dict = dict(processed_value=normalized_val)
        return super(SizeRepository, self).add({**size_dict, **processed_dict, }, result_JSON=result_JSON)

    def update(self, query_dict, prop_dict):
        processed_dict = dict()
        if 'string_value' in prop_dict:
            processed_dict.update(processed_name=normalize_string(prop_dict.get('string_value')))

        return super(SizeRepository, self).update(
            query_dict,
            {**query_dict, **processed_dict, }
        )
