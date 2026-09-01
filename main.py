import sys
import arcade

from builder import NetworkBuilder
from parser import Parser
from pathfinder_dik import Pathfinder
from simulator import Simulator
from validator import Validator
from renderer import Renderer
from logger import Logger


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

    logger = Logger("output.txt")

    schedules = pathfinder.plan_all_drones(
        network.nb_drones
    )

    simulator = Simulator(
        network,
        schedules,
        logger,
    )

    simulator.run()
    Renderer(network, schedules)
    arcade.run()


if __name__ == "__main__":
    main()
