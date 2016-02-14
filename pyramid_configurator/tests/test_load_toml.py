#
import os
import unittest

from pyramid_configurator.loader.toml import load_toml_with_inherit


class LoadTomlTestCase(unittest.TestCase):
    TOML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toml')

    def test_load_simple_toml_file(self):
        toml_dict = load_toml_with_inherit(
            'simple.toml', base_dir=self.TOML_DIR,
        )
        expect_result = {
            'simple': {
                'first': 1,
                'second': 'two',
            }
        }
        self.assertEqual(toml_dict, expect_result)

    def test_load_inherit_simple_toml_file(self):
        toml_dict = load_toml_with_inherit(
            'inherit_simple.toml', base_dir=self.TOML_DIR,
        )
        expect_result = {
            'simple': {
                'first': 5,
                'second': 'two',
                'third': True,
            }
        }
        self.assertEqual(toml_dict, expect_result)

    def test_load_inherit_missing_optional(self):
        toml_dict = load_toml_with_inherit(
            'inherit_missing_optional.toml', base_dir=self.TOML_DIR,
        )
        expect_result = {
            'simple': {
                'first': 5,
                'second': 'two',
                'fourth': [4, 5],
            }
        }
        self.assertEqual(toml_dict, expect_result)

    def test_load_inherit_missing_required(self):
        self.assertRaises(
            IOError,
            load_toml_with_inherit,
            'inherit_missing_required.toml', base_dir=self.TOML_DIR,
        )

    def test_load_inherit_2level(self):
        toml_dict = load_toml_with_inherit(
            'inherit_2level.toml', base_dir=self.TOML_DIR,
        )
        expect_result = {
            'simple': {
                'first': 8,
                'second': 'two',
                'third': 0,
                'fourth': [4, 5],
            }
        }
        self.assertEqual(toml_dict, expect_result)
