*This project has been created as part of the 42 curriculum by vskopova.*

# Fly-in

## Description

Fly-in is a Python program that simulates routing multiple drones through a network of connected zones.

The goal is to move all drones from a start hub to an end hub in as few simulation turns as possible while respecting the rules of the network.

The program handles:

* multiple drones moving through the network
* zone capacity limits
* connection capacity limits
* normal, priority, restricted, and blocked zones
* waiting when a drone cannot safely move
* two-turn movement into restricted zones
* conflict prevention using reservations
* turn-by-turn terminal output
* graphical visualization using Arcade

The graph implementation is custom and does not use an external graph library.


---

## Instructions


### Requirements

* Python 3.10 or newer
* GNU Make
* Dependencies listed in `requirements.txt`

The main dependencies are:

* `arcade`
* `flake8`
* `mypy`

### Installation

Create the virtual environment and install the required dependencies:

```bash
make install
```

### Running the program

Run the simulation by providing a map:

```bash
make run MAP=maps/test.txt
```

For another map:

```bash
make run MAP=maps/easy/01_linear_path.txt
```

The program:

1. parses the map
2. validates the input
3. builds the network
4. calculates schedules for all drones
5. prints the simulation turn by turn
6. writes the same output to `output.txt`
7. opens the graphical visualization

### Debugging

Run the program with Python's debugger:

```bash
make debug MAP=maps/test.txt
```

### Linting and type checking

Run the mandatory static checks:

```bash
make lint
```

For stricter mypy checking:

```bash
make lint-strict
```

### Cleaning

Remove Python cache files:

```bash
make clean
```

Remove the virtual environment as well:

```bash
make fclean
```

---

## Input Format

A map starts with the number of drones and then defines zones and connections.

Example:

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: middle 1 0 [zone=normal max_drones=1]
end_hub: goal 2 0 [color=red]

connection: start-middle
connection: middle-goal
```

### Number of drones

```text
nb_drones: <positive_integer>
```

Example:

```text
nb_drones: 5
```

### Zones

Zones contain a type, name, coordinates, and optional metadata.

```text
hub: name x y [metadata]
```

The supported structural zone definitions are:

```text
start_hub:
hub:
end_hub:
```

A map must contain exactly one start hub and exactly one end hub.

### Zone metadata

Supported metadata includes:

```text
zone=normal
zone=priority
zone=restricted
zone=blocked

color=<color>
max_drones=<positive_integer>
```

If no zone type is specified, the zone is treated as normal.

If no `max_drones` value is specified, its default value is `1`.

### Connections

Connections are undirected:

```text
connection: zone_a-zone_b
```

They may contain a capacity:

```text
connection: zone_a-zone_b [max_link_capacity=2]
```

If no connection capacity is specified, its default value is `1`.

---

## Zone Types

### Normal

A normal zone takes one turn to enter.

```text
A -> B
```

If `B` is normal, the drone reaches it on the next turn.

### Priority

A priority zone also takes one turn to enter.

When multiple path choices have the same travel cost, movement toward a priority zone is preferred by the pathfinding algorithm.

### Restricted

A restricted zone takes two turns to enter.

During the intermediate turn, the drone occupies the connection between the two zones.

Example:

```text
turn 1: D1-A-B
turn 2: D1-B
```

The drone cannot remain waiting on the connection.

### Blocked

Blocked zones cannot be entered and are excluded from possible movements.

---

### Capacities

### Zone capacity

`max_drones` specifies how many drones may occupy a zone at the same turn.

The start and end hubs are treated as having unlimited capacity.

### Connection capacity

`max_link_capacity` specifies how many drones may use the same connection simultaneously.

This is especially important for restricted movements because a drone occupies the connection while travelling.

---

## Algorithm and Implementation Strategy

### Graph representation

The map is represented using custom Python classes:

* `Network` represents the complete graph
* `Zone` represents a location
* `Connection` represents an undirected connection between two zones


The network stores all zones and connections and provides operations for finding neighboring zones and connections.

No external graph library is used.

### Space-time search

The pathfinding algorithm uses **cooperative Dijkstra on an implicit space time graph**.

A search state is represented as:

```text
(zone_name, turn)
```

For example:

```text
("middle", 4)
```

means that the drone is in the `middle` zone at turn 4.

The same physical zone may therefore appear many times in the search at different turns.

For example:

```text
("middle", 3)
("middle", 4)
("middle", 5)
```

are three different search states.

### Priority queue

Python's `heapq` is used as the priority queue.

Search states are ranked using:

```text
travel cost
priority rank
move count
```

The accumulated travel cost is considered first.

If two states have the same cost, movement into a priority zone is preferred.

The move count is used as another tie-breaker when the previous values are equal.

### Waiting

Waiting is represented as another state in the space-time graph.

For example:

```text
("A", 3)
    ->
