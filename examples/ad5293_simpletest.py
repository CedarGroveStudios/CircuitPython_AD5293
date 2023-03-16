# SPDX-FileCopyrightText: Copyright (c) 2023 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: Unlicense

from time import sleep
import board
from analogio import AnalogIn
import cedargrove_ad5293

# wire pin A to +3.3v, pin B to GND, and pin W to A0

ad5293 = cedargrove_ad5293.AD5293(select=board.D6)
wiper_output = AnalogIn(board.A0)

while True:
    ad5293.wiper = 255
    print("Wiper set to %d" % ad5293.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f" % voltage)
    print("")
    sleep(1.0)

    ad5293.wiper = 0
    print("Wiper set to %d" % ad5293.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f" % voltage)
    print("")
    sleep(1.0)

    ad5293.wiper = 126
    print("Wiper set to %d" % ad5293.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f" % voltage)
    print("")
    sleep(1.0)
