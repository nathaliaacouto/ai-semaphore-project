import random
import spade
import asyncio
import sys
import time as t
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

GREEN_LIGHT = "Green"
YELLOW_LIGHT = "Yellow"
RED_LIGHT = "Red"
AWAITING_TIME_TOTAL = 0

position_lights = [1, 3, 5, 7]
start_position_cars = [0, 2, 4, 6]
awaiting_time_for_light = [0, 0, 0, 0]
vehicles_times = [[], [], [], []]
vehicles_lines = [[], [], [], []]


class TrafficLight(Agent):
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

    def __init__(self, color, time, position, number, jid: str, password: str, verify_security: bool = False, *args,
                 **kwargs):
        super().__init__(jid, password, verify_security)
        self.color = color
        self.time = time
        self.position = position
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
            for i in range(len(position_lights)):
                if self.agent.traffic_light.number == i:
                    position_light = position_lights[i - 1]

            if self.agent.position == self.agent.start_position:
                self.agent.creation_time = t.time()

            while self.agent.position <= position_light:
                self.agent.position += self.agent.speed
                await asyncio.sleep(0.5)

            if self.agent.position >= position_light:
                while True:
                    light_color = self.agent.traffic_light.get_color()

                    if light_color == "Green":
                        global AWAITING_TIME_TOTAL
                        total_stop_time = self.agent.waiting_time
                        for i in range(len(position_lights)):
                            if self.agent.traffic_light.number == i + 1:
                                vehicles_times[i].append(round(total_stop_time, 2))
                        AWAITING_TIME_TOTAL += total_stop_time
                        awaiting_time_for_light[(self.agent.traffic_light.number) - 1] += total_stop_time

                        print(
                            f"Green, going. The car was in the red light {self.agent.traffic_light.number} for {total_stop_time:.2f} seconds")

                        self.kill(exit_code=10)
                        break

                    elif light_color == "Red" and self.agent.waiting_time == 0:
                        self.agent.reached_light_time = t.time()

                    if light_color == "Red":
                        self.agent.waiting_time = t.time() - self.agent.reached_light_time
                        for i in range(len(position_lights)):
                            if self.agent.traffic_light.number == i:
                                vehicles_lines[i].append(1)

                    await asyncio.sleep(1)

    def __init__(self, start_position, speed, traffic_light, jid: str, password: str, verify_security: bool = False, *args,
                 **kwargs):
        super().__init__(jid, password, verify_security)
        self.waiting_time = 0
        self.traffic_light = traffic_light
        self.position = start_position
        self.start_position = start_position
        self.creation_time = 0
        self.reached_light_time = 0
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
            for i in range(len(position_lights)):
                if self.agent.traffic_light.number == i:
                    position_light = position_lights[i - 1]

            if self.agent.position == self.agent.start_position:
                self.agent.creation_time = t.time()

            while self.agent.position <= position_light:
                self.agent.position += self.agent.speed
                await asyncio.sleep(0.5)

            if self.agent.position >= position_light:
                while True:
                    light_color = self.agent.traffic_light.get_color()

                    if light_color == "Green":
                        global AWAITING_TIME_TOTAL
                        total_stop_time = self.agent.waiting_time
                        for i in range(len(position_lights)):
                            if self.agent.traffic_light.number == i + 1:
                                vehicles_times[i].append(round(total_stop_time, 2))
                        AWAITING_TIME_TOTAL += total_stop_time
                        awaiting_time_for_light[(self.agent.traffic_light.number) - 1] += total_stop_time

                        print(
                            f"Green, going. The emergency vehicle was in the red light {self.agent.traffic_light.number} for {total_stop_time:.2f} seconds")

                        self.kill(exit_code=10)
                        break

                    elif light_color == "Red" and self.agent.waiting_time == 0:
                        self.agent.reached_light_time = t.time()

                    if light_color == "Red":
                        self.agent.waiting_time = t.time() - self.agent.reached_light_time
                        for i in range(len(position_lights)):
                            if self.agent.traffic_light.number == i:
                                vehicles_lines[i].append(1)

                    await asyncio.sleep(1)

    def __init__(self, start_position, speed, traffic_light, jid: str, password: str, verify_security: bool = False, *args,
                 **kwargs):
        super().__init__(jid, password, verify_security)
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


