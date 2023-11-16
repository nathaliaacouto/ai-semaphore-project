# Traffic Management System Technical Documentation

## Overview

The provided Python code implements a Traffic Management System, introducing additional features such as traffic flow optimization, disruption prediction, and handling emergency vehicles. This documentation aims to provide an in-depth understanding of each component and functionality within the system.

## TrafficLight Agent

The `TrafficLight` Agent encapsulates the behavior of a traffic light. It maintains two crucial properties:

- `color`: Represents the current state of the traffic light (Green, Yellow, Red).
- `time`: Denotes the duration of each traffic light state.

The `change_color` method allows the traffic light to transition between states, adhering to the typical sequence of Green -> Yellow -> Red. The `change_time` method enables dynamic adjustment of the time duration for each state.

The behavior of this agent consists of printing on the screen the color of the light. In the future, this should be changed to use the variables and method implementation.

## Vehicle Agent

The `Vehicle` Agent represents vehicles within the system. Key properties include:

- `waiting_time`: Tracks the time a vehicle spends waiting at a red light.
- `position`: Specifies the current position of the vehicle.

The Agent provides methods such as `stop` to notify the vehicle about a red light and `request_green_light` to initiate a green light request if the waiting time surpasses a predefined threshold.

The behavior is still not defined but it should call both methods that are in the Agent.

## EmergencyVehicleAgent Agent

The `EmergencyVehicleAgent` Agent manages emergency vehicles. Key properties include:

- `vehicle_name`: Specifies the Emergency Vehicle name (Ex.: Ambulance).

The behavior of this agent consists of requesting priority if there is an emergency condition.

## RoadSign Agent

The `RoadSign` Agent defines the characteristics of road signs. It primarily features:

- `sign_type`: Indicates the type of road sign associated with an intersection.

The behavior is still not defined.

## Lane Agent

The `Lane` Agent represents individual lanes within a road. It comprises:

- `lane_id`: Identifies the lane.
- `vehicles`: A list to store vehicle instances within the lane.

The `add_vehicle` method facilitates the addition of new vehicles to the lane.

The behavior is still not defined.

## Road Agent

The `Road` Agent models a road within the system. It includes:

- `name`: A label for the road.
- `lanes`: A list of lanes associated with the road.

The behavior is still not defined.

## Intersection Agent

The `Intersection` Agent models traffic intersections. Its properties consist of:

- `intersection_name`: A unique identifier for the intersection.
- `traffic_light`: An instance of the `TrafficLight` Agent.
- `road_sign`: An instance of the `RoadSign` Agent.
- `road`: An instance of the `Road` Agent, representing a road associated with the intersection.

The behavior is still not defined, but it should adjust the road sign based on the traffic light color and determine if the traffic light should change according to time.

## CentralCoordinationAgent Agent

The `CentralCoordinationAgent` Agent serves as a coordinator for optimizing traffic flow. Key attributes include:

- `intersections`: A list of intersections to be coordinated.

The behavior is still not defined, but it should implement logic to adjust traffic light timings based on traffic conditions. It iterates over intersections, modifying timings, and communicates with other agents for improved traffic flow

## DisruptionManagement Agent

The `DisruptionManagement` Agent handles disruption prediction.

The behavior is still not defined, but it should implement logic for disruption prediction. If disruption probability exceeds a threshold, it alerts relevant agents and adjusts traffic light timings.

## Environment Class

The `Environment` Class orchestrates the overall system. Key properties include:

- `roads`: A list of roads within the environment.
- `intersections`: A list of intersections within the environment.
- `central_agent`: An instance of the `CentralCoordinationAgent` Agent.
- `disruption_agent`: An instance of the `DisruptionManagementAgent` Agent.
- `emergency_agent`: An instance of the `EmergencyVehicleAgent` Agent.

The Class includes methods like `add_road` and `add_intersection` for extending the environment. The `display` method showcases information about roads, lanes, and intersections, and invokes additional functionalities.

## Properties that are the same for all Agents
The setup class there in all Agents is to initialize them and add the behaviour, and all behaviours have the name of the Agent + "Behav"

The 'jid' and 'password' all Agents have in their init are for the system and should be the email and password.

## Conclusion

This Traffic Management System provides a modular and extensible framework for handling various aspects of traffic control, disruption prediction, and emergency scenarios. It includes well-defined Agents with encapsulated functionalities, promoting maintainability and scalability. The placeholder logic enables further customization based on specific use cases.
