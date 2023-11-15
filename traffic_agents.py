import time as t
import random

GREEN_LIGHT_REQUEST = 1
GREEN_LIGHT = "Green"
YELLOW_LIGHT = "Yellow"
RED_LIGHT = "Red"

class TrafficLight:
    def __init__(self, color, time):
        self.color = color
        self.time = time

    def change_color(self):
        if self.color == GREEN_LIGHT:
            self.color = YELLOW_LIGHT
        elif self.color == YELLOW_LIGHT:
            self.color = RED_LIGHT
        elif self.color == RED_LIGHT:
            self.color = GREEN_LIGHT

    def change_time(self, new_time):
        self.time = new_time


class Vehicle:
    def __init__(self, waiting_time, position, weather_condition):
        self.waiting_time = waiting_time
        self.position = position
        self.weather_condition = weather_condition

    def stop(self, color):
        if color == "Red":
            print("Stop, red light")
        if self.weather_condition == "Rainy":
            print("Weather is rainy. Adjusting speed due to safety concerns.")
                # Additional logic for adjusting speed in rainy conditions

    def request_green_light(self):
        if self.waiting_time > 15:
            print("Waiting time is too long, requesting green light")
            return GREEN_LIGHT_REQUEST

    def adjust_speed_based_on_weather(self):
        if self.weather_condition == "Rainy":
            print("Adjusting speed due to rainy weather.")
            slowing_factor = random.uniform(0.7, 1.0)
        elif self.weather_condition == "Snowy":
            print("Adjusting speed due to snowy weather.")
            slowing_factor = random.uniform(0.5, 0.8)
        elif self.weather_condition == "Foggy":
            print("Adjusting speed due to foggy weather.")
            slowing_factor = random.uniform(0.6, 0.9)
        else:
            slowing_factor = 1.0  # No adjustment for other conditions

        self.waiting_time = int(self.waiting_time * slowing_factor)


class RoadSign:
    def __init__(self, sign_type):
        self.sign_type = sign_type


class Lane:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.vehicles = []

    def add_vehicle(self, waiting_time, position, weather_condition):
        vehicle = Vehicle(waiting_time, position, weather_condition)
        self.vehicles.append(vehicle)


class Road:
    def __init__(self, name, num_lanes):
        self.name = name
        self.lanes = [Lane(i) for i in range(num_lanes)]

class WeatherCondition:
    def __init__(self, condition):
        self.condition = condition


class Intersection:
    #Adds a new attribute road to the Intersection class, representing a road associated with each intersection.The road is initialized as an instance of the Road class with two lanes.

    def __init__(self, name, traffic_light_color, traffic_light_time, road_sign_type,weather_condition):
        self.name = name
        self.traffic_light = TrafficLight(traffic_light_color, traffic_light_time)
        self.road_sign = RoadSign(road_sign_type)
        self.weather_condition = WeatherCondition(weather_condition)

        # Additional attributes
        self.road = Road(f"{name}_Road", 2)  # Each intersection has a two-lane road

    def change_road_sign(self):
        if self.traffic_light.color == GREEN_LIGHT:
            self.road_sign.sign_type = "Go"
        elif self.traffic_light.color == YELLOW_LIGHT:
            self.road_sign.sign_type = "Yield"
        elif self.traffic_light.color == RED_LIGHT:
            self.road_sign.sign_type = "Stop"

    def check_change_with_time(self, start_time):
        current_time = str(t.time() - start_time)
        current_time = int(current_time[0])
        if current_time > self.traffic_light.time:
            self.traffic_light.change_color()


class CentralCoordinationAgent:
   #Introduces the CentralCoordinationAgent class responsible for coordinating and optimizing traffic flow.
    #The optimize_traffic_flow method performs the following actions:
        #Adjusts traffic light timings based on traffic conditions.
        #Communicates with other agents, such as Vehicle Agents, to improve traffic flow.

    def __init__(self, intersections):
        self.intersections = intersections

    def optimize_traffic_flow(self):
        # Additional logic to optimize traffic flow
        print("Optimizing traffic flow")

        # Example: Adjust traffic light timings based on traffic conditions
        for intersection in self.intersections:
            if intersection.traffic_light.color == GREEN_LIGHT:
                intersection.traffic_light.change_time(intersection.traffic_light.time - 1)
            elif intersection.traffic_light.color == RED_LIGHT:
                intersection.traffic_light.change_time(intersection.traffic_light.time + 1)

            # Additional logic to communicate with other agents (e.g., Vehicle Agents)
            for lane in intersection.road.lanes:
                for vehicle in lane.vehicles:
                    if vehicle.waiting_time > 20:
                        print(f"Communicating with Vehicle at Lane {lane.lane_id}: "
                              f"Adjusting waiting time for better flow.")


