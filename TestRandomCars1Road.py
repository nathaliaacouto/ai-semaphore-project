# this is the second test, in it, there will be:
# 1 traffic light
# random number of cars whithin the range 5-30, each car has a random speed from 0.2 to 1
# 1 road with 1 lane
# the purpose of this test is to see how much time the car awaits in the red light

import spade
import asyncio
import sys
import time as t
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour

GREEN_LIGHT = "Green"
YELLOW_LIGHT = "Yellow"
RED_LIGHT = "Red"
AWAITING_TIME_TOTAL = 0

start_position_car_first_light = 0
position_first_light = 1


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
    # Behaviour

    def __init__(self, time, position, number, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.color = "Green"
        self.time = time
        self.position = position
        self.number = number

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
            if self.agent.position == self.agent.position:
                self.agent.creation_time = t.time() # the time car enters the road

            while self.agent.position != self.agent.traffic_light.position:
                self.agent.position += self.agent.speed 
                await asyncio.sleep(0.5)

            # after the car reached the traffic light
            if self.agent.position == 1:                 
                while True:
                    light_color = self.agent.traffic_light.get_color()

                    if light_color == "Green": 
                        # if the light is green, check how much time the car was waiting and let it go
                        global AWAITING_TIME_TOTAL
                        total_stop_time = self.agent.waiting_time
                        AWAITING_TIME_TOTAL += total_stop_time

                        print(f"Green, going. The car was in the red light {self.agent.traffic_light.number} for {total_stop_time:.2f} seconds")
                        
                        self.kill(exit_code=10) # if the car went ahead, it doesn't matter to this test anymore
                        break # get out of the loop

                    elif light_color == "Red" and self.agent.waiting_time == 0:
                        # if the light is red and the car just got there (the waiting time is still zero):
                        # this is the time the car reached the traffic light
                        self.agent.reached_light_time = t.time()

                    if light_color == "Red":
                        # if the light is red, add to the waiting time of the agent:
                        # the time now minus the time it reached the red light 
                        # (so it doesn't count the time it was driving to get to the light, just the time it is waiting)
                        self.agent.waiting_time = t.time() - self.agent.reached_light_time
                    
                    await asyncio.sleep(1) # await a bit to check the light again

    def __init__(self, speed, position, traffic_light, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.waiting_time = 0
        self.traffic_light = traffic_light
        self.position = position
        self.speed = speed
        self.creation_time = 0 # stores the time the car is created
        self.reached_light_time = 0 # stores the time the car gets in the light

    def stop_on_light(self, color):
        if color == "Red":
            print("Stop, red light")

    async def setup(self):
        await super().setup()
        behaviour = self.VehicleBehav()
        self.add_behaviour(behaviour)


class Road(Agent):
    def __init__(self, name, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.road_name = name
        self.lanes = 1
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)


async def main():
    light_time = 60 # doesn't really matter now
    traffic_light_agent = TrafficLight(light_time, position_first_light, 1, "admin@localhost", "password")
    await traffic_light_agent.start()

    road = Road("road one", "admin@localhost", "password")

    await asyncio.sleep(30)

    for i in range(random.randint(5, 30)):
        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent1 = Vehicle(speed, start_position_car_first_light, traffic_light_agent, "admin@localhost", "password")
        await vehicle_agent1.start()

        road.add_car(vehicle_agent1)

        await asyncio.sleep(5);

    print(f"Total awaiting time for all cars = {AWAITING_TIME_TOTAL:.2f} seconds")
    print(f"Medium awaiting time for one car = {(AWAITING_TIME_TOTAL/10):.2f} seconds")

    sys.exit()


if __name__ == "__main__":
    spade.run(main())