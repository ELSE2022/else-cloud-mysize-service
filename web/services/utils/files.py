import os
import settings
from pathlib import Path


def create_file(file_name):
    print(settings.MEDIA_ROOT, file_name)
    file_path = os.path.join(
        # os.sep,
        settings.MEDIA_ROOT.strip('/'),
        file_name
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    Path(file_path).touch()
    return file_path
