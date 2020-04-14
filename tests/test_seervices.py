import os
import pytest
from yaml_parser import parse_yaml_services
from services import Services

yaml_path = os.path.abspath('./resources/')


def test_services_parse_example():
    """
       Just simple check if  test .yaml file parsing properly
      :return:
      """
    expected_result_len = 4
    services: Services = parse_yaml_services(yaml_path, 'example.yaml')
    assert expected_result_len == len(services.services)


def test_services_parse_example_with_circular_dep():
    """
       Just simple check if  test .yaml file parsing properly - for case with  circular dependencies
      :return:
      """
    try:
        services: Services = parse_yaml_services(yaml_path, 'example_circular_dep.yaml')
    except Exception as error:
        assert True
    else:
        assert False


def test_services_parse():
    """
       Just simple check if  test .yaml file parsing properly
      :return:
      """
    expected_result_len = 8
    services: Services = parse_yaml_services(yaml_path, 'services.yaml')
    assert expected_result_len == len(services.services)


def test_services_parse_with_circular_dep():
    """
       Just simple check if  test .yaml file parsing properly - for case with  circular dependencies
      :return:
      """
    try:
        services: Services = parse_yaml_services(yaml_path, 'services_circular_dep.yaml')
    except Exception as error:
        assert True
    else:
        assert False