class CentralCoordinationAgent(Agent):
    class CentralCoordinationBehav(CyclicBehaviour):
        async def run(self):
            for i in range(len(vehicles_lines)):
                if len(vehicles_lines[i]) > 10 and awaiting_time_for_light[i] > 30:
                    if self.agent.traffic_lights[i].number == 1:
                        self.agent.traffic_lights[1].central_change_color(RED_LIGHT)
                        self.agent.traffic_lights[3].central_change_color(RED_LIGHT)
                        await asyncio.sleep(2)
                        self.agent.traffic_lights[i].central_change_color(GREEN_LIGHT)
                        self.agent.traffic_lights[2].central_change_color(GREEN_LIGHT)

                    if self.agent.traffic_lights[i].number == 2:
                        self.agent.traffic_lights[0].central_change_color(RED_LIGHT)
                        self.agent.traffic_lights[2].central_change_color(RED_LIGHT)
                        await asyncio.sleep(2)
                        self.agent.traffic_lights[i].central_change_color(GREEN_LIGHT)
                        self.agent.traffic_lights[3].central_change_color(GREEN_LIGHT)

                    if self.agent.traffic_lights[i].number == 3:
                        self.agent.traffic_lights[1].central_change_color(RED_LIGHT)
                        self.agent.traffic_lights[3].central_change_color(RED_LIGHT)
                        await asyncio.sleep(2)
                        self.agent.traffic_lights[i].central_change_color(GREEN_LIGHT)
                        self.agent.traffic_lights[0].central_change_color(GREEN_LIGHT)

                    if self.agent.traffic_lights[i].number == 4:
                        self.agent.traffic_lights[0].central_change_color(RED_LIGHT)
                        self.agent.traffic_lights[2].central_change_color(RED_LIGHT)
                        await asyncio.sleep(2)
                        self.agent.traffic_lights[i].central_change_color(GREEN_LIGHT)
                        self.agent.traffic_lights[1].central_change_color(GREEN_LIGHT)

    def __init__(self, tf1, tf2, tf3, tf4, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.traffic_lights = [tf1, tf2, tf3, tf4]

    async def setup(self):
        await super().setup()
        behaviour = self.CentralCoordinationBehav()
        self.add_behaviour(behaviour)


async def main():
    start_time = t.time()
    light_time = 60
    traffic_light_agent1 = TrafficLight("Green", light_time, position_lights[0], 1, "admin@localhost", "password")
    await traffic_light_agent1.start()

    traffic_light_agent2 = TrafficLight("Red", light_time, position_lights[1], 2, "admin@localhost", "password")
    await traffic_light_agent2.start()

    traffic_light_agent3 = TrafficLight("Green", light_time, position_lights[2], 3, "admin@localhost", "password")
    await traffic_light_agent3.start()

    traffic_light_agent4 = TrafficLight("Red", light_time, position_lights[3], 4, "admin@localhost", "password")
    await traffic_light_agent4.start()

    central_agent = CentralCoordinationAgent(traffic_light_agent1, traffic_light_agent2, traffic_light_agent3,
                                            traffic_light_agent4, "admin@localhost", "password")
    await central_agent.start()

    road_agent1 = Road("2450", 2, "admin@localhost", "password")
    road_agent2 = Road("4763", 2, "admin@localhost", "password")

    count_vehicles = 0
    for i in range(25):
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
        vehicle_agent4 = EmergencyVehicle(start_position_cars[3], speed, traffic_light_agent4, "admin@localhost", "password")
        await vehicle_agent4.start()
        road_agent2.add_vehicle(1, start_position_cars[3], speed, traffic_light_agent4, "admin@localhost", "password")

        count_vehicles = count_vehicles + 4
        await asyncio.sleep(5)

    await asyncio.sleep(10)

    print("\n----- TOTAL -----")
    print(f"Total awaiting time for all {count_vehicles} vehicles = {AWAITING_TIME_TOTAL:.2f} seconds")
    print(f"Medium awaiting time for one vehicle = {(AWAITING_TIME_TOTAL/count_vehicles):.2f} seconds")

    for i in range(len(awaiting_time_for_light)):
        vehicles_in_one_light = count_vehicles / 4
        print(f"\n----- LIGHT {i+1} -----")
        print(f"Total awaiting time for light {i+1}: {awaiting_time_for_light[i]:.2f} seconds")
        print(f"Medium awaiting time one vehicle in light {i+1}: {(awaiting_time_for_light[i]/vehicles_in_one_light):.2f} seconds")
    
    print("\n----- EMERGENCY VEHICLE -----")
    emergency_vehicle_await_time = vehicles_times[-1][0]  # Assuming the last vehicle is the emergency vehicle
    print(f"Total awaiting time for emergency vehicle: {emergency_vehicle_await_time:.2f} seconds")

    finish_time = t.time();
    print(f"time: {(finish_time - start_time):.2f}")

    for i in range(4):
        print(vehicles_times[i]);

    sys.exit()


if __name__ == "__main__":
    spade.run(main())