# RC Speed Tank Controller
A wireless control script written in python 2.7 to control an RC tank using two raspberry pi's and a ps3 controller

## About the project:
This project was my solution to driving an 3d printed vehicle known as the RC Speed Tank by Staind: https://www.thingiverse.com/thing:2414983. I use two raspberry pi's a 3A+ on the tank and a 3B+ that will go inside of a controller. I use the + models because they have support for 5ghz which comes in handy as these Pi's also stream a TCP Video stream. The tank uses 2x 540 45T stock motors driven by 2x BTS7960 H-Bridge motor controllers using PWM. Eventually this will turn into a full build log but for now I'm posting the Tank.py and Client.py scripts for review.

## Dependencies:
**Client.py**
 - Python 2.7
 - Evdev
 
**Tank.py**
 - Python 2.7
 - Pigpio
 
 ### Notes:
 This script is largely based off of https://github.com/KeplerElectronics/Basic_Analog_Drive. I modified it for use over wifi instead of bluetooth and to use my motor controllers instead of his.
