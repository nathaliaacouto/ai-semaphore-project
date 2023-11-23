import unittest
import spade
from unittest import mock
import sys
import time as t
from spade.agent import Agent
from traffic_agents import EmergencyVehicle, GREEN_LIGHT

class TestEmergencyVehicle(unittest.TestCase):
    def test_emergency_condition(self):
        emergency_vehicle = EmergencyVehicle("Ambulance", "admin@localhost", "password")

        with unittest.mock.patch('builtins.print') as mock_print:
            emergency_vehicle.setup()
            emergency_vehicle.EmergencyVehicleBehav().run()

            # Ensure that the global EMERGENCY variable is set to True
            self.assertTrue(emergency_vehicle.EMERGENCY)

            # Ensure that the traffic light color is changed to GREEN_LIGHT
            self.assertEqual(emergency_vehicle.traffic_light.color, GREEN_LIGHT)

            # Ensure that the communication message is printed
            mock_print.assert_any_call("Priority for emergency vehicle granted, light Green")

if __name__ == '__main__':
    unittest.main()
