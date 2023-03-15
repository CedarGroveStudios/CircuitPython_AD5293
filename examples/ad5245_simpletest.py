# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: Unlicense

from time import sleep
import board
from analogio import AnalogIn
import cedargrove_ad5245

# wire pin A to +3.3v, pin B to GND, and pin W to A0

ad5245 = cedargrove_ad5245.AD5245(address=0x2C)
wiper_output = AnalogIn(board.A0)

while True:

    ad5245.wiper = 255
    print("Wiper set to %d" % ad5245.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f" % voltage)
    print("")
    sleep(1.0)

    ad5245.wiper = 0
    print("Wiper set to %d" % ad5245.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f" % voltage)
    print("")
    sleep(1.0)

    ad5245.wiper = 126
    print("Wiper set to %d" % ad5245.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f" % voltage)
    print("")
    sleep(1.0)
