import asyncio
import unittest
import comfospot40
import logging
from serial import SerialException


class TestStateLoad(unittest.IsolatedAsyncioTestCase):
    async def test_read_byte_ok(self):
        class TestSerial:
            async def read(self, _):
                return b"A"

        s = TestSerial()
        p = comfospot40.Parser(s)
        self.assertEqual(b"A", await p.read_byte())

    async def test_read_byte_error(self):
        logging.disable(logging.CRITICAL)

        class TestSerial:
            async def read(self, _):
                raise SerialException("something")
                return b"A"

        s = TestSerial()
        p = comfospot40.Parser(s)
        with self.assertRaises(SerialException):
            await p.read_byte(0)

    async def test_read_byte_retry(self):
        logging.disable(logging.CRITICAL)

        class TestSerial:
            async def read(self, _):
                raise SerialException("something")
                return b"A"

        s = TestSerial()
        p = comfospot40.Parser(s)
        with self.assertRaises(SerialException):
            await asyncio.wait_for(p.read_byte(0), timeout=1)

    async def test_read_byte_retry_timeout(self):
        logging.disable(logging.CRITICAL)

        class TestSerial:
            async def read(self, _):
                raise SerialException("something")
                return b"A"

        s = TestSerial()
        p = comfospot40.Parser(s)
        with self.assertRaises(asyncio.exceptions.TimeoutError):
            await asyncio.wait_for(p.read_byte(2), timeout=0.1)
