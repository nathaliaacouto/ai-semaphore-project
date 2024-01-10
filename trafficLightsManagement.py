# this test is 2 crossroads, in it, there is:
# 4 traffic lights with position and color 
#   when TL1 is open, TL3 is also open, the others are closed
#   when TL2 is open, TL4 is also open, the others are closed
# 100 cars in 3min 
#   each car has a position and a random speed from 0.2 to 1 
#   each car can only go *forward*
#   when approaching the red light, the car slows down and stops
# 4 roads with 2 lanes each
# 
# rules: 
# central agent controls the lights color's
# the light with more cars on the queue is turned on with a sleep time of 5s
# when the emergency vehicle shows up, the light turns on


import random
import spade
import asyncio
import sys
import time as t
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message

GREEN_LIGHT = "Green"
YELLOW_LIGHT = "Yellow"
RED_LIGHT = "Red"
NORMAL = "Normal"
ACCIDENT = "Accident"

emergency_vehicle = [0, 0]
emergency_vehicle_time = 0
awaiting_time_total = 0
accident = False
position_ligths = [1, 3, 5, 7]
start_position_cars = [0, 2, 4, 6] 
awaiting_time_for_light = [0, 0, 0, 0]
vehicles_times = [[], [], [], []] # stores the time the vehicle passed in the red light after it leaves
vehicles_queues = [[], [], [], []]
vehicles_queue_time = [[], [], [], []] # stores the time the vehicle is passing in the red light queue (currently)

