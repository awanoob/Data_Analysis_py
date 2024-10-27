import yaml as ym
from yaml import CLoader


def yaml_read(yaml_path):
    with open(yaml_path, 'r') as yaml_file_in:
        input_cfg = ym.load(yaml_file_in, Loader=CLoader)
    return input_cfg
