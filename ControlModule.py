#!/usr/bin/python

from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import Device, Motor
from time import sleep
from threading import Lock
import asyncio
import sys

class ControlModule:
    if sys.platform == 'win32':
        Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    #Name of Individual MOTORS 
    motor0 = Motor(forward=15, backward=13)
    motor1 = Motor(forward=16, backward=18)
    motor2 = Motor(forward=21, backward=23)
    motor3 = Motor(forward=24, backward=26)

    motors = [motor0, motor1, motor2, motor3]

    ##This segment drives the motors in the direction listed below:
    ## forward and reverse takes speed in percentage(0-100)

    iterationNumber = 1
    running = 0
    lock = Lock()

    def startRun(self):
        with self.lock:
            if (self.running == 1):
                return 0

            self.iterationNumber = self.iterationNumber + 1
            self.running = 1
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

    def isCancelled(self, runIter):
        with self.lock:
            return self.iterationNumber != runIter

    def isBusy(self):
        with self.lock:
            return self.running == 1

    async def spinMotor(self, motorNumber, duration, direction=1):
    #-----------To Drive the Motors Forward------------# 
        runId = self.startRun()
        if (runId == 0):
            print("Already running")
            return "Already running"

        try:
            print("Spinning " + str(motorNumber))

            motor = self.motors[motorNumber]
            if (direction == 1):
                print("Forward")
                motor.forward(1)
            else:
                print("Backward")
                motor.backward(1)
            
            remainingDuration = duration

            while remainingDuration > 0:
                await asyncio.sleep(0.25)
                remainingDuration -= 0.25
                if (self.isCancelled(runId)):
                    break

            print("Stop")
            motor.stop()

        finally:
            self.stopRun()
        
        print("Stop spinning " + str(motorNumber))
        return "Done"

    def stop(self):
        self.stopNow()
        return "Stopped"

