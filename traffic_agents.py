import time as t

GREEN_LIGHT_REQUEST = 1

class TrafficLight:
    def __init__(self, color, time):
        self.color = color
        self.time = time

    def change_color(self, new_color):
        self.color = new_color

    def change_time(self, new_time):
        self.time = new_time

class Vehicle:
    def __init__(self, waiting_time, position):
        self.waiting_time = waiting_time
        self.position = position

    def stop(self, color):
        if color == "Red":
            print("Stop, red light")

    def request_green_light(self):
        if self.waiting_time > 15:
            print("Waiting time is too long, requesting green light")
            return GREEN_LIGHT_REQUEST

class RoadSign:
    def __init__(self, sign_type):
        self.sign_type = sign_type


class Lane:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.vehicles = []

    def add_vehicle(self, waiting_time, position):
        vehicle = Vehicle(waiting_time, position)
        self.vehicles.append(vehicle)


class Road:
    def __init__(self, name, num_lanes):
        self.name = name
        self.lanes = [Lane(i) for i in range(num_lanes)]


class Intersection:
    def __init__(self, name, traffic_light_color, traffic_light_time, road_sign_type):
        self.name = name
        self.traffic_light = TrafficLight(traffic_light_color, traffic_light_time)
        self.road_sign = RoadSign(road_sign_type)


class Environment:
    def __init__(self):
        road_1 = Road("Road_1", 2)  # 2 lanes
        road_2 = Road("Road_2", 3)  # 3 lanes

        intersection_1 = Intersection("Intersection_1", "Red", 1, "Stop")
        intersection_2 = Intersection("Intersection_2", "Green", 20, "Yield")

        # data structures to keep the data related to the environment
        self.roads = [road_1, road_2]
        self.intersections = [intersection_1, intersection_2]

    def add_road(self, road):
        self.roads.append(road)

    def add_intersection(self, intersection):
        self.intersections.append(intersection)

    def change_traffic_light(self):
        for intersection in self.intersections:
            if t.time() > intersection.traffic_light.time:
                intersection.traffic_light.change_color("Green")

    def display(self):
        for road in self.roads:
            print(f"{road.name}: ", end='')
            for lane in road.lanes:
                print(f" Lane {lane.lane_id}", end='')
            print()

        print("Intersections: ")
        for intersection in self.intersections:
            print(
                f"{intersection.name} - Traffic Light: {intersection.traffic_light.color}, Time: {intersection.traffic_light.time} "
                f"- Road Sign: {intersection.road_sign.sign_type}")


if __name__ == "__main__":
    env = Environment()
    env.display()
    print(t.time())
