import unittest

from src.code import validate_line


class TestCase(unittest.TestCase):

    def test_validate_line__true(self):
        data = {
            'period': {
                'end': 1450726772,
                'start': 1447702772
            },
            'plan': {
                'active': True
            }
        }

        result = validate_line(data)

        self.assertTrue(result)

    def test_validate_line__period_false_should_return_false(self):
        data = {
            'period': {
                'end': 1450726772,
                'start': 1467702772
            },
            'plan': {
                'active': True
            }
        }

        result = validate_line(data)

        self.assertFalse(result)

    def test_validate_line__plan_false_should_return_false(self):
        data = {
            'period': {
                'end': 1450726772,
                'start': 1447702772
            },
            'plan': {
                'active': False
            }
        }

        result = validate_line(data)

        self.assertFalse(result)

    def test_validate_line__plan_and_period_false_should_return_false(self):
        data = {
            'period': {
                'end': 1450726772,
                'start': 1467702772
            },
            'plan': {
                'active': False
            }
        }

        result = validate_line(data)

        self.assertFalse(result)
