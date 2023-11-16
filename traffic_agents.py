import spade
import asyncio
import time as t
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour

GREEN_LIGHT = "Green"
YELLOW_LIGHT = "Yellow"
RED_LIGHT = "Red"
REQUEST_GREEN_LIGHT = 1
EMERGENCY = False


class TrafficLight(Agent):
    # Behaviour
    class TrafficLightBehav(CyclicBehaviour):
        async def run(self):
            print(YELLOW_LIGHT)  # needs to be changes by the color
            await asyncio.sleep(5)

            print(RED_LIGHT)  # needs to be changes by the color
            await asyncio.sleep(5)

            print(GREEN_LIGHT)  # needs to be changes by the color
            await asyncio.sleep(5)

            self.kill(exit_code=10)
    # Behaviour

    def __init__(self, color, time, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.color = color
        self.time = time

    def change_color(self):
        # Open in emergency cases
        global EMERGENCY
        if EMERGENCY:
            self.color = GREEN_LIGHT
            # Change variable after
            EMERGENCY = False
            print(f"Priority for emergency vehicle granted, light {self.color}")
        # Other cases
        elif self.color == GREEN_LIGHT:
            self.color = YELLOW_LIGHT
        elif self.color == YELLOW_LIGHT:
            self.color = RED_LIGHT
        elif self.color == RED_LIGHT:
            self.color = GREEN_LIGHT

    def change_time(self, new_time):
        self.time = new_time

    async def setup(self):
        await super().setup()
        behaviour = self.TrafficLightBehav()
        self.add_behaviour(behaviour)


class Vehicle(Agent):
    # Behaviour
    class VehicleBehav(OneShotBehaviour):
        async def run(self):
            print("Vehicle")

    # Behaviour
    def __init__(self, position, time, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.position = position
        self.waiting_time = time

    def stop_on_light(self, color):
        if color == "Red":
            print("Stop, red light")

    def request_green_light(self):
        if self.waiting_time > 15:
            print("Waiting time is too long, requesting green light")
            return REQUEST_GREEN_LIGHT

    async def setup(self):
        await super().setup()
        behaviour = self.VehicleBehav()
        self.add_behaviour(behaviour)


class EmergencyVehicle(Agent):
    # Behaviour
    class EmergencyVehicleBehav(OneShotBehaviour):
        async def run(self):
            print("Requesting priority for emergency vehicle")

            emergency_condition = True
            if emergency_condition:
                print("Emergency vehicle requesting priority at intersections.")
                global EMERGENCY
                EMERGENCY = True

                # Additional logic to communicate with Traffic Light Agents
                print("Communicating with Traffic Light Agents: Granting priority for emergency vehicle.")
                traffic_light = TrafficLight("Green", 10, "admin@localhost", "password")
                TrafficLight.change_color(traffic_light)
    # Behaviour

    def __init__(self, name, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.vehicle_name = name

    async def setup(self):
        await super().setup()
        behaviour = self.EmergencyVehicleBehav()
        self.add_behaviour(behaviour)


class RoadSign(Agent):
    # Behaviour
    class RoadSignBehav(OneShotBehaviour):
        async def run(self):
            print("Road Sign")
    # Behaviour

    def __init__(self, sign_type, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.sign_type = sign_type

    async def setup(self):
        await super().setup()
        behaviour = self.RoadSignBehav()
        self.add_behaviour(behaviour)


class Lane(Agent):
    # Behaviour
    class LaneBehav(OneShotBehaviour):
        async def run(self):
            print("Lane")

    # Behaviour

    def __init__(self, lane_id, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.lane_id = lane_id
        self.vehicles = []

    def add_vehicle(self, waiting_time, position):
        vehicle = Vehicle(waiting_time, position, self.jid, self.password)
        self.vehicles.append(vehicle)

    async def setup(self):
        await super().setup()
        behaviour = self.LaneBehav()
        self.add_behaviour(behaviour)


class Road(Agent):
    # Behaviour
    class RoadBehav(OneShotBehaviour):
        async def run(self):
            print("Road")

    # Behaviour

    def __init__(self, name, num_lanes, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.road_name = name
        self.lanes = [Lane(i, jid, password) for i in range(num_lanes)]

    async def setup(self):
        await super().setup()
        behaviour = self.RoadBehav()
        self.add_behaviour(behaviour)


class Intersection(Agent):
    # Behaviour
    class IntersectionBehav(CyclicBehaviour):
        async def run(self):
            print("Intersection")
            # current_time = str(t.time() - start_time)
            # current_time = int(current_time[0])
            # if current_time > self.traffic_light.time:
            #    self.traffic_light.change_color()

            # if self.traffic_light.color == GREEN_LIGHT:
            #     self.road_sign.sign_type = "Go"
            # elif self.traffic_light.color == YELLOW_LIGHT:
            #    self.road_sign.sign_type = "Yield"
            # elif self.traffic_light.color == RED_LIGHT:
            #    self.road_sign.sign_type = "Stop"
    # Behaviour

    def __init__(self, name, traffic_light_color, traffic_light_time, road_sign_type, lanes_road, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.intersection_name = name
        self.traffic_light = TrafficLight(traffic_light_color, traffic_light_time, jid, password)
        self.road_sign = RoadSign(road_sign_type, jid, password)
        # Additional attributes
        self.road = Road(f"{name}_Road", lanes_road, jid, password)

    async def setup(self):
        await super().setup()
        behaviour = self.IntersectionBehav()
        self.add_behaviour(behaviour)


class CentralCoordinationAgent(Agent):
    # Behaviour
    class CentralCoordinationBehav(CyclicBehaviour):
        async def run(self):
            print("Optimizing traffic flow")

            # Example: Adjust traffic light timings based on traffic conditions
            # for intersection in self.intersections:
            #    if intersection.traffic_light.color == GREEN_LIGHT:
            #        intersection.traffic_light.change_time(intersection.traffic_light.time - 1)
            #    elif intersection.traffic_light.color == RED_LIGHT:
            #        intersection.traffic_light.change_time(intersection.traffic_light.time + 1)

            # Additional logic to communicate with other agents (e.g., Vehicle Agents)
            #    for lane in intersection.road.lanes:
            #        for vehicle in lane.vehicles:
            #            if vehicle.waiting_time > 20:
            #                print(f"Communicating with Vehicle at Lane {lane.lane_id}: "
            #                      f"Adjusting waiting time for better flow.")

    # Behaviour

    def __init__(self, intersections, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.intersections = intersections

    async def setup(self):
        await super().setup()
        behaviour = self.CentralCoordinationBehav()
        self.add_behaviour(behaviour)


class DisruptionManagement(Agent):
    # Behaviour
    class DisruptionManagementBehav(CyclicBehaviour):
        async def run(self):
            print("Predicting disruptions")
            # Example: Placeholder logic for disruption prediction using a machine learning model
            disruption_probability = 0.2  # Placeholder probability
            if disruption_probability > 0.5:
                print("Disruption predicted! Alerting relevant agents.")

                # Additional logic to communicate with other agents (e.g., Traffic Light Agents)
                print("Communicating with Traffic Light Agents: Adjusting timings for predicted disruption.")
    # Behaviour

    def __init__(self, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)

    async def setup(self):
        await super().setup()
        behaviour = self.DisruptionManagementBehav()
        self.add_behaviour(behaviour)


class Environment:
    def __init__(self):
        road_1 = Road("Road_1", 2, "admin@localhost", "password")  # 2 lanes
        road_2 = Road("Road_2", 3, "admin@localhost", "password")  # 3 lanes

        intersection_1 = Intersection("Intersection_1", "Red", 5, "Stop", 2, "admin@localhost", "password")
        intersection_2 = Intersection("Intersection_2", "Green", 5, "Yield",  3, "admin@localhost", "password")

        self.roads = [road_1, road_2]
        self.intersections = [intersection_1, intersection_2]

        # Additional agents
        self.central_agent = CentralCoordinationAgent(self.intersections, "admin@localhost", "password")
        self.disruption_agent = DisruptionManagement("admin@localhost", "password")
        self.emergency_agent = EmergencyVehicle("Ambulance", "admin@localhost", "password")

        # Populate lanes with vehicles for testing
        road_1.lanes[0].add_vehicle(10, "Position_A")
        road_2.lanes[1].add_vehicle(25, "Position_B")

    def add_road(self, road):
        self.roads.append(road)

    def add_intersection(self, intersection):
        self.intersections.append(intersection)

    async def display(self):
        traffic_light = TrafficLight(GREEN_LIGHT, 10, "admin@localhost", "password")
        await traffic_light.start(auto_register=True)
        start_time = t.time()
        for road in self.roads:
            print(f"{road.name}: ", end='')
            for lane in road.lanes:
                print(f" Lane {lane.lane_id}", end='')
                if lane.vehicles:
                    print(" [Vehicles: ", end='')
                    for vehicle in lane.vehicles:
                        print(f"(Waiting Time: {vehicle.waiting_time}, Position: {vehicle.position}) ", end='')
                    print("]", end='')
            print()

        print("Intersections: ")
        for intersection in self.intersections:
            print(
                f"{intersection.name} - Traffic Light: {intersection.traffic_light.color}, "
                f"Time: {intersection.traffic_light.time} "
                f"- Road Sign: {intersection.road_sign.sign_type}")


async def main():
    agent1 = TrafficLight("Red", 10, "admin@localhost", "password")
    await agent1.start(auto_register=True)


if __name__ == "__main__":
    spade.run(main())