("A", 4)
```

means that the drone stays in zone `A` for one turn.

Waiting costs one turn.

This allows a drone to remain in a safe zone while waiting for another zone or connection to become available.

### Movement cost

Movement cost depends on the destination zone:

```text
normal      -> 1 turn
priority    -> 1 turn
restricted  -> 2 turns
blocked     -> inaccessible
```

### Reservation table

Drones are planned one at a time.

After a path is found for one drone, its schedule is stored in a `ReservationTable`.

The reservation table records:

* zone occupancy for each turn
* connection occupancy for each turn

The next drone searches while respecting all reservations already created by previous drones.

For every possible movement, the pathfinder checks:

1. whether the connection has enough capacity
2. whether the destination zone has enough capacity at the arrival turn
3. whether the movement respects the zone's movement cost

If the movement is not possible, the search may find another route or wait until the required capacity becomes available.

### Dynamic search limit

The search uses a dynamically calculated maximum turn instead of a fixed arbitrary value.

The limit is based on:

* the latest existing reservation
* one additional turn after existing reservations
* the maximum length of a simple path through the network
* the worst-case two-turn restricted movement cost

This keeps the space-time search finite while allowing later drones enough time to wait for previous reservations to clear.

### Planning all drones

The complete planning process is:

```text
create empty ReservationTable

for each drone:
    search for a safe schedule
    reserve the schedule
    store the schedule

