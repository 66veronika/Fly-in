from builder import NetworkBuilder
from parser import Parser
from validator import Validator
from pathfinder_dik import Pathfinder


def main() -> None:
    parser = Parser("maps/example.txt")
    data = parser.parse()

    validator = Validator(data)
    validator.validate()

    builder = NetworkBuilder(data)
    network = builder.build()

    pathfinder = Pathfinder(network)

    path = pathfinder.find_path()

    print("\n=== Path ===")
    print(path)


if __name__ == "__main__":
    main()
