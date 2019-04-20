#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

GPIOMode = GPIO.BOARD
GPIOPin = 12
GPIOType = GPIO.OUT
GPIOHz = 50
PulseDut = 50
PinRef = None

GPIO.setmode(GPIOMode)
GPIO.setup(GPIOPin, GPIOType)

def help():
    print("""
cmd:
    1. r-run
    2. p-in
    3. f-frequency
    4. d-dut
    """)

def run():

    global GPIOMode
    global GPIOPin
    global GPIOType
    global GPIOHz
    global PulseDut

    GPIO.setmode(GPIOMode)
    GPIO.setup(GPIOPin, GPIOType)
    PinRef = GPIO.PWM(GPIOPin, GPIOHz)
    PinRef.start(0)
    PinRef.ChangeDutyCycle(PulseDut)

  
def PWM():

    global GPIOMode
    global GPIOPin
    global GPIOType
    global GPIOHz
    global PulseDut

    run()

    try:
        while True:
            cmd = input("Enter cmd(r-run, p-in, f-frequency, d-dut: ")

            if cmd != "r":
                PinRef.stop()

            if cmd == "p":
                GPIOPin = input("value: ")

            if cmd == "f":
                GPIOHz = input("value: ")

            if cmd == "d":
                PulseDut = input("value: ")

            if cmd == "r":
                run()

    except KeyboardInterrupt:
        pass

    PinRef.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    help()
    PWM()
