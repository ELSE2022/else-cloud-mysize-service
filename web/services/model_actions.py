import base64
import os
from pathlib import Path

from data.repositories import (
    SizeRepository,
    ModelRepository,
    ModelTypeRepository
)
from .utils.files import create_file


def add_stl_to_models_service(product, stl_data):
    """
    Add stl files to models

    Parameters
    ----------
    product: data.models.Product.Product
        Entity of a product model
    stl_data: iterable
        Collections with stl files

    Returns
    -------
    None
    """
    for stl in stl_data:
        size_value, model_type_value = stl['title'].replace('.stl', '').split('-')
        size = SizeRepository().get_size_by_value(size_value)
        model_types = ModelTypeRepository().get(dict(name=model_type_value))
        model_type = model_types[0] if model_types else None

        filecodestring = stl['src']
        data = base64.b64decode(filecodestring.split(',')[1])
        attachment_name = os.path.sep.join(
            [
                'Last',
                product.uuid,
                stl['title']
            ]
        )
        attachment_path = create_file(attachment_name)
        Path(attachment_path).write_bytes(data)
        ModelRepository().update(
            dict(model_type=model_type, size=size, product=product),
            dict(stl_path=attachment_path)
        )
