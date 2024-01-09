import random
import pygame
import spade
import asyncio
import sys
import time as t
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

pygame.init()

# Window settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Traffic Movement Simulator')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

GREEN_LIGHT = GREEN
YELLOW_LIGHT = YELLOW
RED_LIGHT = RED

AWAITING_TIME_TOTAL = 0

offset = 70

traffic_lights_positions = [
    (width // 2 - offset, height // 2 - offset),  # Upper left traffic light
    (width // 2 + offset, height // 2 - offset),  # Upper right traffic light
    (width // 2 - offset, height // 2 + offset),  # Lower left traffic light
    (width // 2 + offset, height // 2 + offset)   # Lower right traffic light
]

start_position_cars = [0, 2, 4, 6]
awaiting_time_for_light = [0, 0, 0, 0]
vehicles_times = [[], [], [], []]
vehicles_lines = [[], [], [], []]
all_vehicles = []
SAFE_DISTANCE = 20
ADMIN_JID = "admin@localhost"
ADMIN_PASSWORD = "password"


class TrafficLight(Agent):
    class TrafficLightBehav(CyclicBehaviour):
        async def run(self):
            if t.time() >= self.agent.next_change:
                print(f"Light is changing {self.agent.jid}")
                self.agent.change_light()

            await asyncio.sleep(1)

        def on_start(self):
            self.agent.setup_light()

    def __init__(self, color, position, number, jid, password, *args, **kwargs):
        super().__init__(jid, password, *args, **kwargs)
        self.color = color
        self.position = position
        self.number = number
        self.light_duration = {GREEN_LIGHT: 22, YELLOW_LIGHT: 5, RED_LIGHT: 30}
        self.next_change = t.time() + self.light_duration[self.color]

    def setup_light(self):
        # Initialize the light
        self.next_change = t.time() + self.light_duration[self.color]

    def change_light(self):
        if self.color == GREEN_LIGHT:
            self.color = YELLOW_LIGHT
        elif self.color == YELLOW_LIGHT:
            self.color = RED_LIGHT
        elif self.color == RED_LIGHT:
            self.color = GREEN_LIGHT
        print(f"Light changed to: {self.color}")
        self.next_change = t.time() + self.light_duration[self.color]

    def draw(self):
        color = (GREEN_LIGHT if self.color == GREEN_LIGHT else RED_LIGHT if self.color == RED_LIGHT else YELLOW_LIGHT)
        pygame.draw.circle(screen, color, self.position, 20)


class Lane:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)


class Road(Agent):
    def __init__(self, name, position, size, num_lanes, traffic_light, jid: str, password: str,
                 verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.road_name = name
        self.lanes = [Lane(i) for i in range(num_lanes)]
        self.num_lanes = num_lanes
        self.position = position
        self.size = size
        self.traffic_light = traffic_light

    def add_vehicle(self, num_lane, vehicle):
        self.lanes[num_lane].add_vehicle(vehicle)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.position + self.size)


class CentralCoordinationAgent(Agent):
    class CentralCoordinationBehav(CyclicBehaviour):
        async def run(self):
            for i, light in enumerate(self.agent.traffic_lights):
                if len(vehicles_lines[i]) > 10 and awaiting_time_for_light[i] > 30:
                    print(f"Changing traffic light logic for {i}")  # Add this line
                    await self.adjust_traffic_lights(i)
                    # Reset conditions after changing the light
                    vehicles_lines[i] = []
                    awaiting_time_for_light[i] = 0
            await asyncio.sleep(1)

        async def adjust_traffic_lights(self, light_number):
            # Changing the state of the lights
            for i, light in enumerate(self.agent.traffic_lights):
                if i == light_number:
                    # Set the chosen light to green
                    light.central_change_color(GREEN_LIGHT)
                else:
                    # Set other lights to red
                    light.central_change_color(RED_LIGHT)
            await asyncio.sleep(2)  # Wait 2 seconds for safety

    def __init__(self, traffic_lights, jid, password, *args, **kwargs):
        super().__init__(jid, password, *args, **kwargs)
        self.traffic_lights = traffic_lights

    async def setup(self):
        central_coordination_behaviour = self.CentralCoordinationBehav()
        self.add_behaviour(central_coordination_behaviour)


class Vehicle(Agent):

    class VehicleBehaviour(CyclicBehaviour):
        async def run(self):
            if self.agent.should_move():
                self.agent.move()
            await asyncio.sleep(0.1)
    def __init__(self, road_name, lane, x, y, speed, direction, traffic_light, jid, password):
        super().__init__(jid, password)
        self.road_name = road_name
        self.lane = lane
        self.x = x
        self.y = y
        self.width = 20
        self.height = 10
        self.speed = speed
        self.original_speed = speed  # Stores the original speed for resuming movement
        self.direction = direction
        self.traffic_light = traffic_light
        self.color = (0, 0, 255)  # Blue color of the vehicle

    async def setup(self):
        self.add_behaviour(self.VehicleBehaviour())

    def should_move(self):
        distance_to_light = self.calculate_distance_to_light()
        # Stop if the light is red and you're close
        if self.traffic_light.color == RED_LIGHT and distance_to_light < SAFE_DISTANCE:
            return False
        return True
    def move(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

    def calculate_distance_to_light(self):
        # Calculate distance depending on the direction of movement
        if self.direction == "right":
            return self.traffic_light.position[0] - self.x
        elif self.direction == "left":
            return self.x - self.traffic_light.position[0]
        elif self.direction == "up":
            return self.y - self.traffic_light.position[1]
        elif self.direction == "down":
            return self.traffic_light.position[1] - self.y

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def stop(self):
        self.speed = 0

    def start_moving(self):
        self.speed = self.original_speed


async def generate_vehicles(traffic_lights, number_of_vehicles):
    for _ in range(number_of_vehicles):
        x, y, direction, traffic_light = random_vehicle_position_and_direction(traffic_lights)
        road_name = ""
        random_speed = random.uniform(0.8, 1.0)
        vehicle = Vehicle(road_name, start_position_cars[0], x, y, random_speed, direction, traffic_light, ADMIN_JID,
                          ADMIN_PASSWORD)
        await vehicle.start()
        all_vehicles.append(vehicle)

        # Random time interval from 1 to 5 seconds
        random_interval = random.randint(1, 3)
        await asyncio.sleep(random_interval)


def random_vehicle_position_and_direction(traffic_lights):
    if random.choice([True, False]):
        # Set vehicles horizontally
        x = random.choice([0, width])
        y = height // 2
        direction = "right" if x == 0 else "left"
        traffic_light = traffic_lights[2] if direction == "right" else traffic_lights[1]
    else:
        # Set vehicles vertically
        x = width // 2
        y = random.choice([0, height])
        direction = "down" if y == 0 else "up"
        traffic_light = traffic_lights[0] if direction == "down" else traffic_lights[3]
    return x, y, direction, traffic_light


async def main():
    # Road settings
    ROAD_WIDTH = 100
    ROAD_HEIGHT = height

    # Creating traffic lights
    traffic_lights = [
        TrafficLight(GREEN_LIGHT, traffic_lights_positions[0], 1, ADMIN_JID, ADMIN_PASSWORD),
        TrafficLight(RED_LIGHT, traffic_lights_positions[1], 3, ADMIN_JID, ADMIN_PASSWORD),
        TrafficLight(RED_LIGHT, traffic_lights_positions[2], 5, ADMIN_JID, ADMIN_PASSWORD),
        TrafficLight(GREEN_LIGHT, traffic_lights_positions[3], 7, ADMIN_JID, ADMIN_PASSWORD),
    ]

    for light in traffic_lights:
        await light.start()

    # Creating central coordination agent
    central_agent = CentralCoordinationAgent(traffic_lights, ADMIN_JID, ADMIN_PASSWORD)
    await central_agent.start()

    # Creating roads
    roads = [
        Road("2450", (width // 2 - ROAD_WIDTH // 2, 0), (ROAD_WIDTH, ROAD_HEIGHT), 2, traffic_lights[0], ADMIN_JID,
             ADMIN_PASSWORD),
        Road("4763", (0, height // 2 - ROAD_WIDTH // 2), (width, ROAD_WIDTH), 2, traffic_lights[2], ADMIN_JID,
             ADMIN_PASSWORD),
    ]

    asyncio.create_task(generate_vehicles(traffic_lights, 10))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        current_time = t.time()
        for light in traffic_lights:
            if current_time >= light.next_change:
                light.change_light()

        screen.fill(BLACK)
        for light in traffic_lights:
            light.draw()
        for road in roads:
            road.draw()
        for vehicle in all_vehicles:
            vehicle.draw()
            vehicle.move()

        pygame.display.flip()
        await asyncio.sleep(0.01)

    for light in traffic_lights:
        await light.stop()
    await central_agent.stop()
    pygame.quit()


if __name__ == "__main__":
    spade.run(main())
