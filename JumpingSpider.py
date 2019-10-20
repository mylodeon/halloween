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
        print("Resetting JumpingSpider")
        self.stopAudio()
        result = await self.control.spinMotor(0, 60, 1, lambda: self.control.isButtonPressed(0))
        print("Done resetting JumpingSpider")
        return result

    playfile = True

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
            Popen(basecmd + [myfile])

        return False


    async def go(self):
        if not self.control.isButtonPressed(0):
            return await self.reset()

        self.control.enableLed(0)

        print("Spider is locked and loaded - performing initial jump")
        self.playfile = True
        result = await self.control.spinMotor(0, 4, 1, lambda: self.startPlayingFile())
        self.playfile = True

        print("Waiting for effect")
        result = await asyncio.sleep(3.5)

        print("Bringing spider back in")
        result = await self.control.spinMotor(0, 20, 1, lambda: not self.control.isButtonPressed(0))

        self.control.disableLed(0)
        print("JumpingSpider done")
        return result

    def start(self):
        return self.control.start()

    def stop(self):
        self.stopAudio()
        return self.control.stop()
