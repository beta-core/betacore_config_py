""" Unit test for control
"""
import os
import pathlib
import unittest
from unittest import mock
from yaml.error import YAMLError
from betacore.config import config


class TestEnvironmentAdapter(unittest.TestCase):
    """ Test adapter
    """

    def test_inline_complex(self):
        """ In line complex string
        """
        value = 'value'
        comp = 'complex'
        with mock.patch.dict('os.environ', {'cc': comp, 'vv': value}, clear=True):
            result = config.EnvironmentAdapter.inline_replace("my-${cc}-${vv}")
            self.assertEqual(result, f'my-{comp}-{value}')

    def test_inline_simple(self):
        """ inline simple string
        """
        value = 'value'
        with mock.patch.dict('os.environ', {'vv': value}, clear=True):
            result = config.EnvironmentAdapter.inline_replace("${vv}")
            self.assertEqual(result, f'{value}')

    def test_replace(self):
        """ Test basic replace
        """
        value = 'value'
        with mock.patch.dict('os.environ', {'vv': value}, clear=True):
            result = config.EnvironmentAdapter.replace({
                "test": {
                    config.EnvironmentAdapter.DEFALT_KEY: "vv"
                }
            })
            self.assertDictEqual(result, {"test": value})

    def test_replace_list(self):
        """ Test replace with a list
        """
        value = 'value'
        with mock.patch.dict('os.environ', {'vv': value}, clear=True):
            result = config.EnvironmentAdapter.replace({
                "items": [
                    {
                        "test": {
                            config.EnvironmentAdapter.DEFALT_KEY: "vv"
                        }
                    }]
                })
            self.assertDictEqual(result, {'items': [{'test': value}]})
class TestYamlConfiguration(unittest.TestCase):
    """ Verify configration file loads
    """

    def yaml_path(self, name) -> str:
        """ Load test file
        """
        path = pathlib.Path(__file__).parent.absolute()
        return os.path.join(path, '../data', name)

    def test_set_active_index(self):
        """ Test load file
        """
        path = self.yaml_path('test.yml')
        _config = config.YamlConfiguration(path)
        self.assertIsNotNone(_config)
        self.assertRaises(IndexError, _config.set_active_index, -1)
        self.assertRaises(IndexError, _config.set_active_index, 10)
    def test_load_file(self):
        """ Test load file
        """
        path = self.yaml_path('test.yml')
        data = config.YamlConfiguration.load(path)
        self.assertIsNotNone(data)

    def test_resolve_single(self):
        """ Test replacement
        """
        variable = 'test_resolve_single'
        os.environ['TEST_ENV'] = variable
        path = self.yaml_path('single.yml')
        resolve = config.YamlConfiguration(path).config('test')
        expected = {"env": variable}
        self.assertDictEqual(resolve, expected)

    def test_resolve(self):
        """ Test replacement
        """
        variable = 'test_resolve'
        os.environ['TEST_ENV'] = variable
        path = self.yaml_path('test.yml')
        data = config.YamlConfiguration.load(path)
        resolve = config.YamlConfiguration.replace(data[0])
        expected = {
            'test': {
                "list": ["a", "b", "c"],
                "env": variable,
                "level": {"two": {"a": "a"}}
            }

        }
        self.assertDictEqual(resolve, expected)

    def test_load_file_not_found(self):
        """ Test load file
        """
        path = self.yaml_path('q.yml')
        self.assertRaises(FileNotFoundError,
                          config.YamlConfiguration.load, path)

    def test_load_file_bad_file(self):
        """ Test load file
        """
        path=self.yaml_path('bad.yml')
        self.assertRaises(YAMLError, config.YamlConfiguration.load, path)
