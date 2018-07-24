from data.models.CompareVisualization import CompareVisualization
from .BaseRepository import BaseRepository


class CompareVisualizationRepository(BaseRepository):

    def __init__(self):
        super().__init__(CompareVisualization)

    def add(self, prop_dict, result_JSON=False):
        """
        Create size object

        Parameters
        ----------
        prop_dict: dict
            Model data
        result_JSON: bool
            If True result will be returned as JSON

        Returns
        -------
        Created object
        """
        normalized_val = normalize_string(size_dict.get('string_value'))
        if self.get_size_by_value(normalized_val):
            raise DuplicatedSize(size_dict.get('string_value', ''))
        processed_dict = dict(processed_value=normalized_val)
        return super(SizeRepository, self).add({**prop_dict, **processed_dict, }, result_JSON=result_JSON)
