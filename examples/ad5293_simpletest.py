# SPDX-FileCopyrightText: Copyright (c) 2023 JG for Cedar Grove Maker Studios
# SPDX-License-Identifier: Unlicense

import board
import busio
from cedargrove_ad5293 import AD5293

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)  # Define SPI bus

ad5293 = AD5293(spi, select=board.D6)

# Ramp from 0 to 1023 as fast as possible
while True:
    for i in range(0, 1024):
        ad5293.wiper = i
