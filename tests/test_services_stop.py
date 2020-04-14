"""
    Few simple tests for services_start (test files from sc/test/resources/...)

    Just very basic verification
    TODO: Implement test cases properly
"""

import os
import pytest
from services_stop import stop_estimated_order
from yaml_parser import parse_yaml_services
from services import Services

yaml_path = os.path.abspath('./resources/')


def test_stop_estimated_order_example():
    """
       Just simple check if expected == actual for test .yaml file
      :return:
      """
    expected_result = [['fullhouse'], ['kibana', 'zookeeper'], ['mysql'], ]
    services: Services = parse_yaml_services(yaml_path, 'example.yaml')
    result = stop_estimated_order(services)
    assert len(result) == len(expected_result)
    for i in range(len(result)):
        assert set(result[i]) == set(expected_result[i])


def test_stop_estimated_order_services():
    """
      Just simple check if expected == actual for test .yaml file
      :return:
    """
    expected_result = [
        ['kibana', 'dashboard'],
        ['fullhouse'],
        ['mysql', 'hbase-master',  'elasticsearch'],
        ['hadoop-namenode'],
        ['zookeeper']
    ]

    services: Services = parse_yaml_services(yaml_path, 'services.yaml')
    result = stop_estimated_order(services)
    assert len(result) == len(expected_result)
    for i in range(len(result)):
        assert set(result[i]) == set(expected_result[i])