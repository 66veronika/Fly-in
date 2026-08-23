import sys

from builder import NetworkBuilder
from parser import Parser
from pathfinder_dik import Pathfinder
from simulator import Simulator
from validator import Validator


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>")
        return

    filepath = sys.argv[1]

    parser = Parser(filepath)
    data = parser.parse()

    validator = Validator(data)
    validator.validate()

    builder = NetworkBuilder(data)
    network = builder.build()

    pathfinder = Pathfinder(network)

    schedules = pathfinder.plan_all_drones(
        network.nb_drones
    )

    simulator = Simulator(
        network,
        schedules,
    )

    simulator.run()


if __name__ == "__main__":
    main()