class CentralCoordinationAgent(Agent):
    # Behaviour
    class CentralCoordinationBehav(CyclicBehaviour):
        async def on_start(self):
            # the colors of the lights will be defined by the
            # biggest queue, so, when the program starts, the
            # coordination agent has to sleep a bit and let the cars
            # get to the lights, so we can have queues
            await asyncio.sleep(10) 
            print("Starting the traffic lights")
            await asyncio.sleep(1)
            print("Managing the traffic lights")

        async def run(self):
            emergency_light = 0
            if emergency_vehicle[0] == 1:
                print("Emergency!")    
                emergency_light = emergency_vehicle[1]

            # stores the traffic light with the biggest queue (+1 because list index starts with 0)
            biggest_queue = vehicles_queues.index(max(vehicles_queues, key=len)) + 1

            if((biggest_queue == 1 or emergency_light == 1) or (biggest_queue == 3 or emergency_light == 3)):
                    # if the 1 or 3 queue is the worst, turn green; 
                    # 1 green means 3 is green and 2 and 4 are red 
                    traffic_light_jid = "tf" + str(2) + "@localhost"
                    msg = Message(to="tf2@localhost")
                    msg.body = RED_LIGHT   
                    await self.send(msg)
                    traffic_light_jid = "tf" + str(4) + "@localhost"
                    msg = Message(to=traffic_light_jid)
                    msg.body = RED_LIGHT   
                    await self.send(msg)

                    await asyncio.sleep(6)
                    traffic_light_jid = "tf" + str(1) + "@localhost"
                    msg = Message(to=traffic_light_jid)
                    msg.body = GREEN_LIGHT   
                    await self.send(msg)
                    traffic_light_jid = "tf" + str(3) + "@localhost"
                    msg = Message(to=traffic_light_jid)
                    msg.body = GREEN_LIGHT   
                    await self.send(msg)

            elif((biggest_queue == 2 or emergency_light == 2) or (biggest_queue == 2 or emergency_light == 2)):
                    # if the 2 or 4 queue is the worst, turn green; 
                    # 2 green means 4 is green and 1 and 3 are red 
                    traffic_light_jid = "tf" + str(1) + "@localhost"
                    msg = Message(to=traffic_light_jid)
                    msg.body = RED_LIGHT   
                    await self.send(msg)
                    traffic_light_jid = "tf" + str(3) + "@localhost"
                    msg = Message(to=traffic_light_jid)
                    msg.body = RED_LIGHT   
                    await self.send(msg)

                    await asyncio.sleep(6)
                    traffic_light_jid = "tf" + str(2) + "@localhost"
                    msg = Message(to=traffic_light_jid)
                    msg.body = GREEN_LIGHT   
                    await self.send(msg)
                    traffic_light_jid = "tf" + str(4) + "@localhost"
                    msg = Message(to=traffic_light_jid)
                    msg.body = GREEN_LIGHT   
                    await self.send(msg)
            
            await asyncio.sleep(5)
    # Behaviour

    def __init__(self, tf1, tf2, tf3, tf4, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.traffic_lights = [tf1, tf2, tf3, tf4]

    async def setup(self):
        await super().setup()
        behaviour = self.CentralCoordinationBehav()
        self.add_behaviour(behaviour)


class DisruptionManagement(Agent):
    # Behaviour
    class DisruptionManagementBehav(CyclicBehaviour):
        async def on_start(self):
            # this agent verifies any special circustance 
            # and send a message to the vehicles if so
            print("Starting Disruption Management Agent")

        async def run(self):
            if accident == True:
                # if there is a accident, send message to cars walk slower 
                print("Accident! Cars will move slower")
                #msg = Message(to="car@localhost")
                #msg.body = ACCIDENT  
                #await self.send(msg)
            #else:
                #msg = Message(to="car@localhost")
                #msg.body = NORMAL 
                #await self.send(msg)
            
            await asyncio.sleep(5)
    # Behaviour

    def __init__(self, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)

    async def setup(self):
        await super().setup()
        behaviour = self.DisruptionManagementBehav()
        self.add_behaviour(behaviour)


class TrafficLight(Agent):
    # Behaviour
    class TrafficLightBehav(CyclicBehaviour):
        async def run(self):
            self.agent.count += 1
            msg = await self.receive(timeout= 400) # recieve a messagem from the central

            # if its not the first time the light turns red, change to yellow
            if self.agent.count > 1:
                if format(msg.body) == RED_LIGHT:
                    self.agent.color = YELLOW_LIGHT
                    print(f"Traffic Light {self.agent.number} - {self.agent.color}")
                    await asyncio.sleep(5)
                    self.agent.color = format(msg.body)

            # change the color according to the message
            self.agent.color = format(msg.body)

            print(f"Traffic Light {self.agent.number} - {self.agent.color}") 
    # Behaviour

    def __init__(self, postion, number, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.color = RED_LIGHT
        self.position = postion
        self.number = number
        self.count = 0

    def get_number(self):
        return self.number

    def get_color(self):
        return self.color

    def change_time(self, new_time):
        self.time = new_time

    def change_color(self, color):
        self.color = color

    async def setup(self):
        await super().setup()
        behaviour = self.TrafficLightBehav()
        self.add_behaviour(behaviour)
    

class Vehicle(Agent):
    class VehicleBehav(CyclicBehaviour):
        async def run(self):
            position_light = 0
            for i in range(len(position_ligths)):
                if self.agent.traffic_light.number == i+1: # if light 1, 2, 3, 4
                    position_light = position_ligths[i] # position in list

            # if the position of the car is the start position, it entered the road now
            if self.agent.position == self.agent.start_position:
                self.agent.creation_time = t.time() # the time car enters the road

            # while the car has not reached the light
            while self.agent.position <= position_light:
                light_color = self.agent.traffic_light.get_color()
                
                if accident == True:
                    self.agent.position += (self.agent.speed - 0.2)
                elif (light_color == RED_LIGHT) and (position_light - self.agent.position < 0.3):
                    # if the light is red and the car is getting close, slow down
                    self.agent.position += (self.agent.speed - 0.2)
                else:
                    self.agent.position += self.agent.speed 
                
                await asyncio.sleep(0.5)

            # after the car reached the traffic light
            if self.agent.position >= position_light:    
                count = 0
                while True:
                    light_color = self.agent.traffic_light.get_color()

                    # if the light is green, check how much time the car was waiting and let it go
                    if light_color == GREEN_LIGHT or light_color == YELLOW_LIGHT: 
                        total_stop_time = self.agent.waiting_time

                        for i in range(len(position_ligths)):
                            if self.agent.traffic_light.number == i+1: # if light 1, 2, 3, 4
                                vehicles_times[i].append(round(total_stop_time, 2));
                                if len(vehicles_queues[i]) != 0:
                                    vehicles_queues[i].pop() # takes a number off the waiting list 
                        
                        global awaiting_time_total
                        awaiting_time_total += total_stop_time
                        awaiting_time_for_light[(self.agent.traffic_light.number)-1] += total_stop_time

                        print(f"{light_color}, going. The car was in the red light {self.agent.traffic_light.number} for {total_stop_time:.2f} seconds")
                        
                        self.kill(exit_code=10) # if the car went ahead, it doesn't matter to this test anymore
                        break # get out of the loop

                    # if the light is red and the car just got there (the waiting time is still zero):
                    # this is the time the car reached the traffic light
                    elif light_color == RED_LIGHT and self.agent.waiting_time == 0:
                        self.agent.reached_light_time = t.time()

                    if light_color == RED_LIGHT:
                        count += 1
                        # if the light is red, add to the waiting time of the agent:
                        # the time now minus the time it reached the red light 
                        # (so it doesn't count the time it was driving to get to the light, just the time it is waiting)
                        self.agent.waiting_time = t.time() - self.agent.reached_light_time
                        if count == 1: # the first time it reaches the red light
                            for i in range(len(position_ligths)):
                                if self.agent.traffic_light.number == i+1: # if light 1, 2, 3, 4
                                    vehicles_queues[i].append(1)
                                    # add a number insed of the queue if it is waiting (the number 
                                    # doesn't matter, its just to know how many cars are waiting)
                    
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


class EmergencyVehicle(Agent):
    class EmergencyVehicleBehav(CyclicBehaviour):
        async def run(self):
            position_light = 0
            for i in range(len(position_ligths)):
                if self.agent.traffic_light.number == i+1: # if light 1, 2, 3, 4
                    position_light = position_ligths[i] # position in list

            # if the position of the vehicle is the start position, it entered the road now
            # when it enters, send a message to warn the traffic light to open
            if self.agent.position == self.agent.start_position:
                self.agent.creation_time = t.time() 

                global emergency_vehicle
                emergency_vehicle = [1, self.agent.traffic_light.number]

            # while it has not reached the light
            while self.agent.position < position_light:
                light_color = self.agent.traffic_light.get_color()
                # if the light is still red and the its getting close, slow down
                if (light_color == RED_LIGHT) and (position_light - self.agent.position < 0.3):
                    self.agent.position += (self.agent.speed - 0.2)
                else:
                    self.agent.position += self.agent.speed 
                
                await asyncio.sleep(0.5)

            # after the car reached the traffic light
            if self.agent.position >= position_light:    
                count = 0
                while True:
                    light_color = self.agent.traffic_light.get_color()

                    # if the light is green, check how much time it was waiting and let it go
                    if light_color == GREEN_LIGHT or light_color == YELLOW_LIGHT: 
                        total_stop_time = self.agent.waiting_time
                        
                        global emergency_vehicle_time
                        emergency_vehicle_time += total_stop_time

                        emergency_vehicle = [0, 0]

                        print(f"{light_color}, going. The {self.agent.emergency_name} was in the red light {self.agent.traffic_light.number} for {total_stop_time:.2f} seconds")
                        
                        self.kill(exit_code=10) # if it went ahead, it doesn't matter to this test anymore
                        break # get out of the loop

                    # if the light is red and it just got there (the waiting time is still zero):
                    # this is the time it reached the traffic light
                    elif light_color == RED_LIGHT and self.agent.waiting_time == 0:
                        self.agent.reached_light_time = t.time()

                    if light_color == RED_LIGHT:
                        count += 1
                        # if the light is red, add to the waiting time of the agent:
                        # the time now minus the time it reached the red light 
                        # (so it doesn't count the time it was driving to get to the light, just the time it is waiting)
                        self.agent.waiting_time = t.time() - self.agent.reached_light_time
                    
                    await asyncio.sleep(0.5) # await a bit to check the light again

    def __init__(self, start_position, speed, traffic_light, jid: str, password: str, verify_security: bool = False, *args,
                 **kwargs):
        super().__init__(jid, password, verify_security)
        names = ["Ambulance", "Police", "Firefighters"]
        self.emergency_name = random.choice(names) 
        self.waiting_time = 0
        self.traffic_light = traffic_light
        self.position = start_position
        self.start_position = start_position
        self.creation_time = 0
        self.reached_light_time = 0
        self.speed = speed

    def stop_on_light(self, color):
        if color == "Red":
            print("Emergency Vehicle - Stop, red light")

    def get_await_time(self):
        return self.waiting_time

    async def setup(self):
        await super().setup()

        behaviour = self.EmergencyVehicleBehav()
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
    # the time the program starts
    start_time = t.time();

    # create traffic lights
    traffic_light_agent1 = TrafficLight(position_ligths[0], 1, "tf1@localhost", "password")
    await traffic_light_agent1.start()

    traffic_light_agent2 = TrafficLight(position_ligths[1], 2, "tf2@localhost", "password")
    await traffic_light_agent2.start()

    traffic_light_agent3 = TrafficLight(position_ligths[2], 3, "tf3@localhost", "password")
    await traffic_light_agent3.start()

    traffic_light_agent4 = TrafficLight(position_ligths[3], 4, "tf4@localhost", "password")
    await traffic_light_agent4.start()

    # create central agent
    central_agent = CentralCoordinationAgent(traffic_light_agent1, traffic_light_agent2, traffic_light_agent3, traffic_light_agent4, "central@localhost", "password")
    await central_agent.start()

    # create disruption agent
    disruption_agent = DisruptionManagement("disruption@localhost", "password")
    await disruption_agent.start()

    # create roads
    road_agent1 = Road("2450", 2, "admin@localhost", "password")
    road_agent2 = Road("4763", 2, "admin@localhost", "password")

    # randomly generate accident when starting
    accident_happening = round(random.uniform(0, 4))
    if (accident_happening == 2):
        global accident
        accident = True

    # create vehicles
    count_vehicles = 0
    emergency_start = round(random.uniform(0, 25))
    for i in range(25): # range * 4 is the total number of vehicles created

        speed = round(random.uniform(0.4, 1.0), 1)
        vehicle_agent1 = Vehicle(start_position_cars[0], speed, traffic_light_agent1, "car@localhost", "password")
        await vehicle_agent1.start()
        road_agent1.add_vehicle(0, start_position_cars[0], speed, traffic_light_agent1, "admin@localhost", "password")

        speed = round(random.uniform(0.4, 1.0), 1)
        vehicle_agent2 = Vehicle(start_position_cars[1], speed, traffic_light_agent2, "car@localhost", "password")
        await vehicle_agent2.start()
        road_agent2.add_vehicle(0, start_position_cars[1], speed, traffic_light_agent2, "admin@localhost", "password")

        if emergency_start == i:            
            traffic_light = round(random.uniform(1, 4))
            if traffic_light == 1:
                value = 0
                traffic_light_emergency = traffic_light_agent1
            elif traffic_light == 2:
                value = 1
                traffic_light_emergency = traffic_light_agent2
            elif traffic_light == 3:
                value = 2
                traffic_light_emergency = traffic_light_agent3
            elif traffic_light == 4:
                value = 3
                traffic_light_emergency = traffic_light_agent4
            emergency = EmergencyVehicle(start_position_cars[value], 0.5, traffic_light_emergency, "emergency@localhost", "password")
            await emergency.start()

        speed = round(random.uniform(0.4, 1.0), 1)
        vehicle_agent3 = Vehicle(start_position_cars[2], speed, traffic_light_agent3, "car@localhost", "password")
        await vehicle_agent3.start()
        road_agent1.add_vehicle(1, start_position_cars[2], speed, traffic_light_agent3, "admin@localhost", "password")

        speed = round(random.uniform(0.4, 1.0), 1)
        vehicle_agent4 = Vehicle(start_position_cars[3], speed, traffic_light_agent4, "car@localhost", "password")
        await vehicle_agent4.start()
        road_agent2.add_vehicle(1, start_position_cars[3], speed, traffic_light_agent4, "admin@localhost", "password")

        count_vehicles = count_vehicles + 4 # this will count the total vehicles, since we have 4 agents being created, we need +4
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
    
    # open the file and add the results
    f = open("result.txt", "a")
    f.write(f"\nTotal awaiting time for all {count_vehicles} vehicles = {awaiting_time_total:.2f} seconds\nMedium awaiting time for one vehicle = {(awaiting_time_total/count_vehicles):.2f} seconds \n")
    f.write(f"Emergency vehicle awaiting time: {emergency_vehicle_time:.2f}\n")
    f.write(f"Execution time: {(finish_time - start_time)/60:.2f} minutes\n")
    for i in range(4):
        f.write(f"Semaphore {i+1} medium and times (in seconds): {(sum(vehicles_times[i])/count_vehicles/4):.2f} {vehicles_times[i]}\n");
    f.write("\nNext Test\n")
    f.close()

    sys.exit()


if __name__ == "__main__":
    spade.run(main())
