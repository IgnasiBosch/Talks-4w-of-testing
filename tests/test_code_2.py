import unittest
from unittest.mock import Mock, call

from freezegun import freeze_time

from src.code_2 import SubscriptionValidator, PromotionValidator, \
    LineItemValidator, Invoice


class SubscriptionValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = SubscriptionValidator()

    def test_validate_period__true(self):
        data = {
            'period': {
                'start': 1447702772,
                'end': 1450726772
            }
        }

        result = self.validator._is_valid_period(data)

        self.assertTrue(result)

    def test_validate_period__false(self):
        data = {
            'period': {
                'start': 1467702772,
                'end': 1450726772
            }
        }

        result = self.validator._is_valid_period(data)

        self.assertFalse(result)

    def test_is_valid_plan__true(self):
        data = {
            'plan': {
                'active': True
            }
        }

        result = self.validator._is_valid_plan(data)

        self.assertTrue(result)

    def test_is_valid_plan__false(self):
        data = {
            'plan': {
                'active': False
            }
        }

        result = self.validator._is_valid_plan(data)

        self.assertFalse(result)

    def test_is_valid__should_call_validators_with_same_data(self):
        data = 'dummy data'

        self.validator._is_valid_period = Mock()
        self.validator._is_valid_plan = Mock()

        self.validator.is_valid(data)

        self.validator._is_valid_period.assert_called_once_with(data)
        self.validator._is_valid_plan.assert_called_once_with(data)

    def test_is_valid__false_should_not_call_further_validators(self):
        data = 'dummy data'

        self.validator._is_valid_period = Mock()
        self.validator._is_valid_plan = Mock()
        self.validator._is_valid_period.return_value = False

        result = self.validator.is_valid(data)

        self.assertFalse(result)
        self.validator._is_valid_plan.assert_not_called()


class PromotionValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = PromotionValidator()

    @freeze_time('2018-07-27 12:00:00')
    def test_is_valid__true(self):
        data = {
            'valid_until': '2018-07-30 00:00:00'
        }

        result = self.validator.is_valid(data)

        self.assertTrue(result)

    @freeze_time('2018-07-27 12:00:00')
    def test_is_valid__false(self):
        data = {
            'valid_until': '2018-07-27 11:59:59'
        }

        result = self.validator.is_valid(data)

        self.assertFalse(result)


class LineItemValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = LineItemValidator()

    def test_is_valid__existing_type_should_return_validator(self):
        data = {
            'type': 'test_type'
        }

        mocked_validator = Mock()
        self.validator.validators_by_type['test_type'] = mocked_validator

        self.validator.is_valid(data)

        mocked_validator.is_valid.assert_called_once_with(data)

    def test_is_valid__non_existing_type_should_raise_error(self):
        data = {
            'type': 'test_type_non_existing'
        }

        with self.assertRaises(TypeError):
            self.validator.is_valid(data)


class InvoiceTestCase(unittest.TestCase):
    def setUp(self):
        # System Under Test class
        self.sut_cls = Invoice
        self.line_item_validator = Mock()

    def test_is_closed__true(self):
        data = {
            'closed': True
        }

        invoice = self.sut_cls(data, self.line_item_validator)
        result = invoice.is_closed()

        self.assertTrue(result)

    def test_is_closed__false(self):
        data = {
            'closed': False
        }

        invoice = self.sut_cls(data, self.line_item_validator)
        result = invoice.is_closed()

        self.assertFalse(result)

    def test_is_paid__true(self):
        data = {
            'paid': True
        }

        invoice = self.sut_cls(data, self.line_item_validator)
        result = invoice.is_paid()

        self.assertTrue(result)

    def test_is_paid__false(self):
        data = {
            'paid': False
        }

        invoice = self.sut_cls(data, self.line_item_validator)
        result = invoice.is_paid()

        self.assertFalse(result)

    def test_is_valid__should_call_validators(self):
        data = 'dummy data'

        invoice = self.sut_cls(data, self.line_item_validator)
        invoice.is_paid = Mock()
        invoice.is_closed = Mock()
        invoice._are_valid_lines = Mock()

        invoice.is_valid()

        invoice._are_valid_lines.assert_called_once_with()
        invoice.is_closed.assert_called_once_with()
        invoice.is_paid.assert_called_once_with()

    def test_is_valid__false_not_called_further_validators(self):
        data = 'dummy data'

        invoice = self.sut_cls(data, self.line_item_validator)
        invoice.is_paid = Mock()
        invoice.is_closed = Mock()
        invoice._are_valid_lines = Mock()
        invoice.is_paid.return_value = False

        result = invoice.is_valid()

        self.assertFalse(result)
        invoice.is_closed.assert_not_called()
        invoice._are_valid_lines.assert_not_called()

    def test_are_valid_lines_should_call_line_validators(self):
        data = {
            'lines': {
                'data': ['line_1', 'line_2']
            }
        }

        expected_calls = [call('line_1'), call('line_2')]

        invoice = self.sut_cls(data, self.line_item_validator)
        invoice._are_valid_lines()

        self.assertListEqual(
            self.line_item_validator.is_valid.call_args_list, expected_calls
        )

    def test_are_valid_lines_should_call_only_one_validator_on_first_invalid(
            self
    ):
        data = {
            'lines': {
                'data': ['line_1', 'line_2']
            }
        }

        expected_calls = [call('line_1')]
        self.line_item_validator.is_valid.return_value = False

        invoice = self.sut_cls(data, self.line_item_validator)
        result = invoice._are_valid_lines()

        self.assertFalse(result)
        self.assertListEqual(
            self.line_item_validator.is_valid.call_args_list, expected_calls
        )
