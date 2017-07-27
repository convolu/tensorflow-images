import os
from os.path import join, isdir, isfile

BASEDIR = "101_ObjectCategories"


def get_all_categories():
    a = [f for f in os.listdir(BASEDIR) if isdir(join(BASEDIR, f))]
    return a


def get_all_image_paths(category: str):
    category_path = join(BASEDIR, category)
    return [join(category_path, f) for f in os.listdir(category_path) if isfile(join(category_path, f))]