simulate all stored schedules
```

This prevents later drones from creating zone or connection conflicts with schedules that have already been planned.

---

## Program Structure

The program separates parsing, validation, model creation, pathfinding, simulation, and visualization.

### Parser

`Parser` reads the map file and converts its syntax into raw structured data.

It handles:

* drone count
* zone definitions
* connection definitions
* metadata syntax

### Validator

`Validator` checks the parsed data without building the graph.

It checks conditions such as:

* positive drone count
* exactly one start and end hub
* duplicate zone names
* integer coordinates
* valid metadata keys
* valid zone types
* positive capacities
* connections referencing previously defined zones
* duplicate connections
* self-connections

### NetworkBuilder

`NetworkBuilder` receives validated data and creates the actual typed model objects.

It converts raw values into types such as:

```text
string -> int
string -> ZoneType
string -> HubType
```

and creates `Zone`, `Connection`, and `Network` objects.

### Pathfinder

`Pathfinder` calculates reservation-safe drone schedules using the cooperative Dijkstra.

### ReservationTable

`ReservationTable` tracks capacity usage for zones and connections at individual turns.

### Simulator

`Simulator` converts the calculated schedules into the required turn-by-turn textual output.

Waiting drones are omitted from a turn because they did not move.

### Logger

`Logger` prints each simulation turn and saves the output to `output.txt`.

### Renderer

The renderer displays the network and animates drone movement using Arcade.

---

## Simulation Output

Each line represents one simulation turn.

A normal movement is displayed as:

```text
D1-zone_name
```

Multiple drones moving during the same turn are separated by spaces:

```text
D1-zoneA D2-zoneB D3-zoneC
```

A drone travelling toward a restricted zone is displayed on the connection during the intermediate turn:

```text
D1-zoneA-zoneB
```

A drone that waits during a turn is not printed for that turn.

Once a drone reaches the end hub, it is considered delivered.

---

## Visual Representation

The graphical interface is implemented using Arcade.

The renderer displays:

* all zones and connections
* animated drones
* drone identifiers
* different shapes for different zone types
* map colors defined by zone metadata
* the current turn
* number of delivered drones
* simulation state
* completion information

Zone types are visually distinguished.

Priority, restricted, and blocked zones use different shapes so their behavior can be recognized directly from the map.

The map coordinates from the input file are scaled to fit the application window.

Drone positions are interpolated between zones, which allows movements to be displayed as animations rather than instant jumps.

The interface also provides keyboard controls:

```text
SPACE  Pause / Resume
R      Restart visualization
S      Skip to the end
ESC    Clear zone selection
```

Zones can also be selected with the mouse and deselected by clicking on empty space in the map or by ESC.

The visualization makes it easier to inspect routes, waiting behavior, restricted movements, and the interaction between multiple drones.

---

## Error Handling

Invalid input stops the program and prints an explanatory error.

Examples of rejected input include:

* missing or invalid drone count
* duplicate start or end hubs
* duplicate zone names
* invalid coordinates
* invalid zone types
* invalid metadata
* zero or negative capacities
* connections to unknown zones
* duplicate connections
* connections from a zone to itself

If no feasible schedule can be found for a drone, the pathfinder raises an error instead of producing an invalid simulation.

---

## Resources

Resources used while working on the project include:

* Python documentation — heapq

  * used for understanding priority queues and heap operations

* Python documentation — Enum

  * used for representing zone and hub types

* Python documentation — type hints

  * used for function annotations and static typing

* mypy documentation

  * used for static type checking

* flake8 documentation

  * used for Python style and linting

* Arcade documentation

  * used for the graphical visualization, window events, keyboard controls, and drawing functions

* General graph-search material covering Dijkstra-style shortest-path exploration

  * used to understand lowest-cost-first graph traversal

* Material about space-time pathfinding and reservation tables

  * used to understand how time can be included in a search state and how multiple moving agents can avoid conflicts

  https://api.arcade.academy/en/latest/api_docs/api/drawing_primitives.html?utm_source=chatgpt.com
  https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/
  https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
  https://www.geeksforgeeks.org/dsa/graph-data-structure-and-algorithms/

### Use of AI

AI tools, including ChatGPT, were used during development as a supporting learning and review tool.

AI assistance was used for:

* explaining pathfinding concepts such as Uniform-Cost Search, Dijkstra, and A*
* reviewing the reservation-based pathfinding approach
* explaining Python type hints and heap behavior
* discussing code organization and object-oriented design
* identifying unused code
* reviewing separation between parsing, validation, and model construction
* debugging specific implementation problems
* suggesting edge cases and validation checks
* reviewing documentation and helping structure this README

AI-generated suggestions were reviewed and adapted to the project's implementation rather than being treated as automatically correct.

## Example Input and Output

### Example input

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: middle 1 0 [zone=normal max_drones=1]
end_hub: end 2 0 [color=red]

connection: start-middle
connection: middle-end
```

This map contains:

* 2 drones
* one start hub
* one normal intermediate zone with capacity `1`
* one end hub
* two connections

Because the intermediate zone can contain only one drone at a time, the second drone must wait before entering it.

### Expected output

```text
D1-middle
D1-end D2-middle
D2-end
```

The output is printed one line per simulation turn.

On the first turn, drone 1 moves to `middle`.

On the second turn, drone 1 moves to `end`, which frees the intermediate zone, allowing drone 2 to move to `middle`.

On the third turn, drone 2 reaches `end`.
