import yaml
import os

def load_config(path = "config.yaml"):
    '''
    Loads the configuration data from a specified yaml file
    '''
    with open(path) as f:
        return yaml.safe_load(f)