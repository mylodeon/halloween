#!/usr/bin/python

import time
import ControlModule
import asyncio

class JumpingSpider:
    def __init__(self):
        self.control = ControlModule.ControlModule(self.go)

    async def reset(self):
        print("Resetting JumpingSpider")
        result = await self.control.spinMotor(0, 60, 1, lambda: self.control.isButtonPressed(0))
        print("Done resetting JumpingSpider")
        return result

    async def go(self):
        if not self.control.isButtonPressed(0):
            return await self.reset()

        print("Spider is locked and loaded - performing initial jump")
        result = await self.control.spinMotor(0, 4, 1)
        
        print("Waiting for effect")
        result = await asyncio.sleep(3.5)

        print("Bringing spider back in")
        result = await self.control.spinMotor(0, 20, 1, lambda: not self.control.isButtonPressed(0))

        print("JumpingSpider done")
        return result

    def start(self):
        return self.control.start()

    def stop(self):
        return self.control.stop()
