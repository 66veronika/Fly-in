from models.drone import Drone
from models.network import Network


class Simulator:
    def __init__(
        self,
        network: Network,
        path: list[str]
    ) -> None:

        self.network = network
        self.path = path
        self.drones: list[Drone] = []

        self.create_drones()

    def create_drones(self) -> None:
        start = self.network.get_start_zone()

        for drone_id in range(self.network.nb_drones):
            drone = Drone(
                drone_id=drone_id,
                current_zone=start.name,
            )

            self.drones.append(drone)
            start.occupants.add(drone_id)

    def get_next_zone(self, drone: Drone) -> str | None:
        if drone.current_zone == self.path[-1]:
            return None

        current_index = self.path.index(
            drone.current_zone
        )

        return self.path[current_index + 1]

    def start_move(self, drone: Drone) -> bool:
        if drone.is_in_transit:
            return False

        next_zone_name = self.get_next_zone(drone)
        if next_zone_name is None:
            return False

        destination = self.network.get_zone(next_zone_name)
        if not destination.has_capacity():
            return False
        if not destination.is_accessible():
            return False

        connection = self.network.get_connection(
            drone.current_zone,
            next_zone_name,
        )
        if connection is None:
            raise ValueError(
                "Path contains zones that are not connected"
            )
        if not connection.has_capacity():
            return False

        source = self.network.get_zone(
            drone.current_zone
        )
        source.remove_drone(drone.drone_id)
        connection.add_drone(drone.drone_id)

        drone.start_transit(
            connection,
            next_zone_name,
            destination.movement_cost(),
        )

        return True

    def advance_move(self, drone: Drone) -> bool:
        if not drone.is_in_transit:
            return False

        connection = drone.in_transit_connection
        destination_name = drone.destination_zone

        arrived = drone.advance_transit()
        if not arrived:
            return False
        connection.remove_drone(drone.drone_id)

        destination = self.network.get_zone(destination_name)
        destination.add_drone(drone.drone_id)

        return True

    def simulate_turn(self) -> None:
        arrived_this_turn: set[int] = set()
        for drone in self.drones:
            if drone.is_in_transit:
                arrived = self.advance_move(drone)

                if arrived:
                    arrived_this_turn.add(drone.drone_id)

        for drone in self.drones:
            if drone.drone_id in arrived_this_turn:
                continue

            if not drone.is_in_transit:
                self.start_move(drone)