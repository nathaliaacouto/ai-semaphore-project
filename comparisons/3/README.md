# Tests
## Test 3 (Test4TrafficLights3.py) 🏆
In this test, the Central Coordination agent is responsible for controlling the color of the traffic lights and there is just one rule:

1. The light with more cars on the queue is turned on 

The Central Coordination agent verifies the light with more vehicles on the queue after 20s and it turns it and the other one related to green, also closing the other two

## Test 4 (Test4TrafficLights4.py) 
In this second test, the Central Coordination agent is responsible for controlling the color of the traffic lights and there is just one rule:

1. The light with biggest medium awaiting time queue is turned on after 20s

The Central Coordination agent verifies the light with more vehicles on the queue after 20s and it turns it and the other one related to green, also closing the other two

---

This are the agents that were changed/added in this test:

### Central Coordination Agent (changed)
`run` method: after the on_method finishes, this will start; here, the central coordination agent will check which is the queue with the biggest awaiting time, and turn on the traffic light for it (and turn the others off).

### Vehicles (changed)
The first time the vehicle reaches the traffic light, it adds the awaiting time to the array of the vehicles queue time, and it keeps updating this time, when the light turns green, it takes that time off.

## Messages
A bit about messages:
- Messages are a way that the agents communicate
- 1 agent is the sender, another is a the reciever
- The jid is needed to define who will recieve the message, therefore, here, the traffic lights have different jids than the ones we used before

# Results
This comparison was to see if it was better to give priority to the queues with the biggest awaiting time or the biggest size.
There was little difference, but still, the test 3 has done better, so test number 3 will go on and be improved.
