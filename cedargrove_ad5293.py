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

import time
import board
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_AD5293.git"


class AD5293:
    """Class representing the Cedar Grove AD5293, an SPI digital linear taper
    potentiometer breakout module.

    The AD5293 Digital Potentiometer is an SPI, 10-bit, 100K-ohm device. The
    device operates with a digital logic power source of 2.7v to 5.5v and a
    dual analog power source of +/-9v to +/-16.5v. The potentiometer pins act
    similarly to a passive resistive potentiometer, but requires that voltages
    placed on any of the three pins not exceed the analog power supply voltage.

    The CircuitPython driver supports a single SPI potentiometer device per
    instance. Connecting the SDO pin to the SPI host input pin is not required
    nor recommended since the SDO pin could interfere with other SPI-connected
    devices.

    This driver does not work with daisy-chained devices.

    The Cedar Grove AD5293 custom breakout board provides power and signal
    connections for SPI and the potentiometer chip. The AD5293 is also used in
    the AD9833-based Cedar Grove Precision VCO Eurorack module."""

    def __init__(self, spi=board.SPI(), select=board.D9, wiper=0):
        """Initialize the AD5293 device instance. During initialization, the
        potentiometer is reset, writing is enabled, and the wiper is set to the
        specified initialization value.
        :param busio.SPI spi: The `busio.SPI` definition. Defaults to
        `board.SPI()`.
        :param board select: The chip select pin designation. Defaults to
        `board.D9`.
        :param int wiper: The initial 10-bit potentiometer wiper integer value,
        range from 0 to 1023. Defaults to 0."""

        # Define the SPI bus connection
        self._spi = spi
        chip_sel = digitalio.DigitalInOut(select)
        self._device = SPIDevice(
            self._spi, chip_sel, baudrate=1000000, polarity=0, phase=1
        )

        # Power on delay (2ms minimum)
        time.sleep(0.03)

        # Place device into normal mode (not powered-down)
        self._send_data(0x2000)

        # Reset the device and disable write-protect
        self.reset()

        # Set initial wiper value
        if wiper < 0 or wiper > 1023:
            raise ValueError("Raw wiper value must be from 0 to 1023")
        self._wiper = wiper
        self._normalized_wiper = self._wiper / 1023.0
        self._send_data(0x0400 | wiper)

    @property
    def wiper(self):
        """The raw value of the potentiometer's wiper."""
        return self._wiper

    @wiper.setter
    def wiper(self, new_wiper=0):
        """Set the raw value of the potentiometer's wiper.
        :param new_wiper: The raw wiper value from 0 to 1023."""
        if new_wiper < 0 or new_wiper > 1023:
            raise ValueError("Raw wiper value must be from 0 to 1023")
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
            raise ValueError("Normalized wiper value must be from 0.0 to 1.0")
        self._send_data(0x0400 | int(new_norm_wiper * 1023.0))
        self._normalized_wiper = new_norm_wiper

    def shutdown(self):
        """Connects the W pin to the B pin and opens the A pin. The content
        of the wiper register is not changed."""
        self._send_data(0x2001)

    def reset(self):
        """Reset the potentiometer. Refresh RDAC with mid-scale value. Disable
        write-protect."""
        self._send_data(0x1000)  # Reset
        time.sleep(0.002)  # Reset delay (1.5ms min)
        self._send_data(0x1802)  # Disable write-protect

    def _send_data(self, data):
        """Send a 16-bit word through SPI bus as two 8-bit bytes.
        :param int data: The 16-bit data value to write to the SPI device."""
        with self._device:
            self._spi.write(bytes([data >> 8, data & 0xFF]))
