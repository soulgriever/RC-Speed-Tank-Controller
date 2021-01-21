#!/usr/bin/env python

import socket
import pickle
import time

UDP_IP = '192.168.2.4'
UDP_PORT = 5005

x = 127 # Left Joystick initial value
y = 127 # Right Joystick initial value

from evdev import InputDevice, ecodes
while 1==1:
    try:
        fh = open('/dev/input/event1') #looks for the PS3 controller connected via USB (event0 if using a non six-axis controller)
        print('controller found')
        gamepad = InputDevice('/dev/input/event1')
        print(gamepad)

        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                if event.code == 1: #Left Joystick
                    x = event.value 
                elif event.code == 4: #Right Joystick
                    y = event.value
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                d = {1: x, 2: y} #Create's a local dictionary for Left and Right Joystick values
                msg = pickle.dumps(d) #m = pickle.loads(msg) unserializes the other side
                s.sendto(msg, (UDP_IP, UDP_PORT))
            except socket.error, msg:
                print 'Client connection closed', addr
                break
        
    except IOError:
        time.sleep(1)
        print('Controller Not Found: Stopping Vehicle')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            d = {1: 127, 2: 127}
            msg = pickle.dumps(d)
            s.sendto(msg, (UDP_IP, UDP_PORT))
        except socket.error, msg:
            print 'Client connection closed', addr
            break
