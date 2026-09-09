import sys

import arcade

from algorithm import Pathfinder
from builder import NetworkBuilder
from logger import Logger
from parser import Parser
from renderer import Renderer
from simulator import Simulator
from validator import Validator


def main() -> None:
    """Run the Fly-in simulation."""
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>")
        return

    filepath = sys.argv[1]

    try:
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

        Renderer(
            network,
            schedules,
        )
        arcade.run()

    except MemoryError:
        print("Error: not enough memory to run this simulation")
    except (ValueError, RuntimeError, OSError, OverflowError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()