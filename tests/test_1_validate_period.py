import unittest

from src.code import validate_period


class TestCase(unittest.TestCase):

    def test_validate_period_true(self):
        data = {
            'object': 'invoice',
            'id': 'in_1036Vr2eZvKYlo2CfjuUHA94',
            'customer': 'cus_D6nocXHQTVqNkf',
            'subscription': 'sub_36VrPHS2vVxJMq',
            'date': 1386790772,
            'currency': 'usd',
            'invoice_pdf': None,
            'billing_reason': None,
            'total': 0,
            'livemode': False,
            'charge': None,
            'statement_descriptor': None,
            'webhooks_delivered_at': 1386790772,
            'number': None,
            'starting_balance': 0,
            'paid': True,
            'attempted': True,
            'amount_due': 0,
            'tax': None,
            'billing': 'charge_automatically',
            'application_fee': None,
            'hosted_invoice_url': None,
            'description': None,
            'next_payment_attempt': None,
            'amount_paid': 0,
            'receipt_number': None,
            'closed': True,
            'ending_balance': None,
            'tax_percent': None,
            'discount': None,
            'attempt_count': 0,
            'metadata': {},
            'forgiven': False,
            'subtotal': 0,
            'due_date': None,
            'amount_remaining': 0,
            'lines': {
                'url': '/v1/invoices/in_1036Vr2eZvKYlo2CfjuUHA94/lines',
                'has_more': False,
                'object': 'list',
                'data': [
                    {
                        'object': 'line_item',
                        'type': 'subscription',
                        'proration': False,
                        'description': '1 × vvv (at $54.65 / every 5 weeks)',
                        'subscription_item': 'si_18SfBn2eZvKYlo2C1fwOImYF',
                        'livemode': False,
                        'id': 'sli_eb2591c30b4085',
                        'amount': 5465,
                        'metadata': {},
                        'discountable': True,
                        'currency': 'usd',
                        'quantity': 1,
                        'subscription': 'sub_36VrPHS2vVxJMq',
                        'period': {
                            'end': 1450726772,
                            'start': 1447702772
                        },
                        'plan': {
                            'object': 'plan',
                            'billing_scheme': 'per_unit',
                            'active': True,
                            'livemode': False,
                            'id': '40',
                            'created': 1386694689,
                            'amount': 5465,
                            'tiers': None,
                            'interval': 'week',
                            'aggregate_usage': None,
                            'transform_usage': None,
                            'metadata': {
                                'charset': 'utf-8',
                                'content': '40'
                            },
                            'tiers_mode': None,
                            'product': 'prod_BTcfj5EqyqxDVn',
                            'usage_type': 'licensed',
                            'currency': 'usd',
                            'nickname': None,
                            'trial_period_days': 5,
                            'interval_count': 5
                        }
                    }
                ]
            }
        }

        result = validate_period(data['lines']['data'][0])

        self.assertTrue(result)

    def test_validate_period_false(self):
        data = {
            'object': 'invoice',
            'id': 'in_1036Vr2eZvKYlo2CfjuUHA94',
            'customer': 'cus_D6nocXHQTVqNkf',
            'subscription': 'sub_36VrPHS2vVxJMq',
            'date': 1386790772,
            'currency': 'usd',
            'invoice_pdf': None,
            'billing_reason': None,
            'total': 0,
            'livemode': False,
            'charge': None,
            'statement_descriptor': None,
            'webhooks_delivered_at': 1386790772,
            'number': None,
            'starting_balance': 0,
            'paid': True,
            'attempted': True,
            'amount_due': 0,
            'tax': None,
            'billing': 'charge_automatically',
            'application_fee': None,
            'hosted_invoice_url': None,
            'description': None,
            'next_payment_attempt': None,
            'amount_paid': 0,
            'receipt_number': None,
            'closed': True,
            'ending_balance': None,
            'tax_percent': None,
            'discount': None,
            'attempt_count': 0,
            'metadata': {},
            'forgiven': False,
            'subtotal': 0,
            'due_date': None,
            'amount_remaining': 0,
            'lines': {
                'url': '/v1/invoices/in_1036Vr2eZvKYlo2CfjuUHA94/lines',
                'has_more': False,
                'object': 'list',
                'data': [
                    {
                        'object': 'line_item',
                        'type': 'subscription',
                        'proration': False,
                        'description': '1 × vvv (at $54.65 / every 5 weeks)',
                        'subscription_item': 'si_18SfBn2eZvKYlo2C1fwOImYF',
                        'livemode': False,
                        'id': 'sli_eb2591c30b4085',
                        'amount': 5465,
                        'metadata': {},
                        'discountable': True,
                        'currency': 'usd',
                        'quantity': 1,
                        'subscription': 'sub_36VrPHS2vVxJMq',
                        'period': {
                            'end': 1450726772,
                            'start': 1467702772
                        },
                        'plan': {
                            'object': 'plan',
                            'billing_scheme': 'per_unit',
                            'active': True,
                            'livemode': False,
                            'id': '40',
                            'created': 1386694689,
                            'amount': 5465,
                            'tiers': None,
                            'interval': 'week',
                            'aggregate_usage': None,
                            'transform_usage': None,
                            'metadata': {
                                'charset': 'utf-8',
                                'content': '40'
                            },
                            'tiers_mode': None,
                            'product': 'prod_BTcfj5EqyqxDVn',
                            'usage_type': 'licensed',
                            'currency': 'usd',
                            'nickname': None,
                            'trial_period_days': 5,
                            'interval_count': 5
                        }
                    }
                ]
            }
        }

        result = validate_period(data['lines']['data'][0])

        self.assertFalse(result)
