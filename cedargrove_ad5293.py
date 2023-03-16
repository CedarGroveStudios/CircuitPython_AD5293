# SPDX-FileCopyrightText: Copyright (c) 2023 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_ad5293`
================================================================================

A CircuitPython driver for the AD5293 digital potentiometer.

* Author(s): JG

Implementation Notes
--------------------

**Hardware:**

* Cedar Grove Studios AD5293 breakout or equivalent

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_AD5293.git"


# pylint: disable=too-many-instance-attributes
class AD5293:
    """Class representing the Cedar Grove AD5293, an SPI digital linear taper
    potentiometer.

    The AD5293 Digital Potentiometer is an SPI, 100K-ohm device. The potentiometer
    sports 1024 resistance steps and can work with a logic power source from 2.7v
    to 5.5v. The potentiometer circuit can operate with dual analog supply voltages
    from +/-9v to +/-16.5v. The pins act similarly to a passive resistive
    potentiometer, but require that voltages placed on any of the three pins
    not exceed the analog power supply voltages.

    The Cedar Grove AD5293 custom breakout board provides power and signal
    connections for SPI and the potentiometer chip. The AD5293 is also
    used in the AD9833-based Cedar Grove Precision VCO Eurorack module."""

    _BUFFER = bytearray(2)

    # pylint: disable=too-many-arguments
    def __init__(self, select=board.D6, wiper=0):
        """Initialize SPI bus interconnect, derive chip select pin (to allow
        multiple class instances), and create the SPIDevice instance. During
        initialization, the potentiometer is reset and placed in the power-down
        state.
        :param board select: The AD5293 chip select pin designation. Defaults
        to board.D6.
        :param int wiper: The 10-bit potentiometer wiper integer value, range
        from 0 to 1024. Defaults to 0."""

        self._spi = busio.SPI(board.SCK, MOSI=board.MOSI)  # Define SPI bus
        # self._cs = digitalio.DigitalInOut(getattr(board, select))
        self._cs = digitalio.DigitalInOut(select)
        self._device = SPIDevice(
            self._spi, self._cs, baudrate=5000000, polarity=1, phase=0
        )

        self._wiper = wiper
        self._default_wiper = wiper
        self._normalized_wiper = self._wiper / 1023.0
        self._send_data(0x0400 | wiper)

        self._power_down = False
        self._reset = True

        # Reset the device
        self.reset()

        # Enable register read-write
        self._send_data(0x1802)

    @property
    def wiper(self):
        """The raw value of the potentiometer's wiper."""
        return self._wiper

    @wiper.setter
    def wiper(self, new_wiper=0):
        """Set the raw value of the potentiometer's wiper.
        :param new_wiper: The raw wiper value from 0 to 1023."""
        if new_wiper < 0 or new_wiper > 1023:
            raise ValueError("raw wiper value must be from 0 to 1023")
        self._send_data(0x0400 | int(new_wiper))
        self._wiper = new_wiper

    @property
    def normalized_wiper(self):
        """The normalized value of the potentiometer's wiper."""
        return self._normalized_wiper

    @normalized_wiper.setter
    def normalized_wiper(self, new_norm_wiper):
        """Set the normalized value of the potentiometer's wiper.
        :param new_norm_wiper: The normalized wiper value from 0.0 to 1.0."""
        if new_norm_wiper < 0 or new_norm_wiper > 1.0:
            raise ValueError("normalized wiper value must be from 0.0 to 1.0")
        self._send_data(0x0400 | int(new_norm_wiper * 1023.0))
        self._normalized_wiper = new_norm_wiper

    @property
    def default_wiper(self):
        """The default value of the potentiometer's wiper."""
        return self._default_wiper

    @default_wiper.setter
    def default_wiper(self, new_default_wiper):
        """Set the default value of the potentiometer's wiper.
        :param new_default_wiper: The raw wiper value from 0 to 1023."""
        if new_default_wiper < 0 or new_default_wiper > 1023:
            raise ValueError("default wiper value must be from 0 to 1023")
        self._default_wiper = new_default_wiper

    def set_default(self, new_default):
        """A dummy helper to maintain UI compatibility digital
        potentiometers with EEROM capability (dS3502). The AD5293's
        wiper value will be set to 0 unless the default value is
        set explicitly during or after class instantiation.
        :param new_default: The raw wiper value from 0 to 1023."""
        self._default_wiper = new_default

    def shutdown(self):
        """Connects the W to the B terminal and opens the A terminal connection.
        The contents of the wiper register are not changed."""
        self._send_data(0x2001)

    def reset(self):
        """Reset the potentiometer. Refresh RDAC with mid-scale value. Disable
        write-protect."""
        self._reset = True
        self._send_data(0x1000)  # Reset
        self._send_data(0x1802)  # Disable write-protect

    def _send_data(self, data):
        """Send a 16-bit word through SPI bus as two 8-bit bytes.
        :param int data: The 16-bit data value to write to the SPI device.
        """
        data &= 0xFFFF
        tx_msb = data >> 8
        tx_lsb = data & 0xFF

        with self._device:
            self._spi.write(bytes([tx_msb, tx_lsb]))

    def _read_data(self):
        """Reads a 16-bit word from the SPI bus."""
        with self._device:
            self._spi.readinto(self._BUFFER)
        return self._BUFFER