class DisruptionManagementAgent:
    #Introduces the DisruptionManagementAgent class to handle disruption prediction and management.
    #The predict_disruptions method performs the following actions:
        #Placeholder for disruption prediction logic using a machine learning model.
        #If the disruption probability is greater than 0.5, alerts relevant agents and adjusts traffic light timings.


    def __init__(self):
        # Additional initialization for disruption management
        print("Disruption Management Agent initialized")

    def predict_disruptions(self):
        # Additional logic to predict disruptions
        print("Predicting disruptions")

        # Example: Placeholder logic for disruption prediction using a machine learning model
        disruption_probability = 0.2  # Placeholder probability
        if disruption_probability > 0.5:
            print("Disruption predicted! Alerting relevant agents.")

            # Additional logic to communicate with other agents (e.g., Traffic Light Agents)
            print("Communicating with Traffic Light Agents: Adjusting timings for predicted disruption.")


class EmergencyVehicleAgent:

    #Introduces the EmergencyVehicleAgent class to handle emergency vehicles.
    #The request_priority method performs the following actions:
        #Placeholder for logic to request priority based on emergency conditions.
        #If there is an emergency condition, requests priority and communicates with traffic lights to obtain it.
    def __init__(self):
        # Additional initialization for emergency vehicle agent
        print("Emergency Vehicle Agent initialized")

    def request_priority(self):
        # Additional logic for emergency vehicle priority
        print("Requesting priority for emergency vehicle")

        # Example: Placeholder logic to request priority based on emergency conditions
        emergency_condition = True  # Placeholder for emergency condition
        if emergency_condition:
            print("Emergency vehicle requesting priority at intersections.")

            # Additional logic to communicate with Traffic Light Agents
            print("Communicating with Traffic Light Agents: Granting priority for emergency vehicle.")


# Extend the Environment class to include the new agents
class Environment:
    WEATHER_CONDITIONS = ["Clear", "Rainy", "Snowy", "Foggy"]
    def __init__(self):
        road_1 = Road("Road_1", 2)  # 2 lanes
        road_2 = Road("Road_2", 3)  # 3 lanes

        intersection_1 = Intersection("Intersection_1", "Red", 5, "Stop", self.get_random_weather())
        intersection_2 = Intersection("Intersection_2", "Green", 5, "Yield", self.get_random_weather())

        # data structures to keep the data related to the environment
        self.roads = [road_1, road_2]
        self.intersections = [intersection_1, intersection_2]

        # Additional agents
        self.central_agent = CentralCoordinationAgent(self.intersections)
        self.disruption_agent = DisruptionManagementAgent()
        self.emergency_agent = EmergencyVehicleAgent()

        # Populate lanes with vehicles for testing
        road_1.lanes[0].add_vehicle(10, "Position_A","Rainy")
        road_2.lanes[1].add_vehicle(25, "Position_B","Rainy")

    def adjust_speeds_based_on_weather(self):
        for intersection in self.intersections:
            for lane in intersection.road.lanes:
                for vehicle in lane.vehicles:
                    vehicle.adjust_speed_based_on_weather()
    def get_random_weather(self):
        return random.choice(self.WEATHER_CONDITIONS)
    def add_road(self, road):
        self.roads.append(road)

    def add_intersection(self, intersection):
        self.intersections.append(intersection)

    def display(self):
        #Extends the display method to include additional functionalities:
            #Calls the optimize_traffic_flow method of the CentralCoordinationAgent.
            #Calls the predict_disruptions method of the DisruptionManagementAgent.
            #Calls the request_priority method of the EmergencyVehicleAgent.
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
            intersection.check_change_with_time(start_time)
            print(
                f"{intersection.name} - Traffic Light: {intersection.traffic_light.color}, "
                f"Time: {intersection.traffic_light.time} "
                f"- Road Sign: {intersection.road_sign.sign_type}")

        # Additional functionalities
        self.central_agent.optimize_traffic_flow()
        self.disruption_agent.predict_disruptions()
        self.emergency_agent.request_priority()
        self.adjust_speeds_based_on_weather()


if __name__ == "__main__":
    env = Environment()
    env.display()
