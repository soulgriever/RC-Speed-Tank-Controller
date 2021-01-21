#!/usr/bin/env python

#Import needed libraries
import time
import pigpio
import socket
import pickle

#Wraps the pigpio daemon
pi1 = pigpio.pi()

#Pin Setup

#Left Motor
L_EN   = 14  #Enables the left driver
L_FPWM = 12  #RPWM on driver (Forward)
L_RPWM = 18  #LPWM on driver (Reverse)

#Right Motor
R_EN   = 16  #Enables the right driver
R_FPWM = 13  #RPWM on driver (Forward)
R_RPWM = 19  #LPWM on driver (Reverse)

#Sets all pins to Output
pi1.set_mode(L_EN, pigpio.OUTPUT)
pi1.set_mode(R_EN, pigpio.OUTPUT)
pi1.set_mode(L_FPWM, pigpio.OUTPUT)
pi1.set_mode(L_RPWM, pigpio.OUTPUT)
pi1.set_mode(R_FPWM, pigpio.OUTPUT)
pi1.set_mode(R_RPWM, pigpio.OUTPUT)

#Pulls all pins LOW
pi1.write(L_EN, 0)
pi1.write(R_EN, 0)
pi1.write(L_FPWM, 0)
pi1.write(L_RPWM, 0)
pi1.write(R_FPWM, 0)
pi1.write(R_RPWM, 0)

#Sets PWM frequency to 800Hz
pi1.set_PWM_frequency(L_RPWM, 800)
pi1.set_PWM_frequency(L_FPWM, 800)
pi1.set_PWM_frequency(R_RPWM, 800)
pi1.set_PWM_frequency(R_FPWM, 800)

#Networking config
UDP_IP = '127.0.0.1' #IP of vehicle
UDP_PORT = 5005 #Port to listen on

#Starts network socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))


while True:
    data, addr = s.recvfrom(1024)
    msg = pickle.loads(data)
    
    #Left Motor
    if msg[1] >= 155:
        print(msg[1])
        pi1.write(L_EN, 1)
        pi1.set_PWM_dutycycle(L_RPWM, 0) # Disables reverse PWM
        pi1.set_PWM_dutycycle(L_FPWM, msg[1]-100) # msg[1] is joystick value max of 255
    elif msg[1] <= 100:
        print(msg[1])
        pi1.write(L_EN, 1)
        pi1.set_PWM_dutycycle(L_FPWM, 0) # 0% dutycycle
        pi1.set_PWM_dutycycle(L_RPWM, 255-msg[1]-100) # Inverts logic to make joystick value 0 == PWM 255
    elif msg[1] > 100 and msg[1] < 155:
        pi1.write(L_EN, 0) #Disables Left Driver if joystick is in deadzone
    
    #Right Motor
    if msg[2] >= 155:
        print(msg[2])
        pi1.write(R_EN, 1)
        pi1.set_PWM_dutycycle(R_RPWM, 0) # Disables reverse PWM
        pi1.set_PWM_dutycycle(R_FPWM, msg[2]-100) # msg[1] is joystick value max of 255
    elif msg[2] <= 100:
        print(msg[1])
        pi1.write(R_EN, 1)
        pi1.set_PWM_dutycycle(R_FPWM, 0) # 0% dutycycle
        pi1.set_PWM_dutycycle(R_RPWM, 255-msg[2]-100) # Inverts logic to make joystick value 0 == PWM 255
    elif msg[2] > 100 and msg[1] < 155:
        pi1.write(R_EN, 0) #Disables Left Driver if joystick is in deadzone
