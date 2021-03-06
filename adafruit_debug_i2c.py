# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_debug_i2c`
================================================================================

Wrapper library for debugging I2C.


* Author(s): Roy Hooper, Kattni Rembor

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Debug_I2C.git"


class I2CDebug:
    """
    Wrapper library for debugging I2C.

    This library wraps an I2C object and prints buffers before writes and after reads.

    See the I2C documentation for detailed documentation on the methods in this class.

    :param i2c: An initialized I2C object to debug.

    This example uses the LIS3DH accelerometer. This lib can be used with any I2C device. Save
    the code to your board.

    .. code-block:: python
        import adafruit_lis3dh
        from adafruit_debug_i2c import I2CDebug
        import busio
        import board
        import digitalio

        i2c = I2CDebug(busio.I2C(board.SCL, board.SDA))
        int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
        accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)

        print(accelerometer.acceleration)

        for i in range(5):
            print(accelerometer.acceleration)

    """
    def __init__(self, i2c):
        self._i2c = i2c
        if hasattr(self._i2c, 'writeto_then_readfrom'):
            self.writeto_then_readfrom = self._writeto_then_readfrom

    def __enter__(self):
        """
        No-op used in Context Managers.
        """
        return self._i2c.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Automatically deinitialises the hardware on context exit.
        """
        return self._i2c.__exit__(exc_type, exc_val, exc_tb)

    def deinit(self):
        """
        Releases control of the underlying I2C hardware so other classes can use it.
        """
        return self._i2c.deinit()

    def readfrom_into(self, address, buffer, *args, start=0, end=None):
        """
        Debug version of ``readfrom_into`` that prints the buffer after reading.

        :param int address: 7-bit device address
        :param bytearray buffer: buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include

        """
        self._i2c.readfrom_into(address, buffer, *args, start=start, end=end)
        print("i2c.readfrom_into at address {}:".format(hex(address)), [hex(i) for i in buffer])

    def scan(self):
        """
        Scan all I2C addresses between 0x08 and 0x77 inclusive and return a list of those that respond.

        :return: List of device ids on the I2C bus
        :rtype: list
        """
        return self._i2c.scan()

    def try_lock(self):
        """
        Attempts to grab the I2C lock. Returns True on success.

        :return: True when lock has been grabbed
        :rtype: bool
        """
        return self._i2c.try_lock()

    def unlock(self):
        """
        Releases the I2C lock.
        """
        return self._i2c.unlock()

    def writeto(self, address, buffer, *args, **kwargs):
        """
        Debug version of ``write`` that prints the buffer before sending.

        :param int address: 7-bit device address
        :param bytearray buffer: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include
        :param bool stop: If true, output an I2C stop condition after the
                          buffer is written
        """
        self._i2c.writeto(address, buffer, *args, **kwargs)
        print("i2c.writeto at address {}:".format(hex(address)), [hex(i) for i in buffer])

    def _writeto_then_readfrom(self, address, buffer_out, buffer_in, *args, out_start=0,
                               out_end=None, in_start=0, in_end=None):
        """
        Debug version of ``write_readinto`` that prints the ``buffer_out`` before writing and the
        ``buffer_in`` after reading.

        :TODO Verify parameter documentation is accurate
        :param address: 7-bit device address
        :param bytearray buffer_out: Write out the data in this buffer
        :param bytearray buffer_in: Read data into this buffer
        :param int out_start: Start of the slice of buffer_out to write out:
                              ``buffer_out[out_start:out_end]``
        :param int out_end: End of the slice; this index is not included. Defaults to
                            ``len(buffer_out)``
        :param int in_start: Start of the slice of ``buffer_in`` to read into:
                             ``buffer_in[in_start:in_end]``
        :param int in_end: End of the slice; this index is not included. Defaults to
                           ``len(buffer_in)``
        :param stop: If true, output an I2C stop condition after the buffer is written
        """
        print("i2c.writeto_then_readfrom.buffer_out at address {}:".format(hex(address)),
              [hex(i) for i in buffer_out[out_start:out_end]])
        self._i2c.writeto_then_readfrom(address, buffer_out, buffer_in, *args, out_start=out_start,
                                        out_end=out_end, in_start=in_start, in_end=in_end)
        print("i2c.writeto_then_readfrom.buffer_in at address {}:".format(hex(address)),
              [hex(i) for i in buffer_in[in_start:in_end]])