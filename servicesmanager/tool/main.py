"""
    Use it as solution provider - script which is doing requested job (task.tx)
    Can be run only with one mandatory argument [start, stop]

"""

import argparse
import os
from enum import Enum
from config import *
from services import Services
from services_start import start_order, start_estimated_order
from services_stop import stop_order, stop_estimated_order
from yaml_parser import parse_yaml_services
from typing import List


class Operation(Enum):
    """
        Supported command line values / operations
    """
    ARG_COMMAND_START = "start"
    ARG_COMMAND_STOP = "stop"

    def __str__(self) -> str:
        """
            Custom string representation of command value
        :return: command
        """
        return self.value


def print_flow_order(flow_ar: List) -> str:
    """
        Print service order in more user friendly format
    :param flow_ar:
    :return: string for print
    """
    flow_ar_str = [', '.join(sub_ar) for sub_ar in flow_ar]
    flow_ar_str = ''.join([f"{PRINT_ORDER_INDENT} {i + 1}.{sub_str}\n" for i, sub_str in enumerate(flow_ar_str)])
    return flow_ar_str


def start_services(services: Services):
    """
        Actual logic to perform services starting

        :param services: - parsed services as Services object
        :return: None
    """
    app_root_logger.info("Start services start hierarchy creation")
    # get estimated order
    start_flow: List = start_estimated_order(services)
    start_flow_str: str = print_flow_order(start_flow)
    app_root_logger.info(f"Services estimated starting order will be: \n{start_flow_str}")

    # example of real order
    start_flow: List = start_order(services)
    start_flow_str: str = print_flow_order(start_flow)
    app_root_logger.info(f"Services 'real' starting order will be: \n{start_flow_str}")


def stop_services(services: Services):
    """
        Actual logic to perform services stopping

        :param services: - parsed services as Services object
        :return: None
    """
    app_root_logger.info("Start services stop hierarchy creation")
    # get estimated order
    stop_flow: List = stop_estimated_order(services)
    stop_flow_str: str = print_flow_order(stop_flow)
    app_root_logger.info(f"Services estimated stopping order will be:\n{stop_flow_str}")

    # example of real order
    stop_flow: List = stop_order(services)
    stop_flow_str: str = print_flow_order(stop_flow)
    app_root_logger.info(f"Services 'real' stopping order will be:\n{stop_flow_str}")


if __name__ == '__main__':
    # Parse command line args
    parser = argparse.ArgumentParser()

    parser.add_argument('operation', type=Operation, choices=list(Operation),
                        help=f"{__doc__} \n "
                             f"Supported operation values {Operation.ARG_COMMAND_START} or {Operation.ARG_COMMAND_STOP}")
    # default  default=Operation.ARG_COMMAND_START,
    args = parser.parse_args()

    # parse / validate given yaml
    try:
        yaml_path = os.path.abspath(YAML_PATH)
        services: Services = parse_yaml_services(yaml_path, YAML_NAME)
        if services:
            app_root_logger.info("YAML file has been parsed and services hierarchy has been created")
            app_root_logger.debug(repr(services))

            if args.operation == Operation.ARG_COMMAND_START:
                start_services(services)
            else:
                stop_services(services)
            app_root_logger.info("DONE !!!")
        else:
            app_root_logger.error("There is no any services or yaml has not been parsed properly ")

    except Exception as error:
        app_root_logger.error(f"The current services cant be processed because {error}")
