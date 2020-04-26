"""
    Services stop hierarchy creation / running
"""

# TODO: implement class based approach and get rid of 'too much' args in methods

from services import Services, ServiceDTO
from typing import List, Set
import asyncio
from config import *
from random import randint


def stop_estimated_order(yaml_services: Services) -> List:
    """
        Generate estimated / abstract stopping order where stop service operation
        is synchronous an all services starts with the same time

       :param yaml_services:  all data as Services
       :return: array of arrays with services stop order
    """

    stopped_serv: Set[str] = set(yaml_services.stop_root)
    serv_to_stop: Set[str] = set()  # all next potential services
    next_to_check: Set[str] = set()
    for serv_name in stopped_serv:
        next_to_check.update(yaml_services[serv_name].deps)

    stop_flow: List[List[str]] = [list(stopped_serv)]
    while len(next_to_check) > 0:
        just_stopped: Set[str] = set(next_to_stop(stop_flow, yaml_services, serv_to_stop, stopped_serv, next_to_check))
        stopped_serv.update(just_stopped)
        for serv_name in just_stopped:
            next_to_check.update(yaml_services[serv_name].deps)

    return stop_flow


def stop_order(yaml_services: Services) -> List:
    """
        Generate "real-life" stopping order where start service operation
        is NOT synchronous an all services can be stopped for any time

       :param yaml_services:  all data as Services
       :return: array of arrays with services stop order
    """
    stopped_serv: Set[str] = set()
    serv_to_stop: Set[str] = set(yaml_services.stop_root)
    stop_flow: List[List[str]] = [list(serv_to_stop)]
    next_to_check: Set[str] = set()
    asyncio.run(stop_all_service(stop_flow, yaml_services, serv_to_stop, stopped_serv, next_to_check))

    return stop_flow


def next_to_stop(stop_flow: List[List[str]],
                 yaml_services: Services,
                 serv_to_stop: Set[str],
                 stopped_serv: Set[str],
                 next_to_check: Set[str]) -> List[str]:
    """
        Get next available services for stop

        :param stop_flow: all services stop order
        :param yaml_services: services structure
        :param serv_to_stop: pending to stop
        :param stopped_serv: already stopped
        :param next_to_check: pending to check is it can be ready to stop after next service will be stopped

        :return: next ready to stop
    """
    next_ready: List[str] = []
    serv: ServiceDTO
    serv_to_del: Set[str] = set()
    for key in next_to_check:
        serv = yaml_services[key]
        if set(serv.dependants).issubset(stopped_serv):
            next_ready.append(key)
            serv_to_del.add(key)

    serv_to_stop.update(next_ready)
    stop_flow.append(next_ready)
    next_to_check -= serv_to_del
    return next_ready


async def stop_all_service(stop_flow: List[List[str]],
                           yaml_services: Services,
                           serv_to_stop: Set[str],
                           stopped_serv: Set[str],
                           next_to_check: Set[str]):
    """
      Run pending to stop services

        :param stop_flow: all services stop order
        :param yaml_services: services structure
        :param serv_to_stop: pending to stop
        :param stopped_serv: already stopped
        :param next_to_check: pending to check is it can be ready to stop after next service will be stopped

    """
    app_root_logger.info(" Server stop_all_service - started")
    tasks = []
    for serv in list(serv_to_stop):
        task1 = asyncio.create_task(stop_serv_host(serv, stop_flow, yaml_services, serv_to_stop, stopped_serv, next_to_check))
        tasks.append(task1)
        serv_to_stop.remove(serv)
    await asyncio.gather(*tasks)


async def stop_serv_host(serv: str,
                         stop_flow: List[List[str]],
                         yaml_services: Services,
                         serv_to_stop: Set[str],
                         stopped_serv: Set[str],
                         next_to_check: Set[str]):
    """
      Real stop one specific service

        :param stop_flow: all services stop order
        :param yaml_services: services structure
        :param serv_to_stop: pending to stop
        :param stopped_serv: already stopped
        :param next_to_check: pending to check is it can be ready to stop after next service will be stopped
    """
    # random delay
    delay = randint(1, 4)
    app_root_logger.info(f" stop_serv_host {serv} - stopped for {delay} sec")
    # replace this with REAL service start by stopped all hosts in parallel and wait for all started
    # just random sleep in order to simulate stop of all hosts
    await asyncio.sleep(delay)
    stopped_serv.add(serv)
    next_to_check.update(yaml_services[serv].deps)

    app_root_logger.info(f" stop_serv_host {serv} - end")
    next_pending = next_to_stop(stop_flow, yaml_services, serv_to_stop, stopped_serv, next_to_check)
    # add tasks in processing event loop
    if len(next_pending):
        await stop_all_service(stop_flow, yaml_services, serv_to_stop, stopped_serv, next_to_check)
