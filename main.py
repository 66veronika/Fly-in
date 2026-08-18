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

    print("\n=== INITIAL ===")
    for drone in simulator.drones:
        print(drone)

    print("start:", network.get_zone("start").occupants)
    print("middle:", network.get_zone("middle").occupants)
    print("goal:", network.get_zone("goal").occupants)


    print("\n=== TURN 1 ===")
    simulator.simulate_turn()

    for drone in simulator.drones:
        print(drone)

    print("start:", network.get_zone("start").occupants)
    print("middle:", network.get_zone("middle").occupants)
    print("goal:", network.get_zone("goal").occupants)


    print("\n=== TURN 2 ===")
    simulator.simulate_turn()

    for drone in simulator.drones:
        print(drone)

    print("start:", network.get_zone("start").occupants)
    print("middle:", network.get_zone("middle").occupants)
    print("goal:", network.get_zone("goal").occupants)


    print("\n=== TURN 3 ===")
    simulator.simulate_turn()

    for drone in simulator.drones:
        print(drone)

    print("start:", network.get_zone("start").occupants)
    print("middle:", network.get_zone("middle").occupants)
    print("goal:", network.get_zone("goal").occupants)

if __name__ == "__main__":
    main()
