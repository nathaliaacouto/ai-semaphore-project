# this is the simplest test of all, in this test, there will be:
# 1 traffic light
# 10 cars 
# the purpose of this test is to see how much time the car awaits in the red light

import spade
import asyncio
import sys
import time as t
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour

GREEN_LIGHT = "Green"
YELLOW_LIGHT = "Yellow"
RED_LIGHT = "Red"
AWAITING_TIME_TOTAL = 0

class TrafficLight(Agent):
    # Behaviour
    class TrafficLightBehav(CyclicBehaviour):
        async def run(self):
            print(self.agent.color)
            await asyncio.sleep(24) # green light on for 24 seconds

            self.agent.change_color()
            print(self.agent.color)  
            await asyncio.sleep(5) # yellow light on for 5 seconds

            self.agent.change_color()
            print(self.agent.color)  
            await asyncio.sleep(30) # red light on for 30 seconds

            self.agent.change_color()

            #self.kill(exit_code=10)
    # Behaviour

    def __init__(self, time, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.color = "Green"
        self.time = time

    def change_time(self, new_time):
        self.time = new_time

    def change_color(self):
        if self.color == GREEN_LIGHT:
            self.color = YELLOW_LIGHT
        elif self.color == YELLOW_LIGHT:
            self.color = RED_LIGHT
        elif self.color == RED_LIGHT:
            self.color = GREEN_LIGHT

    def get_color(self):
        return self.color

    async def setup(self):
        await super().setup()
        behaviour = self.TrafficLightBehav()
        self.add_behaviour(behaviour)


class Vehicle(Agent):
    class VehicleBehav(CyclicBehaviour):
        async def run(self):
            while True:
                if self.agent.traffic_light.get_color() == "Green": 
                    if self.agent.waiting_time is not None:
                        global AWAITING_TIME_TOTAL
                        total_stop_time = t.time() - self.agent.waiting_time
                        AWAITING_TIME_TOTAL += total_stop_time
                        print(f"Green, going. The car was in the red light for {total_stop_time:.2f} seconds")
                    self.kill(exit_code=10) # if it went ahead, it doesn't matter to this test anymore
                    break
                elif self.agent.traffic_light.get_color() == "Red" and self.agent.waiting_time is None:
                    self.agent.waiting_time = t.time()
                
                await asyncio.sleep(1)

    def __init__(self, traffic_light, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.waiting_time = None
        self.traffic_light = traffic_light

    def stop_on_light(self, color):
        if color == "Red":
            print("Stop, red light")

    async def setup(self):
        await super().setup()
        behaviour = self.VehicleBehav()
        self.add_behaviour(behaviour)


async def main():
    light_time = 60 # doesn't really matter now
    traffic_light_agent = TrafficLight(light_time, "admin@localhost", "password")
    await traffic_light_agent.start()

    await asyncio.sleep(20)
    for i in range(10):
        vehicle_agent = Vehicle(traffic_light_agent, "admin@localhost", "password")
        await vehicle_agent.start()

        await asyncio.sleep(5);

    print(f"Total awaiting time for all cars = {AWAITING_TIME_TOTAL:.2f} seconds")
    print(f"Medium awaiting time for one car = {(AWAITING_TIME_TOTAL/10):.2f} seconds")

    sys.exit()


if __name__ == "__main__":
    spade.run(main())
