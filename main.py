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

    if not paths:
        raise RuntimeError("No path from start to goal")

    print("\n=== All Paths ===")

    for path in paths:
        print(
            path,
            "cost:",
            pathfinder.path_cost(path),
        )

    path = paths[0]

    print("\n=== Chosen Path ===")
    print(path)

    simulator = Simulator(network, path)

if __name__ == "__main__":
    main()
