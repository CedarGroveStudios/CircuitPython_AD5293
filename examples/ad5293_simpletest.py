# SPDX-FileCopyrightText: Copyright (c) 2023 JG for Cedar Grove Maker Studios
# SPDX-License-Identifier: Unlicense

import board
from cedargrove_ad5293 import AD5293

ad5293 = AD5293(spi=board.SPI(), select=board.D9)

# Ramp from 0 to 1023 as quickly as possible
while True:
    for i in range(0, 1024):
        ad5293.wiper = i
