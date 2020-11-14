""" Allow for various configuration options in python
"""
import os
import re
import copy
from typing import List, Optional
import yaml


class EnvironmentAdapter:
    """ Configuration that will swap out meta variables with environment variables values
    """

    DEFALT_VALUE: str = '*****'
    DEFALT_KEY: str = 'environment_variable'

    @staticmethod
    def inline_replace(line: str) -> str:
        """ Replacing ${ENV} with value
            :param line str: will replace any `${...}` values with variable
            :return: return with swapped value
            :rtype: str
        """
        _line: str = line
        for match in re.finditer(r'\${[^}]*}', line):
            _segment = line[match.start(): match.end()]
            _value = os.getenv(_segment[2:-1], EnvironmentAdapter.DEFALT_VALUE)
            _line = _line.replace(_segment, _value)
        return _line

    @staticmethod
    def replace(data: dict) -> dict:
        """ resolve a dict config with environment variables
            the will inject the values for environment variable: 'name'
            using os.getenv('name')
        """
        config: dict = copy.deepcopy(data)
        for key, value in config.items():
            if isinstance(value, dict) and EnvironmentAdapter.DEFALT_KEY in value.keys():
                config[key] = os.getenv(value[EnvironmentAdapter.DEFALT_KEY],
                                        EnvironmentAdapter.DEFALT_VALUE)
                continue
            if isinstance(value, dict):
                config[key] = EnvironmentAdapter.replace(value)
                continue
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        config[key][index] = EnvironmentAdapter.replace(item)
                continue
            if isinstance(value, str):
                config[key] = EnvironmentAdapter.inline_replace(value)
                continue
        return config


class YamlConfiguration(EnvironmentAdapter):
    """ Load Yaml Configuration
    """

    data: List[dict]
    index: int

    def __init__(self, yaml_file: str, index: int = 0):
        """ Loads Yaml config; if multiple configs in same file
            use index to select
        """
        self.data = self.load(yaml_file)
        self.set_active_index(index)

    def valid_index(self, index: int) -> bool:
        """ Checks if index is in range
        """
        return len(self.data) >= index >= 0

    def set_active_index(self, index: int):
        """ Set active index
        """
        if not self.valid_index(index):
            raise IndexError("Index out of range")

        self.index = index

    def config(self,
               section: Optional[str] = None,
               safe: bool = False,
               index: Optional[int] = None) -> dict:
        """
            Loads the configuration file
            :param section str: return a section of the config
            :param safe bool: return the configuration unaltered
            :param Optional[int] index: index of yaml document you want to read from, \
                                        if None will use :const:`self.index`
            :return: yaml configuration as a dictionary
            :rtype: dict
        """
        if not index or not self.valid_index(index):
            index = self.index

        _data = self.data[index][section] if section else self.data[index]

        return _data if safe else self.replace(_data)

    @staticmethod
    def load(yaml_file: str) -> List[dict]:
        """
            Read the yaml file into python
            :return: list of all yaml configs
            :rtype: list
            :raise FileNotFoundError: yaml file could not be found on disk
            :raise yaml.error.YAMLError: yaml file is malformed
        """
        if not os.path.isfile(yaml_file):
            raise FileNotFoundError("Yaml file is not found at path")

        with open(yaml_file, 'r') as file:
            yaml_configs = list(yaml.full_load_all(file))
            return yaml_configs
