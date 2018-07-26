class LineItemValidator:
    """Validates an item from an invoice"""

    def __init__(self, line_item):
        self._line_item = line_item

    def is_valid(self):
        return self._is_valid_period() and self._is_valid_plan()

    def _is_valid_period(self):
        start = self._line_item['period']['start']
        end = self._line_item['period']['end']

        return start < end

    def _is_valid_plan(self):
        plan = self._line_item['plan']

        return plan.get('active', False)


class Invoice:
    """Mapping of an invoice"""

    def __init__(self, invoice):
        self._invoice = invoice

    def is_valid(self):
        return self.is_paid() and self.is_closed() and self._are_valid_lines()

    def _are_valid_lines(self):

        for line_item in self._invoice['lines']['data']:
            if not LineItemValidator(line_item).is_valid():
                return False

        return True

    def is_closed(self):
        return self._invoice['closed']

    def is_paid(self):
        return self._invoice['paid']
