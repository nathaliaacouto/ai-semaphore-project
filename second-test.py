import spade
import asyncio
import sys
import time as t
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

GREEN_LIGHT_NS = "Green_NS"
RED_LIGHT_NS = "Red_NS"
GREEN_LIGHT_WE = "Green_WE"
RED_LIGHT_WE = "Red_WE"
AWAITING_TIME_TOTAL_NS = 0
AWAITING_TIME_TOTAL_WE = 0

class TrafficLight(Agent):
    class TrafficLightBehav(CyclicBehaviour):
        async def run(self):
            while True:
                print(f"{self.agent.direction} - {self.agent.color}")
                await asyncio.sleep(24)  # green light on for 24 seconds
                self.agent.change_color()

                print(f"{self.agent.direction} - {self.agent.color}")
                await asyncio.sleep(5)  # yellow light on for 5 seconds
                self.agent.change_color()

                print(f"{self.agent.direction} - {self.agent.color}")
                await asyncio.sleep(30)  # red light on for 30 seconds
                self.agent.change_color()

                await asyncio.sleep(1)

    def __init__(self, direction, jid: str, password: str, verify_security: bool = False, *args, **kwargs):
        super().__init__(jid, password, verify_security)
        self.direction = direction
        self.color = GREEN_LIGHT_NS if direction == "North-South" else RED_LIGHT_WE

    def change_color(self):
        if self.direction == "North-South":
            if self.color == GREEN_LIGHT_NS:
                self.color = RED_LIGHT_NS
            elif self.color == RED_LIGHT_NS:
                self.color = GREEN_LIGHT_NS
        else:  # West-East
            if self.color == GREEN_LIGHT_WE:
                self.color = RED_LIGHT_WE
            elif self.color == RED_LIGHT_WE:
                self.color = GREEN_LIGHT_WE

    def get_color(self):
        return self.color

    async def setup(self):
        await super().setup()
        behaviour = self.TrafficLightBehav()
        self.add_behaviour(behaviour)


class Vehicle(Agent):
    class VehicleBehav(CyclicBehaviour):
        async def run(self):
            global AWAITING_TIME_TOTAL_NS, AWAITING_TIME_TOTAL_WE
            while True:
                if self.agent.direction == "North-South":
                    if self.agent.traffic_light.get_color() == GREEN_LIGHT_NS:
                        if self.agent.waiting_time is not None:
                            total_stop_time = t.time() - self.agent.waiting_time
                            AWAITING_TIME_TOTAL_NS += total_stop_time
                            print(
                                f"{self.agent.direction} - Green, going. The car was in the red light for {total_stop_time:.2f} seconds")
                        self.agent.waiting_time = None  # Reset waiting time
                        self.kill(exit_code=10)  # if it went ahead, it doesn't matter to this test anymore
                        break
                    elif self.agent.traffic_light.get_color() == RED_LIGHT_NS and self.agent.waiting_time is None:
                        self.agent.waiting_time = t.time()
                else:  # West-East
                    if self.agent.traffic_light.get_color() == GREEN_LIGHT_WE:
                        if self.agent.waiting_time is not None:
                            total_stop_time = t.time() - self.agent.waiting_time
                            AWAITING_TIME_TOTAL_WE += total_stop_time
                            print(
                                f"{self.agent.direction} - Green, going. The car was in the red light for {total_stop_time:.2f} seconds")
                        self.agent.waiting_time = None  # Reset waiting time
                        self.kill(exit_code=10)  # if it went ahead, it doesn't matter to this test anymore
                        break
                    elif self.agent.traffic_light.get_color() == RED_LIGHT_WE and self.agent.waiting_time is None:
                        self.agent.waiting_time = t.time()

                await asyncio.sleep(1)

    def __init__(self, direction, traffic_light, jid: str, password: str, verify_security: bool = False, *args,
                 **kwargs):
        super().__init__(jid, password, verify_security)
        self.direction = direction
        self.waiting_time = None
        self.traffic_light = traffic_light

    async def setup(self):
        await super().setup()
        behaviour = self.VehicleBehav()
        self.add_behaviour(behaviour)



async def main():
    light_time_ns = 60  # Time for North-South light cycle
    light_time_we = 45  # Time for West-East light cycle

    traffic_light_agent_ns = TrafficLight("North-South", "light_ns@localhost", "password")
    traffic_light_agent_we = TrafficLight("West-East", "light_we@localhost", "password")

    await traffic_light_agent_ns.start()
    await traffic_light_agent_we.start()

    await asyncio.sleep(20)

    vehicles_ns = []
    vehicles_we = []

    for i in range(10):
        await asyncio.sleep(random.uniform(1, 5))
        vehicle_agent_ns = Vehicle("North-South", traffic_light_agent_ns, f"car_ns_{i}@localhost", "password")
        await vehicle_agent_ns.start()
        vehicles_ns.append(vehicle_agent_ns)

        await asyncio.sleep(random.uniform(1, 5))
        vehicle_agent_we = Vehicle("West-East", traffic_light_agent_we, f"car_we_{i}@localhost", "password")
        await vehicle_agent_we.start()
        vehicles_we.append(vehicle_agent_we)

    await asyncio.gather(*[vehicle.stop() for vehicle in vehicles_ns + vehicles_we])

    print(f"Total awaiting time for all North-South cars = {AWAITING_TIME_TOTAL_NS:.2f} seconds")
    print(f"Medium awaiting time for one North-South car = {(AWAITING_TIME_TOTAL_NS / 10):.2f} seconds")

    print(f"Total awaiting time for all West-East cars = {AWAITING_TIME_TOTAL_WE:.2f} seconds")
    print(f"Medium awaiting time for one West-East car = {(AWAITING_TIME_TOTAL_WE / 10):.2f} seconds")

    sys.exit()


if __name__ == "__main__":
    spade.run(main())