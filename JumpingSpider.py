#!/usr/bin/python

import time
import ControlModule
import asyncio
import concurrent;
import threading;

class JumpingSpider:

    #Name of Individual MOTORS 
    control = ControlModule.ControlModule()
    iter = 1

    loop = asyncio.new_event_loop()
    pool = concurrent.futures.ProcessPoolExecutor()

    busy = 0

    ##This segment drives the motors in the direction listed below:
    ## forward and reverse takes speed in percentage(0-100)

    async def go(self):
    #-----------To Drive the Motors Forward------------# 
        print("Go thread:" + str(threading.current_thread().ident))
        self.iter = self.iter + 1
        print("Go " + str(self.iter))
        print(threading.current_thread().ident)
        result = await self.control.spinMotor(0, 10, 1)
        print("Go " + str(self.iter) + " done")
        return result

    def target(self, timeout=None):
        print("Target  thread:" + str(threading.current_thread().ident))
        try:
            self.busy = 1
            print("Target")
            print(threading.current_thread().ident)
            asyncio.set_event_loop(self.loop)
            asyncio.run(self.go())
            print("Target done")
        finally:
            self.busy = 0

    def start(self):
        if self.busy == 1:
            return "Busy"

        print("Start")
        print("Start thread:" + str(threading.current_thread().ident))
        self.loop.run_in_executor(self.pool, self.target)
        print("Start done")
        return "Starting execution"

    def stop(self):
    #-----------To Drive the Motors Forward------------# 
        return self.control.stop()
