import asyncio
from asyncio import Queue

from src import Listener


class InvoiceListener(Listener):
    """Listener for new invoices received"""

    def __init__(self, invoice_validator, cache, io_loop=None):
        self._invoice_validator = invoice_validator
        self._io_loop = io_loop or asyncio.get_event_loop()
        self._cache = cache
        self.queue = Queue()

    def process_soon(self, msg):
        """Send a new message to a queue."""

        self.queue.put_nowait(msg)

    async def listen(self):
        """Listen to new invoices"""

        while True:
            invoice = await self.queue.get()
            await self.process_invoice(invoice)

    async def process_invoice(self, invoice):
        """Process invoice received"""
        if self._invoice_validator.is_valid(invoice):
            await self._cache.set('invoice', invoice)
            self._io_loop.create_task(...)

        else:
            # TODO log a message etc
            pass
