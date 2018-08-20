from slugify import slugify


def normalize_string(value):
    return slugify(value.strip().lower())
