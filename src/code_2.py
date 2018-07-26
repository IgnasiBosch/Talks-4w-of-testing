from datetime import datetime


class SubscriptionValidator:

    def is_valid(self, line_item):
        return self._is_valid_period(line_item) and self._is_valid_plan(
            line_item)

    @staticmethod
    def _is_valid_period(line_item):
        start = line_item['period']['start']
        end = line_item['period']['end']

        return start < end

    @staticmethod
    def _is_valid_plan(line_item):
        plan = line_item['plan']

        return plan.get('active', False)


class PromotionValidator:
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def is_valid(cls, line_item):
        return datetime.strptime(
            line_item['valid_until'], cls.TIME_FORMAT
        ) > datetime.utcnow()


class LineItemValidator:
    validators_by_type = {
        'subscription': SubscriptionValidator,
        'promotion': PromotionValidator
    }

    @classmethod
    def is_valid(cls, line_item):
        try:
            return cls.validators_by_type[line_item['type']].is_valid(
                line_item)

        except KeyError:
            raise TypeError('Invalid item type')


class InvoiceValidator:

    def __init__(self, invoice, line_item_validator):
        self._invoice = invoice
        self._line_item_validator = line_item_validator

    def is_valid(self):
        return self.is_paid() and self.is_closed() and self._are_valid_lines()

    def _are_valid_lines(self):

        for line_item in self._invoice['lines']['data']:
            if not self._line_item_validator.is_valid(line_item):
                return False

        return True

    def is_closed(self):
        return self._invoice['closed']

    def is_paid(self):
        return self._invoice['paid']
