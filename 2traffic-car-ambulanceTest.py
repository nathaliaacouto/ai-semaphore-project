#The test checks the initial state, it has 2 traffic ligths,  simulates the passage of time some cars, introduces an emergency vehicle, and verifies the resulting state.
import unittest
import asyncio
import spade

from traffic_agents import Environment, GREEN_LIGHT, RED_LIGHT, YELLOW_LIGHT, REQUEST_GREEN_LIGHT

class Test2TrafficSimulation(unittest.TestCase):
    def test_advanced_traffic_simulation(self):
        test_environment = Environment()

        asyncio.run(test_environment.display())

        for intersection in test_environment.intersections:
            self.assertEqual(intersection.traffic_light.color, RED_LIGHT)

        for _ in range(3):  # Simulate 3 cycles (Red -> Green -> Yellow)
            asyncio.run(test_environment.central_agent.CentralCoordinationBehav().run())

        # Check the state after the simulation
        for intersection in test_environment.intersections:
            self.assertEqual(intersection.traffic_light.color, GREEN_LIGHT)

        # Simulate the presence of an emergency vehicle (ambulance)
        ambulance_behavior = test_environment.emergency_agent.EmergencyVehicleBehav()
        asyncio.run(ambulance_behavior.run())

        # Get the waiting time of the ambulance
        ambulance_waiting_time = test_environment.emergency_agent.waiting_time

        print(f"Ambulance Output: Priority granted. Waiting Time: {ambulance_waiting_time} seconds")

        # Check the state after the emergency vehicle
        for intersection in test_environment.intersections:
            self.assertEqual(intersection.traffic_light.color, GREEN_LIGHT)
            self.assertTrue(test_environment.emergency_agent.EMERGENCY)

        # Simulate the passage of time to change the traffic light
        asyncio.run(test_environment.central_agent.CentralCoordinationBehav().run())

        # Check the state after the emergency vehicle has passed
        for intersection in test_environment.intersections:
            self.assertEqual(intersection.traffic_light.color, YELLOW_LIGHT)

        # Add more vehicles to lanes
        for _ in range(5):
            test_environment.roads[0].lanes[1].add_vehicle(20, "Position_C")
            test_environment.roads[1].lanes[0].add_vehicle(12, "Position_D")

        # Simulate the waiting time
        for _ in range(2):  # Simulate 2 cycles (Yellow -> Red)
            asyncio.run(test_environment.central_agent.CentralCoordinationBehav().run())

        
        total_waiting_time = sum(vehicle.waiting_time for road in test_environment.roads for lane in road.lanes for vehicle in lane.vehicles)
        print("Total Waiting Time for All Cars:", total_waiting_time)

        # Check the state after the waiting time for cars
        for intersection in test_environment.intersections:
            self.assertEqual(intersection.traffic_light.color, RED_LIGHT)

            # Check if cars request green light
            for lane in intersection.road.lanes:
                for vehicle in lane.vehicles:
                    print(f"Waiting Time for {vehicle.position}: {vehicle.waiting_time}")

                    if vehicle.waiting_time > 15:
                        self.assertEqual(vehicle.request_green_light(), REQUEST_GREEN_LIGHT)

if __name__ == '__main__':
    unittest.main()
