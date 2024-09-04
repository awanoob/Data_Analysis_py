import yaml as ym
from yaml import CLoader

yaml_path = r"C:\VSCode\Python\python_proj\.DataAnalysis_py\main_func\test.yaml"
with open(yaml_path, 'r', encoding='UTF-8') as yaml_file_in:
    input_cfg = ym.load(yaml_file_in, Loader=CLoader)
    print(input_cfg)
