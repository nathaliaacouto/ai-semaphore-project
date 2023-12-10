# this test is 2 crossroads, in it, there is:
# 4 traffic lights with position and color 
#   when TL1 is open, TL3 is also open, the others are closed
#   when TL2 is open, TL4 is also open, the others are closed
# 100 cars, 
#   each car has a position and a random speed from 0.2 to 1 
#   each car can only go *forward*
# 4 roads with 2 lanes each
# 
# rules: 
# none


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
awaiting_time_total = 0

position_ligths = [1, 3, 5, 7]
start_position_cars = [0, 2, 4, 6] 
awaiting_time_for_light = [0, 0, 0, 0]
vehicles_times = [[], [], [], []]
vehicles_lines = [[], [], [], []]

class TrafficLight(Agent):
    # Behaviour
    class TrafficLightBehav(CyclicBehaviour):
        async def run(self):
            print(f"Traffic Light {self.agent.number} - {self.agent.color}")
            if self.agent.color == "Green":
                await asyncio.sleep(22) 
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

    def central_change_color(self, color):
        self.color = color

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
            for i in range(len(position_ligths)):
                if self.agent.traffic_light.number == i: # if light 1, 2, 3, 4
                    position_light = position_ligths[i-1] # position 0 in list

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
                        global awaiting_time_total
                        total_stop_time = self.agent.waiting_time
                        for i in range(len(position_ligths)):
                            if self.agent.traffic_light.number == i+1: # if light 1, 2, 3, 4
                                vehicles_times[i].append(round(total_stop_time, 2));
                        awaiting_time_total += total_stop_time
                        awaiting_time_for_light[(self.agent.traffic_light.number)-1] += total_stop_time

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
                        for i in range(len(position_ligths)):
                            if self.agent.traffic_light.number == i: # if light 1, 2, 3, 4
                                vehicles_lines[i].append(1)
                                # add a number insed of the line if it is waiting (the number doesn't matter, just to know how many cars are waiting)
                    
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

    def get_await_time(self):
        return self.waiting_time

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
    start_time = t.time();
    light_time = 60 # doesn't really matter now
    traffic_light_agent1 = TrafficLight("Green", light_time, position_ligths[0], 1, "admin@localhost", "password")
    await traffic_light_agent1.start()

    traffic_light_agent2 = TrafficLight("Red", light_time, position_ligths[1], 2, "admin@localhost", "password")
    await traffic_light_agent2.start()

    traffic_light_agent3 = TrafficLight("Green", light_time, position_ligths[2], 3, "admin@localhost", "password")
    await traffic_light_agent3.start()

    traffic_light_agent4 = TrafficLight("Red", light_time, position_ligths[3], 4, "admin@localhost", "password")
    await traffic_light_agent4.start()

    road_agent1 = Road("2450", 2, "admin@localhost", "password")
    road_agent2 = Road("4763", 2, "admin@localhost", "password")

    count_vehicles = 0
    for i in range(25): # 100 cars
        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent1 = Vehicle(start_position_cars[0], speed, traffic_light_agent1, "admin@localhost", "password")
        await vehicle_agent1.start()
        road_agent1.add_vehicle(0, start_position_cars[0], speed, traffic_light_agent1, "admin@localhost", "password")

        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent2 = Vehicle(start_position_cars[1], speed, traffic_light_agent2, "admin@localhost", "password")
        await vehicle_agent2.start()
        road_agent2.add_vehicle(0, start_position_cars[1], speed, traffic_light_agent2, "admin@localhost", "password")

        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent3 = Vehicle(start_position_cars[2], speed, traffic_light_agent3, "admin@localhost", "password")
        await vehicle_agent3.start()
        road_agent1.add_vehicle(1, start_position_cars[2], speed, traffic_light_agent3, "admin@localhost", "password")

        speed = round(random.uniform(0.2, 1.0), 1)
        vehicle_agent4 = Vehicle(start_position_cars[3], speed, traffic_light_agent4, "admin@localhost", "password")
        await vehicle_agent4.start()
        road_agent2.add_vehicle(1, start_position_cars[3], speed, traffic_light_agent4, "admin@localhost", "password")

        count_vehicles = count_vehicles + 4 # this will count the vehicles, since we have 4 agents being created, we need +4
        await asyncio.sleep(5);

    await asyncio.sleep(10);

    print("\n----- TOTAL -----")
    print(f"Total awaiting time for all {count_vehicles} vehicles = {awaiting_time_total:.2f} seconds")
    print(f"Medium awaiting time for one vehicle = {(awaiting_time_total/count_vehicles):.2f} seconds")

    for i in range(len(awaiting_time_for_light)):
        vehicles_in_one_light = count_vehicles/4
        print(f"\n----- LIGHT {i+1} -----")
        print(f"Total awaiting time for light {i+1}: {awaiting_time_for_light[i]:.2f} seconds")
        print(f"Medium awaiting time one vehicle in light {i+1}: {(awaiting_time_for_light[i]/vehicles_in_one_light):.2f} seconds")

    finish_time = t.time();
    print(f"time: {(finish_time - start_time):.2f}")

    for i in range(4):
        print(vehicles_times[i])
    
    f = open("ai-semaphore-project/comparisons/documents/test1.txt", "a")
    f.write(f"\nTotal awaiting time for all {count_vehicles} vehicles = {awaiting_time_total:.2f} seconds\nMedium awaiting time for one vehicle = {(awaiting_time_total/count_vehicles):.2f} seconds \n")
    f.write(f"Execution time: {(finish_time - start_time)/60:.2f} minutes\n")
    for i in range(4):
        f.write(f"Semaphore {i} times (in seconds): {vehicles_times[i]}\n");
    f.write("\nNext Test\n")
    f.close()

    sys.exit()


if __name__ == "__main__":
    spade.run(main())
