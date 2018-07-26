import unittest
from unittest.mock import Mock, patch, call

from src.code_1 import LineItemValidator, InvoiceValidator


class LineItemValidatorTestCase(unittest.TestCase):
    def setUp(self):
        # System Under Test class
        self.sut_cls = LineItemValidator

    def test_validate_period__true(self):
        data = {
            'period': {
                'start': 1447702772,
                'end': 1450726772
            }
        }

        line_item_validator = self.sut_cls(data)
        result = line_item_validator._is_valid_period()

        self.assertTrue(result)

    def test_validate_period__false(self):
        data = {
            'period': {
                'start': 1467702772,
                'end': 1450726772
            }
        }

        line_item_validator = self.sut_cls(data)
        result = line_item_validator._is_valid_period()

        self.assertFalse(result)

    def test_is_valid_plan__true(self):
        data = {
            'plan': {
                'active': True
            }
        }

        line_item_validator = self.sut_cls(data)
        result = line_item_validator._is_valid_plan()

        self.assertTrue(result)

    def test_is_valid_plan__false(self):
        data = {
            'plan': {
                'active': False
            }
        }

        line_item_validator = self.sut_cls(data)
        result = line_item_validator._is_valid_plan()

        self.assertFalse(result)

    def test_is_valid__should_call_validators(self):
        data = 'dummy data'

        line_item_validator = self.sut_cls(data)
        line_item_validator._is_valid_period = Mock()
        line_item_validator._is_valid_plan = Mock()

        line_item_validator.is_valid()

        line_item_validator._is_valid_period.assert_called_once_with()
        line_item_validator._is_valid_plan.assert_called_once_with()

    def test_is_valid__false_not_called_further_validators(self):
        data = 'dummy data'

        line_item_validator = self.sut_cls(data)
        line_item_validator._is_valid_period = Mock()
        line_item_validator._is_valid_plan = Mock()

        line_item_validator._is_valid_period.return_value = False

        self.assertFalse(line_item_validator.is_valid())
        line_item_validator._is_valid_plan.assert_not_called()


class InvoiceTestCase(unittest.TestCase):
    def setUp(self):
        # System Under Test class
        self.sut_cls = InvoiceValidator

    def test_is_closed__true(self):
        data = {
            'closed': True
        }

        invoice = self.sut_cls(data)
        result = invoice.is_closed()

        self.assertTrue(result)

    def test_is_closed__false(self):
        data = {
            'closed': False
        }

        invoice = self.sut_cls(data)
        result = invoice.is_closed()

        self.assertFalse(result)

    def test_is_paid__true(self):
        data = {
            'paid': True
        }

        invoice = self.sut_cls(data)
        result = invoice.is_paid()

        self.assertTrue(result)

    def test_is_paid__false(self):
        data = {
            'paid': False
        }

        invoice = self.sut_cls(data)
        result = invoice.is_paid()

        self.assertFalse(result)

    def test_is_valid__should_call_validators(self):
        data = 'dummy data'

        invoice = self.sut_cls(data)
        invoice.is_paid = Mock()
        invoice.is_closed = Mock()
        invoice._are_valid_lines = Mock()

        invoice.is_valid()

        invoice._are_valid_lines.assert_called_once_with()
        invoice.is_closed.assert_called_once_with()
        invoice.is_paid.assert_called_once_with()

    def test_is_valid__false_not_called_further_validators(self):
        data = 'dummy data'

        invoice = self.sut_cls(data)
        invoice.is_paid = Mock()
        invoice.is_closed = Mock()
        invoice._are_valid_lines = Mock()
        invoice.is_paid.return_value = False

        result = invoice.is_valid()

        self.assertFalse(result)
        invoice.is_closed.assert_not_called()
        invoice._are_valid_lines.assert_not_called()

    @patch('src.code_1.LineItemValidator')
    def test_are_valid_lines_should_call_line_validators(
            self, line_item_validator_mocked
    ):
        data = {
            'lines': {
                'data': ['line_1', 'line_2']
            }
        }

        expected_calls = [call('line_1'), call('line_2')]

        invoice = self.sut_cls(data)
        invoice._are_valid_lines()

        self.assertListEqual(
            line_item_validator_mocked.call_args_list, expected_calls
        )

    @patch('src.code_1.LineItemValidator')
    def test_are_valid_lines_should_call_only_one_validator_on_first_invalid(
            self, line_item_validator_mocked
    ):
        data = {
            'lines': {
                'data': ['line_1', 'line_2']
            }
        }

        expected_calls = [call('line_1')]

        first_validator = Mock()
        first_validator.is_valid.return_value = False
        line_item_validator_mocked.side_effect = [first_validator]

        invoice = self.sut_cls(data)
        result = invoice._are_valid_lines()

        self.assertFalse(result)
        self.assertListEqual(
            line_item_validator_mocked.call_args_list, expected_calls
        )
