# Tests
## Test 2 (Test4TrafficLights2.py)
In this second test, there are no rules and the Central Coordination agent is responsible for controlling the color of the traffic lights.

## Test 3 (Test4TrafficLights3.py) 🏆
In this second test, the Central Coordination agent is responsible for controlling the color of the traffic lights and there is just one rule:

1. The light with more cars on the queue is turned on 

The Central Coordination agent verifies the light with more vehicles on the queue after 20s and it turns it and the other one related to green, also closing the other two

---

This are the agents that were changed/added in this test:

### Central Coordination Agent (changed)
`on_start` method: this will run when the agent starts; it awaits 10s just to give time for the cars to be generated and go to the semaphore

`run` method: after the on_method finishes, this will start; here, the central coordination agent will check which is the queue with most cars in it, and turn on the traffic light for it (and turn the others off).

### Vehicles (changed)
The first time the vehicle reaches the traffic light, it adds a number 1* to the array of the queues, indicating it is waiting, when the light turns green, it takes that number off.

*the number really doesn't matter, it could be 2, 3, 4, 5.., it is merely a way to show that there is a vehicle awaiting 

## Messages
A bit about messages:
- Messages are a way that the agents communicate
- 1 agent is the sender, another is a the reciever
- The jid is needed to define who will recieve the message, therefore, here, the traffic lights have different jids than the ones we used before

# Results
The test number 3 has gone better than expected, with results that are similar to the ones from the test 1 (our best until now), so, this test number 3 will go on and be improved.
