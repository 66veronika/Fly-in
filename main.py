from builder import NetworkBuilder
from parser import Parser
from validator import Validator


def main() -> None:
    parser = Parser("maps/example.txt")
    data = parser.parse()

    validator = Validator(data)
    validator.validate()

    builder = NetworkBuilder(data)
    network = builder.build()

    print("=== Network ===")
    print(network)

    print("\n=== Neighbors ===")

    print("start:", network.neighbors("start"))
    print("waypoint1:", network.neighbors("waypoint1"))
    print("waypoint2:", network.neighbors("waypoint2"))
    print("goal:", network.neighbors("goal"))

    print("\n=== Connection lookup ===")

    connection = network.get_connection(
        "start",
        "waypoint1",
    )
    print(connection)

    print(
        network.get_connection(
            "start",
            "goal",
        )
    )

    print("\n=== Start / End ===")

    print("Start:", network.get_start_zone())
    print("End:", network.get_end_zone())


if __name__ == "__main__":
    main()
