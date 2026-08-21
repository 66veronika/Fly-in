from builder import NetworkBuilder
from parser import Parser
from validator import Validator
from pathfinder_dik import Pathfinder
from simulator import Simulator


def main() -> None:
    parser = Parser("maps/challenger/01_the_impossible_dream.txt")
    data = parser.parse()

    validator = Validator(data)
    validator.validate()

    builder = NetworkBuilder(data)
    network = builder.build()

    pathfinder = Pathfinder(network)

    # Dijkstra: cheapest path for one drone.
    shortest_path = pathfinder.find_path()

    if not shortest_path:
        raise RuntimeError(
            "No path from start to goal"
        )

    print("\n=== Dijkstra Shortest Path ===")
    print(
        shortest_path,
        "cost=",
        pathfinder.path_cost(shortest_path),
    )

    # Candidate paths for multi-drone routing.
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

    simulator = Simulator(
        network,
        assignments,
    )

    simulator.run()


if __name__ == "__main__":
    main()