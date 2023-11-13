# trio-serial-windows

Implements a serial port with a [Trio](https://trio.readthedocs.io/) `Stream` interface on Windows.
See [trio-serial](https://pypi.org/project/trio-serial/) for the equivalent functionality on Linux and MacOS.

Example usage (assuming a looped back serial connection):
```python
import trio
import trio_serial_windows


async def main():
    async with trio_serial_windows.SerialStream("COM5", baudrate=115200) as port:
        await port.send_all(b"Hello, World!")
        await trio.sleep(0.2)
        print(await port.receive_some())

trio.run(main)
```