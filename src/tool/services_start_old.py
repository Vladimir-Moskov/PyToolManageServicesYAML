"""
    Services start hierarchy creation / running
"""

from services import Services, Service
from typing import List, Dict
import asyncio
from config import *
from random import randint


def _create_deps_helper_dic(yaml_services: Services) -> Dict:
    """
        Create helper data structure
    :param yaml_services: all data as Services
    :return: helper dictionary for creation services hierarchy
    """
    services_with_depends = set()
    deps_helper_dic = {}

    # build up direct dependency dictionary - vere service all deps is key
    for value in yaml_services.services:
        if not value.deps or len(value.deps) == 0:
            key_t = tuple()
        else:
            services_with_depends.add(value.name)
            key_t = tuple(value.deps)

        new_val = deps_helper_dic.get(key_t, [])
        new_val.append(value)
        deps_helper_dic[key_t] = new_val

    return deps_helper_dic


def start_estimated_order(yaml_services: Services) -> List:
    """
        Generate estimated / abstract starting order where start service operation
        is synchronous an all services starts with the same time

       :param yaml_services:  all data as Services
       :return: array of arrays with services start order
    """
    deps_helper_dic = _create_deps_helper_dic(yaml_services)
    def_key = tuple()
    serv_to_start = set(x.name for x in deps_helper_dic[def_key])
    started_serv = set(serv_to_start)

    del deps_helper_dic[def_key]
    start_flow = [list(started_serv)]
    while len(deps_helper_dic) > 0:
        started_serv.update(next_to_start(start_flow, deps_helper_dic, serv_to_start, started_serv))

    return start_flow


def start_order(yaml_services: Services) -> List:
    """
        Generate "real-life" starting order where start service operation
        is NOT synchronous an all services can be started for any time

       :param yaml_services:  all data as Services
       :return: array of arrays with services start order
    """

    deps_helper_dic = _create_deps_helper_dic(yaml_services)
    def_key = tuple()
    started_serv = set()
    serv_to_start = set(x.name for x in deps_helper_dic[def_key])

    del deps_helper_dic[def_key]
    start_flow = [list(serv_to_start)]
    asyncio.run(start_all_service(start_flow, deps_helper_dic, serv_to_start, started_serv))

    return start_flow


def next_to_start(start_flow, deps_helper_dic, serv_to_start, started_serv) -> List[str]:
    """
        Get next available services for start

        :param start_flow: all services start order
        :param deps_helper_dic:
        :param serv_to_start: pending to start
        :param started_serv: already started

        :return: next pending to start
    """
    next_ready = []

    if len(deps_helper_dic) > 0:
        del_ready = []
        for key, value in deps_helper_dic.items():
            if set(key).issubset(started_serv):
                next_ready.extend(x.name for x in value)
                del_ready.append(key)
        for key in del_ready:
            del deps_helper_dic[key]
        if len(next_ready) > 0:
            start_flow.append(next_ready)
            serv_to_start.update(next_ready)
    return next_ready


async def start_all_service(start_flow, deps_helper_dic, serv_to_start, started_serv):
    """
        Run pending to start services

        :param start_flow: all services start order
        :param deps_helper_dic:
        :param serv_to_start: pending to start
        :param started_serv: already started
    """
    app_root_logger.info(" Server start_all_service - started")
    tasks = []
    for serv in list(serv_to_start):
        task1 = asyncio.create_task(start_serv_host(serv, start_flow, deps_helper_dic, serv_to_start, started_serv))
        tasks.append(task1)
        serv_to_start.remove(serv)
    await asyncio.gather(*tasks)


async def start_serv_host(serv, start_flow, deps_helper_dic, serv_to_start, started_serv):
    """
        Real start one specific service
    :param serv:
    :param start_flow: all services start order
    :param deps_helper_dic:
    :param serv_to_start: pending to start
    :param started_serv: already started

    """

    delay = randint(1, 4)
    app_root_logger.info(f" start_serv_host {serv} - started for {delay} sec")
    # replace this with REAL service start by start all hosts in parallel and wait for all started
    # just random sleep in order to simulate start of all hosts
    await asyncio.sleep(delay)
    started_serv.add(serv)

    app_root_logger.info(f" start_serv_host {serv} - end")
    next_pending = next_to_start(start_flow, deps_helper_dic, serv_to_start, started_serv)
    # add tasks in processing event loop
    if len(next_pending):
        await start_all_service(start_flow, deps_helper_dic, serv_to_start, started_serv)
