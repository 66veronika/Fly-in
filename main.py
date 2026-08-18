from builder import NetworkBuilder
from parser import Parser
from validator import Validator
from pathfinder_dik import Pathfinder
from simulator import Simulator


def main() -> None:
    parser = Parser("maps/test.txt")
    data = parser.parse()

    validator = Validator(data)
    validator.validate()

    builder = NetworkBuilder(data)
    network = builder.build()

    pathfinder = Pathfinder(network)
    path = pathfinder.find_path()

    print("\n=== Path ===")
    print(path)

    simulator = Simulator(network, path)

    drone = simulator.drones[0]

    print("\n=== Initial state ===")
    print(drone)
    print("Start occupants:", network.get_start_zone().occupants)

    next_zone_name = simulator.get_next_zone(drone)

    connection = network.get_connection(
        drone.current_zone,
        next_zone_name,
    )

    destination = network.get_zone(next_zone_name)

    print("Connection occupants:", connection.occupants)
    print("Destination occupants:", destination.occupants)

    moved = simulator.start_move(drone)

    print("\n=== After start_move ===")
    print("Started move:", moved)
    print(drone)
    print("Start occupants:", network.get_start_zone().occupants)
    print("Connection occupants:", connection.occupants)
    print("Destination occupants:", destination.occupants)

    arrived = simulator.advance_move(drone)

    print("\n=== After advance_move ===")
    print("Arrived:", arrived)
    print(drone)
    print("Start occupants:", network.get_start_zone().occupants)
    print("Connection occupants:", connection.occupants)
    print("Destination occupants:", destination.occupants)

if __name__ == "__main__":
    main()
