"""I2C drivers for the ``greenpak`` package."""
from typing_extensions import override
from typing_extensions import deprecated


class GreenPakI2cInterface:
    """A base class for GreenPak compatible I2C driver implementations."""

    @deprecated("Use gp_write() instead.")
    def write(self, addr: int, data: bytearray, silent: bool = False) -> bool:
        """Write the given bytes to the I2C device with address.

        :param addr: I2C device address in the range [0, 127]
        :type addr: int

        :param data: The data to write. A bytearray with 0 to 256 bytes.
            If ``data`` is empty, the implementation should still perform the write operation
            but with zero bytes. This is used for I2C scanning.
        :type data: int

        :param silent: If True, do not print diagnostic information in case of a write failure.
        :type silent: bool

        :returns: True if OK, False if an error.
        :rtype: bool
        """
        assert False, f"Class {self.__class__} does not implement write()"

    @deprecated("Use gp_read() instead.")
    def read(
        self, addr: int, byte_count: int, silent: bool = False
    ) -> bytearray | None:
        """Read the given number of bytes from the I2C device with given address.

        :param addr: I2C device address in the range [0, 127]
        :type addr: int

        :param byte_count: The number of bytes to read. Should be in the range [0, 256]. If
            byte_count is zero, the implementation should still perform the read operation
            but with zero bytes. This is used for I2C scanning.
        :type byte_count: int

        :param silent: If True, do not print diagnostic information in case of a read failure.
        :type silent: bool

        :returns: The bytes read or None if an error.
        :rtype: bytearray
        """
        assert False, f"Class {self.__class__} does not implement read()"

    """ Below are a new set of interface methods, which may eventually replace read, write
    methods above.

    New driver/adapter implementations should implement these to work with upcoming
    greenpak driver change.
    """
    def gp_write(self, i2c_addr: int, start: int, data: bytearray) -> bool:

        """New interface method: gp_write()

        :param i2c_addr: I2C device address in the range [0, 127]
        :type addr: int

        :param start: SLG memory/register start address for the write, range [0,256]
        :type start: int

        :returns: True if write succeeds
        :rtype: bool
        """

        assert False, f"Class {self.__class__} does not implement gp_write()"

    def gp_read(self, i2c_addr: int, start: int, byte_count: int) -> bytearray | None:

        """New interface method: gp_read()

        :param i2c_addr: I2C device address in the range [0, 127]
        :type addr: int

        :param start: SLG memory/register start address for the write, range [0,256]
        :type start: int

        :returns:  bytearray if the op went OK, None if an error happened.
        :rtype: bytearray
        """

        assert False, f"Class {self.__class__} does not implement gp_read()"


class GreenPakI2cAdapter(GreenPakI2cInterface):
    """A GreenPakI2cInterface implementation for I2C Adapter boards."""

    def __init__(self, port):
        from i2c_adapter import I2cAdapter
        self.__i2c: I2cAdapter = I2cAdapter(port)

    @override
    def write(self, addr: int, data: bytearray, silent: bool = False) -> bool:
        return self.__i2c.write(addr, data, silent=silent)

    @override
    def read(self, addr: int, byte_count: int, silent: bool = False) -> bytearray:
        return self.__i2c.read(addr, byte_count, silent=silent)


class GreenPakI2cDriver(GreenPakI2cInterface):
    """A GreenPakI2cInterface implementation for I2C Adapter boards."""

    def __init__(self, port, pullups=True):
        from i2cdriver import I2CDriver
        self.__i2c: I2CDriver = I2CDriver(port, reset=True)
        # Per https://i2cdriver.com/i2cdriver.pdf
        # 4.7K on SCL/SDA if pullups is True, else, no pullups.
        self.__i2c.setpullups(0b100100 if pullups else 0b000000)

    @override
    def write(self, addr: int, data: bytearray, silent: bool = False) -> bool:
        ok1 = self.__i2c.start(addr, 0)
        ok2 = self.__i2c.write(data)
        self.__i2c.stop()
        return ok1 and ok2

    @override
    def read(
        self, addr: int, byte_count: int, silent: bool = False
    ) -> bytearray | None:
        ack = self.__i2c.start(addr, 1)
        if ack:
            data = self.__i2c.read(byte_count)
        self.__i2c.stop()
        return data if ack else None

# removed SMBus class
