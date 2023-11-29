# this test is 2 crossroads, in it, there is:
# 4 traffic lights with position and color 
#   when TL1 is open, TL3 is also open, the others are closed
#   when TL2 is open, TL4 is also open, the others are closed
# a random number of cars whithin the random range 5-30 * 4, 
#   each car has a position and a random speed from 0.2 to 1 
#   each car can only go *forward*
# 4 roads with 2 lanes each
# the purpose of this test is to see how much time the car awaits in the red light

import random
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

start_position_car_first_light = 0
position_first_light = 1
start_position_car_second_light = 2
position_second_light = 3
start_position_car_third_light = 4
position_third_light = 5
start_position_car_fourth_light = 6
position_fourth_light = 7

class TrafficLight(Agent):
    # Behaviour
    class TrafficLightBehav(CyclicBehaviour):
        async def run(self):
            print(f"Traffic Light {self.agent.number} - {self.agent.color}")
            if self.agent.color == "Green":
                await asyncio.sleep(23) 
                self.agent.change_color()
            elif self.agent.color == "Yellow":
                await asyncio.sleep(5)
                self.agent.change_color()
            elif self.agent.color == "Red":
                await asyncio.sleep(30) 
                self.agent.change_color()
    # Behaviour

    def __init__(self, color, time, postion, number, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.color = color
        self.time = time
        self.position = postion
        self.number = number

    def get_number(self):
        return self.number

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
            position_light = 0
            if self.agent.traffic_light.number == 1:
                position_light = position_first_light
            elif self.agent.traffic_light.number == 2:
                position_light = position_second_light

            if self.agent.position == self.agent.start_position:
                self.agent.creation_time = t.time() # the time car enters the road

            while self.agent.position <= position_light:
                self.agent.position += self.agent.speed # the car goes 0.2 per second (speed)
                await asyncio.sleep(0.5)

            # after the car reached the traffic light
            if self.agent.position >= position_light:    
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

    def __init__(self, start_position, speed, traffic_light, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.waiting_time = 0
        self.traffic_light = traffic_light
        self.position = start_position
        self.start_position = start_position
        self.creation_time = 0
        self.reached_light_time = 0 # stores the time the car gets in the light
        self.speed = speed

    def stop_on_light(self, color):
        if color == "Red":
            print("Stop, red light")

    async def setup(self):
        await super().setup()
        behaviour = self.VehicleBehav()
        self.add_behaviour(behaviour)

class Lane(Agent):
    def __init__(self, lane_id, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.lane_id = lane_id
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)


class Road(Agent):
    def __init__(self, name, num_lanes, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.road_name = name
        self.lanes = [Lane(i, jid, password) for i in range(num_lanes)]
        self.num_lanes = num_lanes

    def add_vehicle(self, num_lane, position, speed, light, jid, password):
        vehicle = Vehicle(position, speed, light, jid, password)
        self.lanes[num_lane].add_vehicle(vehicle)


async def main():
    light_time = 60 # doesn't really matter now
    traffic_light_agent1 = TrafficLight("Green", light_time, position_first_light, 1, "admin@localhost", "password")
    await traffic_light_agent1.start()

    traffic_light_agent2 = TrafficLight("Red", light_time, position_second_light, 2, "admin@localhost", "password")
    await traffic_light_agent2.start()

    traffic_light_agent3 = TrafficLight("Green", light_time, position_third_light, 3, "admin@localhost", "password")
    await traffic_light_agent3.start()

    traffic_light_agent4 = TrafficLight("Red", light_time, position_second_light, 4, "admin@localhost", "password")
    await traffic_light_agent4.start()

    road_agent1 = Road("2450", 2, "admin@localhost", "password")
    road_agent2 = Road("4763", 2, "admin@localhost", "password")

    await asyncio.sleep(10)

    count_vehicles = 0
    for i in range(random.randint(5, 30)):
        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent1 = Vehicle(start_position_car_first_light, speed, traffic_light_agent1, "admin@localhost", "password")
        await vehicle_agent1.start()
        road_agent1.add_vehicle(0, start_position_car_first_light, speed, traffic_light_agent1, "admin@localhost", "password")

        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent2 = Vehicle(start_position_car_second_light, speed, traffic_light_agent2, "admin@localhost", "password")
        await vehicle_agent2.start()
        road_agent2.add_vehicle(0, start_position_car_second_light, speed, traffic_light_agent2, "admin@localhost", "password")

        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent3 = Vehicle(start_position_car_third_light, speed, traffic_light_agent3, "admin@localhost", "password")
        await vehicle_agent3.start()
        road_agent1.add_vehicle(1, start_position_car_third_light, speed, traffic_light_agent3, "admin@localhost", "password")

        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent4 = Vehicle(start_position_car_fourth_light, speed, traffic_light_agent4, "admin@localhost", "password")
        await vehicle_agent4.start()
        road_agent2.add_vehicle(1, start_position_car_fourth_light, speed, traffic_light_agent4, "admin@localhost", "password")

        count_vehicles = count_vehicles + 4 # this will count the vehicles, since we have 4 agents being created, we need +4
        await asyncio.sleep(5);

    await asyncio.sleep(10);

    print(f"Total awaiting time for all {count_vehicles} vehicles = {AWAITING_TIME_TOTAL:.2f} seconds")
    print(f"Medium awaiting time for one vehicle = {(AWAITING_TIME_TOTAL/count_vehicles):.2f} seconds")

    sys.exit()


if __name__ == "__main__":
    spade.run(main())