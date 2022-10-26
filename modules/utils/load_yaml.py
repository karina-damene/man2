from pathlib import Path   
import yaml     
def load_yaml_func(path_yaml_file):
    with Path(path_yaml_file).open() as f:
        config = yaml.safe_load(f)
    for bak, tables in config.items():
        for table, data_parameted in tables.items():
            return data_parameted, tables
        
#data_parameted, tables = load_yaml (r'config/config_data_bak.yaml')