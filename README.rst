Introduction
============

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/CircuitPython_AD5293/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/CircuitPython_AD5293/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A CircuitPython driver for the AD5293 digital potentiometer.

The AD5293 Digital Potentiometer is an SPI, 10-bit, 100K-ohm device. The device
operates with a digital logic power source of 2.7v to 5.5v and a dual analog
power source of +/-9v to +/-16.5v. The potentiometer pins act similarly to a passive
resistive potentiometer, but requires that voltages placed on any of the
three pins not exceed the analog power supply voltage.

The CircuitPython driver supports a single SPI potentiometer device per instance.
It does not work with daisy-chained devices.

The Cedar Grove AD5293 custom breakout board provides power and signal
connections for SPI and the potentiometer chip. The AD5293 is also
used in the AD9833-based Cedar Grove Precision VCO Eurorack module.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install cedargrove_ad5293

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import board
    import cedargrove_ad5293

    ad5293 = cedargrove_ad5245.AD5293(spi=board.SPI(), select=board.D9)

    ad5293.wiper = 1023
    print("Wiper set to %d"%ad5293.wiper)

``ad5293_simpletest.py`` and other examples can be found in the ``examples`` folder.


Documentation
=============
`AD5293 CircuitPython Driver API Class Description <https://github.com/CedarGroveStudios/CircuitPython_AD5293/blob/main/media/pseudo_rtd_cedargrove_ad5293.pdf>`_

`CedarGrove AD5293 Breakout OSH Park Project <https://oshpark.com/shared_projects/ADF8EdH9>`_

`CedarGrove AD5293 Breakout PCB Repository <https://github.com/CedarGroveStudios/PCB_AD5293_Digital_Potentiometer>`_

.. image:: https://github.com/CedarGroveStudios/CircuitPython_AD5293/blob/main/media/ad5293_glamour.png

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_AD5293/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
