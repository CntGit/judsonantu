#avg value set as 8423000
#reducing avg value with live value

import RPi.GPIO as gpio
import threading
import time

DAT = 13
CLK = 8
num = 0

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(CLK, gpio.OUT)

def weight():
    i = 0
    num = 0
    gpio.setup(DAT,gpio.OUT)
    gpio.output(DAT,True)
    gpio.output(CLK,False)
    gpio.setup(DAT,gpio.IN)

    while gpio.input(DAT) == 1:
        i = 0
    for i in range(24):
        gpio.output(CLK,True)
        num = num<<1
        gpio.output(CLK,False)
        if gpio.input(DAT) == 0:
            num = num+1

    gpio.output(CLK,True)
    num = num^0x800000
    gpio.output(CLK,False)
    #print(num)
    time.sleep(0.1)
    return num

#use the below code while useing load_cell.py independently
"""while True:
    wei = weight()
    mass = 8423200 - wei
    print(int(mass/425))"""
