#!/usr/bin/python

from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import Device, Motor, Button, LED
from time import sleep
from threading import Lock
import asyncio
import sys
import concurrent
import threading

class ControlModule:
    if sys.platform == 'win32':
        Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    pool = concurrent.futures.ProcessPoolExecutor()

    #Name of Individual MOTORS 
    motor0 = Motor(forward=22, backward=27, enable=17)
    motor1 = Motor(forward=23, backward=24, enable=25)
    motor2 = Motor(forward=9, backward=11, enable=10)
    motor3 = Motor(forward=8, backward=7, enable=12)

    motors = [motor0, motor1, motor2, motor3]

    button0 = Button(16)
    button1 = Button(20)
    button2 = Button(21)
    button3 = Button(26)

    buttons = [button0, button1, button2,button3]

    led0 = LED(19)
    led1 = LED(13)
    led2 = LED(6)
    led3 = LED(5)

    leds = [led0, led1, led2, led3]

    if sys.platform == 'win32':
        Device.pin_factory.pin(16).drive_low()

    iterationNumber = 1
    currentRun = 0
    running = 0
    lock = Lock()

    def __init__(self, goroutine):
        self.go = goroutine

    def startRun(self):
        with self.lock:
            if (self.running == 1):
                return 0

            self.iterationNumber = self.iterationNumber + 1
            self.running = 1
            self.currentRun = self.iterationNumber
            return self.iterationNumber

    def stopRun(self):
        with self.lock:
            self.iterationNumber = self.iterationNumber + 1
            self.running = 0
            return self.iterationNumber

    def stopNow(self):
        with self.lock:
            self.iterationNumber = self.iterationNumber + 1
            return self.iterationNumber

    def isCancelled(self):
        with self.lock:
            return self.iterationNumber != self.currentRun

    def isBusy(self):
        with self.lock:
            return self.running == 1

    def isButtonPressed(self, buttonNumber):
        button = self.buttons[buttonNumber]
        result = button.is_pressed
        return result

    def enableLed(self, ledNumber):
        led = self.leds[ledNumber]
        led.on()
        
    def disableLed(self, ledNumber):
        led = self.leds[ledNumber]
        led.off()

    async def spinMotor(self, motorNumber, duration, direction=1, stopRoutine=None):
        if (self.isCancelled()):
            return "Cancelled"

        if stopRoutine:
            if stopRoutine():
                return "Stopped"

        motor = self.motors[motorNumber]
        if (direction == 1):
            print("Forward " + str(motorNumber))
            motor.forward(1)
        else:
            print("Backward " + str(motorNumber))
            motor.backward(1)
        
        remainingDuration = duration

        while remainingDuration > 0:
            if stopRoutine:
                if stopRoutine():
                    break

            await asyncio.sleep(0.05)
            remainingDuration -= 0.05
            if (self.isCancelled()):
                break

        motor.stop()
        print("Stopped spinning " + str(motorNumber))

        return "Done"

    def target(self):
        print("Target  thread:" + str(threading.current_thread().ident))
        try:
            self.startRun()
            loop = asyncio.new_event_loop()
            print("Target")
            print(threading.current_thread().ident)
            loop.run_until_complete(self.go())
            print("Target done")
        finally:
            self.stopRun()

    def start(self):
        runId = self.startRun()
        if (runId == 0):
            print("Already running")
            return "Already running"

        print("Start thread:" + str(threading.current_thread().ident))
        thread = threading.Thread(target=self.target)
        thread.start()

        return "Starting execution"

    def stop(self):
        self.stopNow()
        return "Stopped"


