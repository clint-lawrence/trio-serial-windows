r"""
Test trio-serial-windows, using pyserial as a reference implementation.

These test work using hardware. Use two interfaces with tx and rx
connected as indicated. (I don't have suitable hardware on hand
right now, but will expand to hardware handshaking when I can)

                 Tx ____  ____ Tx
                        \/
 Reference Port  Rx ____/\____ Rx   Test Port
  (pyserial)    GND ---------- GND  (trio-serial-windows)
"""
from serial import Serial
from trio_serial_windows import SerialStream
import trio
import pytest

# we won't test every baud rate, but slow, medium & fast
BAUD_RATES = [110, 9600, 115200]
DEFAULT_BAUD_RATE = 115200

PORT_REFERENCE = "COM5"
PORT_TEST = "COM6"


@pytest.mark.parametrize("baudrate", BAUD_RATES)
async def test_rx(baudrate):
    with Serial(PORT_REFERENCE, baudrate=baudrate) as refp:
        async with SerialStream(PORT_TEST, baudrate=baudrate) as testp:
            refp.write(b"hello")
            await trio.sleep(0.01)
            assert await testp.receive_some(5) == b"hello"


@pytest.mark.parametrize("baudrate", BAUD_RATES)
async def test_tx(baudrate):
    with Serial(PORT_REFERENCE, baudrate=baudrate) as refp:
        async with SerialStream(PORT_TEST, baudrate=baudrate) as testp:
            await testp.send_all(b"hello")
            assert refp.read(5) == b"hello"
