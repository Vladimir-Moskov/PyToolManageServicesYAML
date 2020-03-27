"""
    yaml file reader
    - returns parsed / validated services from  file content

"""

import os

import yaml
from config import *
from services import Services


def parse_yaml_services(yaml_path: str, yaml_name: str) -> Services:
    """
        Convert yaml file to python object

        :param yaml_path: folder of yaml file
        :param yaml_name: yaml file name
        :return: serialized Services
    """
    services: Services = None
    try:
        with open(os.path.join(yaml_path, yaml_name), 'r') as stream:
            try:
                yaml_obj = yaml.safe_load(stream)
                services = Services(**yaml_obj)
            except yaml.YAMLError as error:
                app_root_logger.error(f"{repr(error)}")
                raise error
            except Exception as error:
                app_root_logger.error(f"{repr(error)}")
                raise error
    except Exception as error:
        app_root_logger.error(f"{repr(error)}")
        raise error
    return services
