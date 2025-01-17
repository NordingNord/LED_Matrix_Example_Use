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
import visual_handshake_draw_pattern
import subprocess


###############################################
# ROS Imports                                 #
###############################################
import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile

###############################################
# ROS Topic messages                          #
###############################################
#import rclpy.service
from std_msgs.msg import String
from std_msgs.msg import Float32

from sensor_msgs.msg import Image

from geometry_msgs.msg import PoseStamped

from mavros_msgs.msg import State, RCOut
from path_interfaces.msg import Path, Point, Pattern
from path_interfaces.srv import GetPath, GetPosition
from mavros_msgs.srv import SetMode
from mavros.base import SENSOR_QOS

###############################################
# ROS2 Node class                            #
###############################################
class VisualHandshakeDrone(Node):
    def __init__(self):
        super(VisualHandshakeDrone,self).__init__("visual_handshake_drone")

        ###############################
        # Subscribers                 #
        ###############################
        self.subscriber_pattern = self.create_subscription(Pattern,'/handshake/pattern',self.pattern_callback, 10)


        ###############################
        # Arguments                   #
        ###############################
        self.arg_col = "--led-cols=64"
        self.arg_row = "--led-rows=32"
        self.arg_slow = "--led-slowdown-gpio=4"
        self.arg_bright = "--led-brightness=20"
        self.arg_pulse = "--led-no-hardware-pulse=LED_NO_HARDWARE_PULSE"

    #####################
    # Topic conversion  #
    #####################
    def read_pattern(self,pattern_msg):
        # Convert message to pattern format
        pattern = []
        for i in range(len(pattern_msg)):
            row = []
            for j in range(len(pattern_msg[i].row)):
                pixel_value = []
                for k in range(3):
                    pixel_value.append(pattern_msg[i].row[j].colour[k])
                row.append(pixel_value)
            pattern.append(row)
        return pattern

    #####################
    # Callbacks         #
    #####################
    def pattern_callback(self,msg):
        self.get_logger().info('Pattern received')
        pattern = self.read_pattern(msg.pattern)

        # Kill drawer if still running
        if hasattr(self,'drawer') == True:
            poll = self.drawer.poll()
            if poll is None:
                self.drawer.kill()
        # Start drawer with new pattern
        self.start_drawer(pattern)
    
    def start_drawer(self,pattern):
        self.drawer = subprocess.Popen(['python3','src/eit-playground/src/visual_handshake_draw_pattern.py',self.arg_col,self.arg_row,self.arg_slow,self.arg_bright,self.arg_pulse,str(pattern)])


# Main function
def main(args=None):
    rclpy.init(args=args)
    handshaker = VisualHandshakeDrone()

    rclpy.spin(handshaker)
    handshaker.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()