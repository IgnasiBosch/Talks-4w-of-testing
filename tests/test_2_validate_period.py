import unittest

from src.code import validate_period


class TestCase(unittest.TestCase):

    def test_validate_period__true(self):
        data = {
            'period': {
                'start': 1447702772,
                'end': 1450726772
            }
        }

        result = validate_period(data)

        self.assertTrue(result)

    def test_validate_period__false(self):
        data = {
            'period': {
                'start': 1467702772,
                'end': 1450726772
            }
        }

        result = validate_period(data)

        self.assertFalse(result)

    def test_validate_period__key_error_when_no_period(self):
        data = {
            'some_other_key': 'some_other_value'
        }

        with self.assertRaises(KeyError):
            validate_period(data)
