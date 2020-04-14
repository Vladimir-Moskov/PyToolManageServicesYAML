"""
    Just some General settings and imports here
"""

import logging
import sys

YAML_PATH: str = '../resources/'
YAML_NAME: str = 'services.yaml'
LOGGER_NAME: str = 'PyToolManageServicesYAMLLogger'

app_root_logger = logging.getLogger(LOGGER_NAME)
app_root_logger.setLevel(logging.DEBUG)

PRINT_ORDER_INDENT: str = " " * 4

# TODO: logger color formatting
# TODO: add additional logging to file

handler: logging.StreamHandler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app_root_logger.addHandler(handler)
