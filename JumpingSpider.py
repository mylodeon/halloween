#!/usr/bin/python

import time
import ControlModule
import asyncio
import os
import sys
from subprocess import Popen

class JumpingSpider:
    def __init__(self):
        self.control = ControlModule.ControlModule(self.go)

    def stopAudio(self):
        os.system('pkill -9 mplayer')
    
    async def reset(self):
        self.control.debugOn(0)
        self.control.debugOn(3)
        print("Resetting JumpingSpider")
        self.stopAudio()
        result = await self.control.spinMotor(0, 60, 1, lambda: self.control.isButtonPressed(0))
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

            print("Starting sound")
            basecmd = ["mplayer", "-ao", "alsa:device=bluealsa"]
            if sys.platform == 'win32':
                basecmd = ["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"]

            myfile = "jump.wav"
            self.audioPlayer = Popen(basecmd + [myfile])

        return False


    async def go(self):
        if not self.control.isButtonPressed(0):
            print("Spider is not ready - resetting")
            return await self.reset()

        self.control.enableLed(0)

        print("Spider is locked and loaded - performing initial jump")
        self.playfile = True
        self.control.debugOn(0)
        result = await self.control.spinMotor(0, 10, 1, lambda: self.startPlayingFile())

        self.control.debugOn(1)
        self.playfile = True

        print("Waiting for effect")
        result = await asyncio.sleep(3.5)
        self.control.debugOn(2)

        print("Bringing spider back in")
        result = await self.control.spinMotor(0, 30, 1, lambda: self.control.isButtonPressed(0))
        self.control.debugOn(3)

        if self.audioPlayer:
            self.audioPlayer.wait()

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
