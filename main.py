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

    simulator = Simulator(
        network,
        path,
    )

    drone = simulator.drones[0]

    print("\n=== Before move ===")
    print(drone)
    print("Start occupants:", network.get_start_zone().occupants)

    moved = simulator.start_move(drone)

    print("\nMoved:", moved)

    print("\n=== After move ===")
    print(drone)
    print("Start occupants:", network.get_start_zone().occupants)

    next_zone = simulator.get_next_zone(drone)

    connection = network.get_connection(
        drone.current_zone,
        next_zone,
    )

    print("Connection occupants:", connection.occupants)


if __name__ == "__main__":
    main()
