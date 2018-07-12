import unittest
from unittest.mock import patch

from src.code import validate_line


class TestCase(unittest.TestCase):

    def setUp(self):
        self.patcher_validate_period = patch('src.code.validate_period')
        self.mocked_validate_period = self.patcher_validate_period.start()

        self.patcher_validate_plan = patch('src.code.validate_plan')
        self.mocked_validate_plan = self.patcher_validate_plan.start()

        self.data = {
            'some_key': 'some_value'
        }

    def tearDown(self):
        self.patcher_validate_period.stop()
        self.patcher_validate_plan.stop()

    def test_validate_line__should_call_validators(self):
        """
        Assert validate_line calls individual validators with provided data
        """
        validate_line(self.data)

        self.mocked_validate_period.assert_called_once_with(self.data)
        self.mocked_validate_plan.assert_called_once_with(self.data)

    def test_validate_line__should_return_true(self):
        self.mocked_validate_period.return_value = True
        self.mocked_validate_plan.return_value = True

        result = validate_line(self.data)

        self.assertTrue(result)

    def test_validate_line__false_period_should_return_false_and_no_call_validate_plan(self):
        self.mocked_validate_period.return_value = False
        self.mocked_validate_plan.return_value = True

        result = validate_line(self.data)

        self.assertFalse(result)
        self.mocked_validate_plan.assert_not_called()

    def test_validate_line__false_plan_should_return_false(self):
        self.mocked_validate_period.return_value = True
        self.mocked_validate_plan.return_value = False

        result = validate_line(self.data)

        self.assertFalse(result)

