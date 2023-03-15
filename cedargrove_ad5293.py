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
    to 5.5v. The potentiometer circuit can operate with analog supply voltages from
    +/-9v to +/-16.5v. The pins act similarly to a passive resistive potentiometer,
    but require that voltages placed on any of the three pins not exceed the analog
    power supply voltage or drop below ground potential.

    The Cedar Grove AD5293 custom breakout board provides power and signal connections
    for SPI and the potentiometer chip. The AD5293 is also integrated with the
    AD9833-based Precision VCO Eurorack module."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        select=board.D6,
        wiper = 0,
    ):
        """Initialize SPI bus interconnect, derive chip select pin (to allow
        multiple class instances), and create the SPIDevice instance. During
        initialization, the generator is reset and placed in the pause state.

        :param board select: The AD5293 chip select pin designation. Defaults
        to board.D6.
        :param int wiper: The 10-bit potentiometer wiper integer value, range
        from 0 to 1024 waveform frequency in Hz ranging from
        0 to 2 ** 28. Defaults to 0.
        """

        self._spi = busio.SPI(board.SCK, MOSI=board.MOSI)  # Define SPI bus
        self._cs = digitalio.DigitalInOut(getattr(board, select))
        self._device = SPIDevice(
            self._spi, self._cs, baudrate=5000000, polarity=1, phase=0
        )

        self._wiper = wiper
        self._default_wiper = wiper
        self._normalized_wiper = self._wiper / 255.0
        self._write_to_device(0, wiper)



        # Initiate register pointers
        self._freq_reg = 0  # FREQ0
        self._phase_reg = 0  # PHASE0

        self._pause = True
        self._reset = True

        # Reset the device
        self.reset()

        # Set the master clock frequency
        self._m_clock = m_clock

    @property
    def wiper(self):
        """The raw value of the potentionmeter's wiper.
        :param wiper_value: The raw wiper value from 0 to 255.
        """
        return self._wiper

    @wiper.setter
    def wiper(self, value=0):
        if value < 0 or value > 255:
            raise ValueError("raw wiper value must be from 0 to 255")
        self._write_to_device(0x00, value)
        self._wiper = value

    @property
    def normalized_wiper(self):
        """The normalized value of the potentionmeter's wiper.
        :param normalized_wiper_value: The normalized wiper value from 0.0 to 1.0.
        """
        return self._normalized_wiper

    @normalized_wiper.setter
    def normalized_wiper(self, value):
        if value < 0 or value > 1.0:
            raise ValueError("normalized wiper value must be from 0.0 to 1.0")
        self._write_to_device(0x00, int(value * 255.0))
        self._normalized_wiper = value

    @property
    def default_wiper(self):
        """The default value of the potentionmeter's wiper.
        :param wiper_value: The raw wiper value from 0 to 255.
        """
        return self._default_wiper

    @default_wiper.setter
    def default_wiper(self, value):
        if value < 0 or value > 255:
            raise ValueError("default wiper value must be from 0 to 255")
        self._default_wiper = value

    def set_default(self, default):
        """A dummy helper to maintain UI compatibility digital
        potentiometers with EEROM capability (dS3502). The AD5245's
        wiper value will be set to 0 unless the default value is
        set explicitly during or after class instantiation."""
        self._default_wiper = default

    def shutdown(self):
        """Connects the W to the B terminal and opens the A terminal connection.
        The contents of the wiper register are not changed."""
        self._write_to_device(0x20, 0)

     def reset(self):
        """Stop and reset the waveform generator. Pause the master clock.
        Update all registers with default values. Set sine wave mode. Clear the
        reset mode but keep the master clock paused.
        """
        # Reset control register contents, pause, and put device in reset state
        self._reset = True
        self._pause = True
        self._freq_reg = 0
        self._phase_reg = 0
        self._wave_type = "sine"
        self._update_control_register()

        # While reset, zero the frequency and phase registers
        self._update_freq_register(new_freq=0, register=0)
        self._update_freq_register(new_freq=0, register=1)
        self._update_phase_register(new_phase=0, register=0)
        self._update_phase_register(new_phase=0, register=1)

        # Take the waveform generator out of reset state, master clock still paused
        self._reset = False
        self._update_control_register()

    def _send_data(self, data):
        """Send a 16-bit word through SPI bus as two 8-bit bytes.
        :param int data: The 16-bit data value to write to the SPI device.
        """
        data &= 0xFFFF
        tx_msb = data >> 8
        tx_lsb = data & 0xFF

        with self._device:
            self._spi.write(bytes([tx_msb, tx_lsb]))

    def _update_control_register(self):
        """Construct the control register contents per existing local parameters
        then send the new control register word to the waveform generator.
        """
        # Set default control register mask value (sine wave mode)
        control_reg = 0x2000

        if self._reset:
            # Set the reset bit
            control_reg |= 0x0100

        if self._pause:
            # Disable master clock bit
            control_reg |= 0x0080

        control_reg |= self._freq_reg << 11  # Frequency register select bit
        control_reg |= self._phase_reg << 10  # Phase register select bit

        if self._wave_type == "triangle":
            # Set triangle mode
            control_reg |= 0x0002

        if self._wave_type == "square":
            # Set square mode
            control_reg |= 0x0028

        self._send_data(control_reg)

