The A* Romania Pathfinder is an implementation of the A* search algorithm designed to find the shortest path between cities in Romania’s road network. This project demonstrates how informed search algorithms can efficiently solve pathfinding problems using both actual costs and heuristic estimates.

The A* algorithm provides an efficient solution by combining:

- **g(n)**: The actual cost from the start node to the current node
- **h(n)**: A heuristic estimate of the cost from the current node to the goal
- **f(n) = g(n) + h(n)**: The total estimated cost
### Graph Representation

The Romanian road network is modeled as a weighted graph using Python dictionaries, where:

- Each city is a node in the graph
- Each road is an edge with a weight representing the distance in kilometers
- Cities are connected bidirectionally with their neighbors

Admissible Heuristics

The implementation uses straight-line distance estimates to Bucharest as heuristics for each city:

- **Arad**: 366 km
- **Sibiu**: 253 km
- **Pitesti**: 100 km
- **Bucharest**: 0 km (goal)

These heuristics guide the search toward the goal efficiently without overestimating costs.

Visual Graph Representation

The project includes visualization capabilities using NetworkX and Matplotlib:

- Display all cities and road connections
- Show distances on each road segment
- Highlight the optimal path in red for easy identification

Optimal Path Finding

For the route from Arad to Bucharest, the algorithm finds:

- **Optimal Route**: Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest
- **Total Distance**: 418 km

talk something for the A* vs UCS

