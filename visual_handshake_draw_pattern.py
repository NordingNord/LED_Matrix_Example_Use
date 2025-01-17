#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################
# Standard Imports                            #
###############################################
import time
import threading
import math
import numpy as np
import random
import secrets
import sys
from ast import literal_eval


###############################################
# LED matrix imports                          #
###############################################
from rpi_rgb_led_matrix_master.bindings.python.samples.samplebase import SampleBase
from rpi_rgb_led_matrix_master.bindings.python.rgbmatrix import graphics

###############################################
# Led matrix class                            #
###############################################
class DrawPattern(SampleBase):
    def __init__(self,*args, **kwargs):

        ###############################
        # Visual handshake variables  #
        ###############################
        self.pattern = literal_eval(sys.argv[6])

        self.screen_width = 64
        self.screen_height = 32

        # Remove pattern arguments
        sys.argv = [sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]]
        super(DrawPattern,self).__init__(*args, **kwargs)

    def run(self):
        # Create canvas
        canvas = self.matrix.CreateFrameCanvas()
        print("Beginning to draw")
        # Run forever
        while True:
            # Draw on canvas until box is open
            for y in range(self.matrix.height):
                for x in range(self.matrix.width):
                    canvas.SetPixel(x,y,self.pattern[y][x][2],self.pattern[y][x][1],self.pattern[y][x][0])

            scanvas = self.matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    draw_pattern = DrawPattern()
    if (not draw_pattern.process()):
        draw_pattern.print_help()