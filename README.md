
# Traffic Management System 

## Introduction

This document provides an overview and explanation of the Traffic Management System, a simulation of traffic flow at intersections. The system incorporates various agents, including traffic lights, vehicles, and central coordination to optimize traffic flow, predict disruptions, and prioritize emergency vehicles.

## Components

### 1. TrafficLight Class

Represents a traffic light at an intersection.

- Attributes:
  - `color`: Current color of the traffic light (Green, Yellow, Red).
  - `time`: Duration of each traffic light state.

- Methods:
  - `change_color`: Changes the traffic light color based on the current state.
  - `change_time`: Updates the duration of each traffic light state.

### 2. Vehicle Class

Simulates a vehicle approaching an intersection.

- Attributes:
  - `waiting_time`: Time the vehicle has been waiting at the intersection.
  - `position`: Current position of the vehicle.

- Methods:
  - `stop`: Stops the vehicle if the traffic light is red.
  - `request_green_light`: Requests a green light if waiting time exceeds a threshold.

### 3. RoadSign Class

Represents a road sign indicating traffic rules.

- Attributes:
  - `sign_type`: Type of road sign (e.g., Go, Yield, Stop).

### 4. Lane Class

Represents a lane on a road.

- Attributes:
  - `lane_id`: Identifier for the lane.
  - `vehicles`: List of vehicles in the lane.

- Methods:
  - `add_vehicle`: Adds a vehicle to the lane.

### 5. Road Class

Represents a road with multiple lanes.

- Attributes:
  - `name`: Name of the road.
  - `lanes`: List of lanes on the road.

### 6. Intersection Class

Represents an intersection with traffic lights and road signs.

- Attributes:
  - `name`: Name of the intersection.
  - `traffic_light`: TrafficLight instance controlling the intersection's traffic light.
  - `road_sign`: RoadSign instance indicating traffic rules.
  - `road`: Road instance associated with the intersection.

- Methods:
  - `change_road_sign`: Updates the road sign based on the traffic light color.
  - `check_change_with_time`: Checks if it's time to change the traffic light color.

### 7. CentralCoordinationAgent Class

Coordinates traffic flow by adjusting traffic light timings.

- Attributes:
  - `intersections`: List of intersections to coordinate.

- Methods:
  - `optimize_traffic_flow`: Adjusts traffic light timings based on traffic conditions.

### 8. DisruptionManagementAgent Class

Predicts disruptions and communicates with other agents.

- Methods:
  - `predict_disruptions`: Predicts disruptions and communicates with Traffic Light Agents.

### 9. EmergencyVehicleAgent Class

Manages emergency vehicle priority.

- Methods:
  - `request_priority`: Requests priority for emergency vehicles and communicates with Traffic Light Agents.

### 10. Environment Class

Represents the overall environment with multiple roads and intersections.

- Attributes:
  - `roads`: List of roads in the environment.
  - `intersections`: List of intersections in the environment.
  - `central_agent`: CentralCoordinationAgent instance.
  - `disruption_agent`: DisruptionManagementAgent instance.
  - `emergency_agent`: EmergencyVehicleAgent instance.

- Methods:
  - `add_road`: Adds a road to the environment.
  - `add_intersection`: Adds an intersection to the environment.
  - `display`: Displays the current state of roads and intersections.

## Execution

The system is executed by creating an instance of the Environment class and calling the `display` method. During execution, the environment simulates traffic flow, adjusts traffic light timings, predicts disruptions, and handles emergency vehicle priorities.

## Conclusion

The Traffic Management System provides a modular and extensible framework for simulating and optimizing traffic flow at intersections. Each component plays a specific role, contributing to a comprehensive simulation of a real-world traffic management scenario. The system's flexibility allows for further enhancements and customizations to meet specific requirements and scenarios.