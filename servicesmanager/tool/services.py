"""
    Serialized DTO for services from  yaml file
"""
from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict


@dataclass
class ServiceDTO:
    """
        Service DTO - data class, support only current fields, the rest field will be ignored
    """
    name: str
    hosts: List[str]
    deps: List[str]
    dependants: List[str]  # additional data field to store all dependants

    def __init__(self, name: str, **entry):
        self.name = name
        self.hosts = None
        self.deps = []  # dependencies
        self.dependants = []  # dependants
        self.__dict__.update(entry)
        if self.deps:
            self.deps.sort()


class Services:
    """
          Services DTO - data class, to store yaml file as dictionary
    """
    def __init__(self, **entries):
        # all services as array - has not been used and became redundant, could be deleted
        # create a list of services with predefined size
        self.services: List[ServiceDTO] = [None]*len(entries)
        # for case of start / stop flow - will be used as helpers
        self.start_root: List[str] = []
        self.stop_root: List[str] = []

        # set up dependants
        for key, value in entries.items():
            if 'deps' in value:
                for dep in value['deps']:
                    if 'dependants' not in entries[dep]:
                        entries[dep]['dependants'] = [key]
                    else:
                        entries[dep]['dependants'].append(key)

        # does not matter is it stopping or starting flow -
        # circular dependencies will behave in the same way,
        # so check in start direction only
        if self.has_circular_dependencies(entries):
            raise Exception('Current yaml file has circular dependencies in services structure')

        # set up all services as dic for optimized asses
        for i, item in enumerate(entries.items()):
            key, value = item
            new_service: ServiceDTO = ServiceDTO(key,  **value)
            self.services[i] = new_service
            setattr(self, key, self.services[i])
            # set up root for case of start / stop flow
            if len(new_service.deps) == 0:
                self.start_root.append(new_service.name)
            if len(new_service.dependants) == 0:
                self.stop_root.append(new_service.name)

    def __getitem__(self, key) -> ServiceDTO:
        """
        Implement subscriptable interface in order to get service by name
        :param key: service name
        :return: Service item
        """
        if isinstance(self.__dict__[key], ServiceDTO):
            return self.__dict__[key]
        else:
            return None

    def __repr__(self) -> str:
        return f"Services size = {len(self.services)} \n {repr(self.services)}"

    @classmethod
    def has_circular_dependencies(cls, entries: Dict) -> bool:
        """
            It may be done with help of lib, but according requirements
              ' it is not allowed to use Python libraries for graph representation',
           So here is custom cycle detection implementation.

           Find circular dependencies in given hierarchy of services
           Just good old  DFS  Traversal can be used to detect a circular dependencies
           in order to validate starting / stopping flow
            Best possible runtime / time complexity
            O(S+C), where S is number of services, C is number of connections / dependencies

        :return: validation result - Returns true if yaml services have circular_dependencies
        """
        visited_serv_dic = defaultdict(bool)
        recursive_serv_dic = defaultdict(bool)

        for key, value in entries.items():
            if not visited_serv_dic[key]:
                # Enter in recursion - start go deep in current branch
                if cls.__circular_dependencies_recursive(key, entries, visited_serv_dic, recursive_serv_dic):
                    return True
        return False

    @classmethod
    def __circular_dependencies_recursive(cls,
                                          serv_name: str,
                                          entries: Dict,
                                          visited_serv_dic: Dict,
                                          recursive_serv_dic: Dict) -> bool:
        """

        :param serv_name: current service for check
        :param visited_serv_dic: all visited services
        :param recursive_serv_dic: current services visited in branch / recursion

        :return: validation result - Returns true if yaml services have circular_dependencies
        """
        # Set current serv_name as visited and save as entered in recursion
        visited_serv_dic[serv_name] = True
        recursive_serv_dic[serv_name] = True

        # Check all  dependants
        # if dependant is visited and in recursion
        # then there is circular dependencies
        dependants = entries[serv_name].get('dependants', [])
        for dependant in dependants:
            if visited_serv_dic[dependant] == False:
                if cls.__circular_dependencies_recursive(dependant, entries, visited_serv_dic, recursive_serv_dic):
                    return True
            elif recursive_serv_dic[dependant]:
                return True

        #  save as not in recursion any more
        recursive_serv_dic[serv_name] = False
        return False
