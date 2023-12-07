# Tests
## Test 1 (Test4TrafficLights1.py)
In this first test, there are no rules and the traffic lights control themselves.

## Test 2 (Test4TrafficLights.py)
In this second test, there are no rules and another agent is added, the Central Coordination.
This agent is responsible for controlling the color of the traffic lights.

This are the agents that were changed/added in this test:

### Central Coordination Agent (new)
`on_start` method: this will run when the agent starts; it sends a message to the agents 1 and 3 to 'turn on' the green light, and another message to the agents 2 and 4 to 'turn on' the Red light.

`run` method: after the on_method finishes, this will start; here, the central coordination agent will check if the first light is green, and, a reminder:
- 1 and 3 are connected, if 1 is green, 3 is green; if 1 is red, 3 is red; 
- 2 and 4 are the opposite to 1, if 1 is green, 2 and 4 are red; if 1 is red, 3 and 4 are green
So, if the light 1 is green, it waits 22 seconds to change it to red (note: the yellow part is done inside the traffic lights), and then, awaits 8 more seconds to change the others to green (remember that we need some time in between so the cars don't hit themselves).
If the light 1 is red, it does the opposite.

### Traffic Light (changed)
As said before, the traffic lights don't decide to change their own colors anymore, so now, in their behaviour, they recieve the message from the central and change their color based on it. It also has a count to verify if it is the first time they are 'turning on', this happens because, in the first time, the yellow won't show before the red.

## Messages
These tests are the first time we use messages, so basically, a bit about them:
- Messages are a way that the agents communicate
- 1 agent is the sender, another is a the reciever
- The jid is needed to define who will recieve the message, therefore, here, the traffic lights have different jids than the ones we used before

# Results
It is clear, looking at the txt files, that the first test, where the lights 
are not controlled by the central command, was better, *but*, this central 
agent is needed for the next steps of the project, therefore, the test number 
2 will be going foward to another comparison.
