#!/usr/bin/python

import PiMotor
import time
import RPi.GPIO as GPIO

class JumpingSpider:

    #Name of Individual MOTORS 
    m1 = PiMotor.Motor("MOTOR1",1)
    m2 = PiMotor.Motor("MOTOR2",1)
    m3 = PiMotor.Motor("MOTOR3",1)
    m4 = PiMotor.Motor("MOTOR4",1)

    #To drive all motors together
    motorAll = PiMotor.LinkedMotors(m1,m2,m3,m4)

    #Names for Individual Arrows
    ab = PiMotor.Arrow(1)
    al = PiMotor.Arrow(2)
    af = PiMotor.Arrow(3) 
    ar = PiMotor.Arrow(4)

    ##This segment drives the motors in the direction listed below:
    ## forward and reverse takes speed in percentage(0-100)

    def go(self):
    #-----------To Drive the Motors Forward------------# 
            print("Run")
            ab.on()
            m1.forward(100)
            time.sleep(5)
            m1.stop()
            ab.off()

