# -*- coding: utf-8 -*-
"""
@author: Emilio Moretti
Copyright 2013 Emilio Moretti <emilio.morettiATgmailDOTcom>
This program is distributed under the terms of the GNU Lesser General Public License.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

#WARNING: handling mouse events is harder than keyboard events.
# You have to do most things manually
from AutoHotPy import AutoHotPy
from destrotyer import Destroyer
import sys
import numpy as np
from PIL import ImageGrab
import cv2
import time


def stop_bot(autohotpy, event):
    """
    exit the program when you press ESC
    """
    autohotpy.stop()


def start_bot(autohotpy, event):
    """
    This function simulates a left click
    """

    destr = Destroyer(autohotpy)
    destr.loop()


if __name__=="__main__":

    # destr = Destroyer(1)
    # destr.loop()

    auto = AutoHotPy()
    auto.registerExit(auto.ESC, stop_bot)
    auto.registerForKeyDown(auto.S, start_bot)
    auto.start()
