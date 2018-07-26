import asynctest
from asynctest import CoroutineMock, Mock

from src.invoice_listener_2 import InvoiceListener


class TestSubscriptionListener(asynctest.TestCase):
    use_default_loop = True
    forbid_get_event_loop = False

    def setUp(self):
        self.invoice_validator_mocked = Mock()
        self.cache_mocked = CoroutineMock()
        self.listener = InvoiceListener(
            self.invoice_validator_mocked, self.cache_mocked
        )
        self.listener.process_invoice = CoroutineMock()

    async def test_check_redis_status(self):
        invoice = 'dummy data'

        self.invoice_validator_mocked.is_valid.return_value = True

        await self.listener.process_invoice(invoice)

        self.listener._cache.set.assert_awaited_once_with('invoice', invoice)
