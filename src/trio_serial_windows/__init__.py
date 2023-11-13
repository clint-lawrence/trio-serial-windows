from __future__ import annotations

import os
from typing import Type

# disable warnings for unused imports - we're intentionally importing them
# so that they are in the package namespace
# ruff: noqa: F401

# This is a bit of a mess... We want to use AbstractSerialStream from trio-serial
# however, trio-serial won't import on windows. But the import error gets raise
# _after_ abstract module has loaded. So although our "import trio_serial.abstract"
# fails to enter anything into the local name space, it is in sys.modules. So we
# manually bind the objects we need directly from sys.modules. Hopefully we can
# tidy this up with some work with trio-serial.
try:
    import trio_serial.abstract
except ImportError:
    pass

import sys

AbstractSerialStream = sys.modules["trio_serial.abstract"].AbstractSerialStream
Parity = sys.modules["trio_serial.abstract"].Parity
StopBits = sys.modules["trio_serial.abstract"].StopBits
del sys

__version__ = "0.1.0"

SerialStream: Type[AbstractSerialStream]

if os.name == "nt":
    # This package implements a Windows version of trio-serial's
    # AbstractSerialStream
    from trio_serial_windows._windows import WindowsSerialStream as SerialStream
else:
    raise ImportError(
        f"Platform {os.name!r} not supported. Try 'trio-serial' on posix platforms."
    )
