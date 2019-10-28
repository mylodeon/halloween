#!/usr/bin/python

import time
import ControlModule
import asyncio
import os
import sys
from subprocess import Popen
import pygame

class JumpingSpider:
    def __init__(self):
        self.control = ControlModule.ControlModule(self.go)
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        #pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 1024)
        self.sound = pygame.mixer.Sound("jump.wav")

    def stopAudio(self):
        self.sound.stop()
        return
    
    async def reset(self):
        self.control.debugOn(0)
        self.control.debugOn(3)
        print("Resetting JumpingSpider")
        self.stopAudio()
        result = await self.control.spinMotor(0, 60, 1, lambda: self.control.isButtonPressed(0))

        print("Adding another 2 seconds")
        result = await self.control.spinMotor(0, 2, 1)

        self.control.debugOff(0)
        self.control.debugOff(3)
        print("Done resetting JumpingSpider")
        return result

    playfile = True
    audioPlayer = None

    def startPlayingFile(self):
        if not self.playfile:
            return False

        if not self.control.isButtonPressed(0):
            self.playfile = False
            self.sound.play()

        return False

    async def go(self):
        if not self.control.isButtonPressed(0):
            print("Spider is not ready - resetting")
            return await self.reset()

        self.control.enableLed(0)

        print("Spider is locked and loaded - performing initial jump")
        self.playfile = True
        self.control.debugOn(0)

        print("Play")
        result = await self.control.spinMotor(0, 10, 1, lambda: self.startPlayingFile())
        self.control.debugOn(1)

        print("Bringing spider back in")
        result = await self.control.spinMotor(0, 60, 1, lambda: self.control.isButtonPressed(0))
        self.control.debugOn(2)

        print("Adding another 2 seconds")
        result = await self.control.spinMotor(0, 2, 1)
        self.control.debugOn(3)

        self.control.disableLed(0)
        self.control.debugOff(0)
        self.control.debugOff(1)
        self.control.debugOff(2)
        self.control.debugOff(3)

        print("JumpingSpider done")
        return result

    def start(self):
        return self.control.start()

    def stop(self):
        self.stopAudio()
        return self.control.stop()
