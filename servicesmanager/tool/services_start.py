"""
    Services start hierarchy creation / running
"""

# TODO: implement class based approach and get rid of 'too much' args in methods

from services import Services, ServiceDTO
from typing import List, Set
import asyncio
from config import *
from random import randint


def start_estimated_order(yaml_services: Services) -> List:
    """
        Generate estimated / abstract starting order where start service operation
        is synchronous an all services starts with the same time

       :param yaml_services:  all data as Services
       :return: array of arrays with services start order
    """

    started_serv: Set[str] = set(yaml_services.start_root)
    serv_to_start: Set[str] = set()  # all next potential services
    next_to_check: Set[str] = set()
    for serv_name in started_serv:
        next_to_check.update(yaml_services[serv_name].dependants)

    start_flow: List[List[str]] = [list(started_serv)]
    while len(next_to_check) > 0:
        just_started: Set[str] = set(next_to_start(start_flow, yaml_services, serv_to_start, started_serv, next_to_check))
        started_serv.update(just_started)
        for serv_name in just_started:
            next_to_check.update(yaml_services[serv_name].dependants)

    return start_flow


def start_order(yaml_services: Services) -> List:
    """
        Generate "real-life" starting order where start service operation
        is NOT synchronous an all services can be started for any time

       :param yaml_services:  all data as Services
       :return: array of arrays with services start order
    """

    started_serv: Set[str] = set()
    serv_to_start: Set[str] = set(yaml_services.start_root)
    start_flow: List[List[str]] = [list(serv_to_start)]
    next_to_check: Set[str] = set()
    asyncio.run(start_all_service(start_flow, yaml_services, serv_to_start, started_serv, next_to_check))

    return start_flow


def next_to_start(start_flow: List[List[str]],
                  yaml_services: Services,
                  serv_to_start: Set[str],
                  started_serv: Set[str],
                  next_to_check: Set[str] ) -> List[str]:
    """
        Get next available services for start

        :param start_flow: all services start order
        :param yaml_services: services structure
        :param serv_to_start: pending to start
        :param started_serv: already started
        :param next_to_check: pending to check is it can be ready to start after next service will be started

        :return: next ready to start
    """
    next_ready: List[str] = []
    serv: ServiceDTO
    serv_to_del: Set[str] = set()
    for key in next_to_check:
        serv = yaml_services[key]
        if set(serv.deps).issubset(started_serv):
            next_ready.append(key)
            serv_to_del.add(key)

    serv_to_start.update(next_ready)
    start_flow.append(next_ready)
    next_to_check -= serv_to_del
    return next_ready


async def start_all_service(start_flow: List[List[str]],
                            yaml_services: Services,
                            serv_to_start: Set[str],
                            started_serv: Set[str],
                            next_to_check: Set[str]):
    """
        Run pending to start services

        :param start_flow: all services start order
        :param yaml_services: services structure
        :param serv_to_start: pending to start
        :param started_serv: already started
        :param next_to_check: pending to check is it can be ready to start after next service will be started

    """
    app_root_logger.info(" Server start_all_service - started")
    tasks = []
    for serv in list(serv_to_start):
        task1 = asyncio.create_task(start_serv_host(serv, start_flow, yaml_services, serv_to_start, started_serv, next_to_check))
        tasks.append(task1)
        serv_to_start.remove(serv)
    await asyncio.gather(*tasks)


async def start_serv_host(serv: str,
                          start_flow: List[List[str]],
                          yaml_services: Services,
                          serv_to_start: Set[str],
                          started_serv: Set[str],
                          next_to_check: Set[str]):
    """
        Real start one specific service
        :param serv: current started service
        :param start_flow: all services start order
        :param yaml_services: services structure
        :param serv_to_start: pending to start
        :param started_serv: already started
        :param next_to_check: pending to check is it can be ready to start after next service will be started
    """
    # random delay
    delay = randint(1, 4)
    app_root_logger.info(f" start_serv_host {serv} - started for {delay} sec")
    # replace this with REAL service start by start all hosts in parallel and wait for all started
    # just random sleep in order to simulate start of all hosts
    await asyncio.sleep(delay)
    started_serv.add(serv)
    next_to_check.update(yaml_services[serv].dependants)

    app_root_logger.info(f" start_serv_host {serv} - end")
    next_pending = next_to_start(start_flow, yaml_services, serv_to_start, started_serv, next_to_check)
    # add tasks in processing event loop if there are any service can be started
    if len(next_pending):
        await start_all_service(start_flow, yaml_services, serv_to_start, started_serv, next_to_check)
