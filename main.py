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

    paths = pathfinder.find_all_paths()

    assignments = pathfinder.assign_paths(
        paths,
        network.nb_drones,
    )

    print("\n=== Assignments ===")

    for drone_id, path in enumerate(assignments):
        print(
            f"Drone {drone_id}: "
            f"{path} "
            f"cost={pathfinder.path_cost(path)}"
        )
        print(
            path,
            "cost=",
            pathfinder.path_cost(path),
            "capacity=",
            pathfinder.path_bottleneck_capacity(path),
        )

    simulator = Simulator(network, assignments)

    print("\n=== Drone Paths ===")

    for drone in simulator.drones:
        print(
            f"Drone {drone.drone_id}: "
            f"{drone.path}"
        )
    simulator.run()


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        print("\nInterrupted")
