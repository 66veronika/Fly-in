from models.drone import Drone
from models.network import Network


class Simulator:
    def __init__(
        self,
        network: Network,
        assignments: list[list[str]],
    ) -> None:
        if len(assignments) != network.nb_drones:
            raise ValueError(
                "Number of path assignments must "
                "match number of drones"
            )

        self.network = network
        self.assignments = assignments
        self.drones: list[Drone] = []

        self.create_drones()

    def create_drones(self) -> None:
        start = self.network.get_start_zone()

        for drone_id in range(
            self.network.nb_drones
        ):
            drone_path = self.assignments[drone_id]

            drone = Drone(
                drone_id=drone_id,
                current_zone=start.name,
                path=drone_path,
            )

            self.drones.append(drone)

            # Start is the special exception:
            # all drones may initially occupy it.
            start.occupants.add(drone_id)

    def get_next_zone(
        self,
        drone: Drone,
    ) -> str | None:
        if drone.current_zone == drone.path[-1]:
            return None

        current_index = drone.path.index(
            drone.current_zone
        )

        return drone.path[current_index + 1]

    def start_move(
        self,
        drone: Drone,
    ) -> bool:
        if drone.is_in_transit:
            return False

        next_zone_name = self.get_next_zone(drone)

        if next_zone_name is None:
            return False

        destination = self.network.get_zone(
            next_zone_name
        )

        if not destination.is_accessible():
            return False

        if not destination.has_capacity():
            return False

        connection = self.network.get_connection(
            drone.current_zone,
            next_zone_name,
        )

        if connection is None:
            raise RuntimeError(
                "Path contains zones that are not connected"
            )

        if not connection.has_capacity():
            return False

        source = self.network.get_zone(
            drone.current_zone
        )

        # Reserve destination before leaving the source.
        destination.reserve(drone.drone_id)

        source.remove_drone(drone.drone_id)

        connection.add_drone(drone.drone_id)

        drone.start_transit(
            connection,
            next_zone_name,
            destination.movement_cost(),
        )

        return True

    def advance_move(
        self,
        drone: Drone,
    ) -> bool:
        if not drone.is_in_transit:
            return False

        connection = drone.in_transit_connection
        destination_name = drone.destination_zone

        if (
            connection is None
            or destination_name is None
        ):
            raise RuntimeError(
                f"Drone {drone.drone_id} "
                "has invalid transit state"
            )

        arrived = drone.advance_transit()

        if not arrived:
            return False

        connection.remove_drone(
            drone.drone_id
        )

        destination = self.network.get_zone(
            destination_name
        )

        destination.remove_reservation(
            drone.drone_id
        )

        destination.add_drone(
            drone.drone_id
        )

        return True

    def simulate_turn(self) -> bool:
        progress = False

        arrived_this_turn: set[int] = set()

        # Phase 1:
        # Advance drones already travelling.
        for drone in self.drones:
            if not drone.is_in_transit:
                continue

            # Even if it does not arrive this turn,
            # its timer decreases, so progress occurred.
            progress = True

            arrived = self.advance_move(drone)

            if arrived:
                arrived_this_turn.add(
                    drone.drone_id
                )

        # Phase 2:
        # Start new movements.
        for drone in self.drones:
            # A drone cannot arrive and leave again
            # during the same turn.
            if drone.drone_id in arrived_this_turn:
                continue

            if drone.is_in_transit:
                continue

            started = self.start_move(drone)

            if started:
                progress = True

        return progress

    def all_delivered(self) -> bool:
        end = self.network.get_end_zone().name

        for drone in self.drones:
            if not drone.is_delivered(end):
                return False

        return True

    def run(self) -> None:
        turn = 0

        while not self.all_delivered():
            turn += 1

            print(f"\n=== TURN {turn} ===")

            progress = self.simulate_turn()

            if not progress:
                raise RuntimeError(
                    "Simulation deadlock: "
                    "no drone can make progress"
                )

            for drone in self.drones:
                print(drone)