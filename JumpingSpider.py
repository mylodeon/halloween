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

    async def reset(self):
        print("Resetting JumpingSpider")
        os.system('pkill -9 mplayer')
        result = await self.control.spinMotor(0, 60, 1, lambda: self.control.isButtonPressed(0))
        print("Done resetting JumpingSpider")
        return result

    async def go(self):
        if not self.control.isButtonPressed(0):
            return await self.reset()

        self.control.enableLed(0)

        print("Spider is locked and loaded - performing initial jump")
        task = self.control.spinMotor(0, 4, 1)

        basecmd = ["mplayer", "-ao", "alsa:device=bluealsa"]
        await task

        if sys.platform == 'win32':
            basecmd = ["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"]

        myfile = "jump.wav"
        Popen(basecmd + [myfile])

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
        return self.control.stop()
