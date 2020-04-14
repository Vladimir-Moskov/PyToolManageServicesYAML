"""
    Few simple tests for services_start (test files from sc/test/resources/...)

    Just very basic verification
    TODO: Implement test cases properly
"""

import os
import pytest
from services_start import start_order, start_estimated_order
from yaml_parser import parse_yaml_services
from services import Services

yaml_path = os.path.abspath('./resources/')


def test_start_estimated_order_example():
    """
        Just simple check if expected == actual for test .yaml file
    :return:
    """
    expected_result = [['mysql', 'zookeeper'], ['kibana'], ['fullhouse']]
    services: Services = parse_yaml_services(yaml_path, 'example.yaml')
    result = start_estimated_order(services)
    assert len(result) == len(expected_result)
    for i in range(len(result)):
        assert set(result[i]) == set(expected_result[i])


def test_start_estimated_order_services():
    """
      Just simple check if expected == actual for test .yaml file
      :return:
    """
    expected_result = [
        ['mysql', 'zookeeper', 'elasticsearch'],
        ['kibana', 'hadoop-namenode'],
        ['hbase-master'],
        ['fullhouse'],
        ['dashboard']
    ]
    services: Services = parse_yaml_services(yaml_path, 'services.yaml')
    result = start_estimated_order(services)
    assert len(result) == len(expected_result)
    for i in range(len(result)):
        assert set(result[i]) == set(expected_result[i])

