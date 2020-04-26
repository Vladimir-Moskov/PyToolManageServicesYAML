"""
    Services stop hierarchy creation / running
"""

from services import Services, ServiceDTO
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
    deps_helper_dic = {}

    # build up reversed dependency dictionary - vere service all dependants is key
    for value in yaml_services.services:
        if not value.dependants or len(value.dependants) == 0:
            key_t = tuple()
        else:
            key_t = tuple(value.dependants)

        new_val = deps_helper_dic.get(key_t, [])
        new_val.append(value)
        deps_helper_dic[key_t] = new_val

    return deps_helper_dic


def stop_estimated_order(yaml_services: Services) -> List:
    """
        Generate estimated / abstract stopping order where stop service operation
        is synchronous an all services starts with the same time

       :param yaml_services:  all data as Services
       :return: array of arrays with services stop order
    """
    deps_helper_dic = _create_deps_helper_dic(yaml_services)

    def_key = tuple()
    serv_to_stop = set(x.name for x in deps_helper_dic[def_key])
    del deps_helper_dic[def_key]
    stop_flow = [list(serv_to_stop)]
    stopped_serv = set(serv_to_stop)

    while len(deps_helper_dic) > 0:
        stopped_serv.update(next_to_stop(stop_flow, deps_helper_dic, serv_to_stop, stopped_serv))

    return stop_flow


def stop_order(yaml_services: Services) -> List:
    """
        Generate "real-life" stopping order where start service operation
        is NOT synchronous an all services can be stopped for any time

       :param yaml_services:  all data as Services
       :return: array of arrays with services stop order
    """
    deps_helper_dic = _create_deps_helper_dic(yaml_services)

    #
    def_key = tuple()
    serv_to_stop = set(x.name for x in deps_helper_dic[def_key])
    del deps_helper_dic[def_key]
    stop_flow = [list(serv_to_stop)]
    stopped_serv = set()
    asyncio.run(stop_all_service(stop_flow, deps_helper_dic, serv_to_stop, stopped_serv))

    return stop_flow


def next_to_stop(stop_flow, deps_helper_dic, serv_to_stop, stopped_serv) -> List[str]:
    """
        Get next available services for stop

        :param stop_flow: all services stop order
        :param deps_helper_dic:
        :param serv_to_stop: pending to stop
        :param stopped_serv: already stopped

        :return: next pending to stop
    """
    next_ready = []

    if len(deps_helper_dic) > 0:
        del_ready = []
        for key, value in deps_helper_dic.items():
            if set(key).issubset(stopped_serv):
                next_ready.extend(x.name for x in value)
                del_ready.append(key)
        for key in del_ready:
            del deps_helper_dic[key]
        if len(next_ready) > 0:
            stop_flow.append(next_ready)
            serv_to_stop.update(next_ready)

    return next_ready


async def stop_all_service(stop_flow, deps_helper_dic, serv_to_stop, stopped_serv):
    """
      Run pending to stop services

        :param stop_flow: all services stop order
        :param deps_helper_dic:
        :param serv_to_stop: pending to stop
        :param stopped_serv: already stopped
    """
    app_root_logger.info(" Server stop_all_service - started")
    tasks = []
    for serv in list(serv_to_stop):
        task1 = asyncio.create_task(stop_serv_host(serv, stop_flow, deps_helper_dic, serv_to_stop, stopped_serv))
        tasks.append(task1)
        serv_to_stop.remove(serv)
    await asyncio.gather(*tasks)


async def stop_serv_host(serv, stop_flow, deps_helper_dic, serv_to_stop, stopped_serv):
    """
      Real stop one specific service

        :param stop_flow: all services stop order
        :param deps_helper_dic:
        :param serv_to_stop: pending to stop
        :param stopped_serv: already stopped
    """
    delay = randint(1, 4)
    app_root_logger.info(f" stop_serv_host {serv} - stopped for {delay} sec")
    # replace this with REAL service start by stopped all hosts in parallel and wait for all started
    # just random sleep in order to simulate stop of all hosts
    await asyncio.sleep(delay)
    stopped_serv.add(serv)

    app_root_logger.info(f" stop_serv_host {serv} - end")
    next_pending = next_to_stop(stop_flow, deps_helper_dic, serv_to_stop, stopped_serv)
    # add tasks in processing event loop
    if len(next_pending):
        await stop_all_service(stop_flow, deps_helper_dic, serv_to_stop, stopped_serv)
