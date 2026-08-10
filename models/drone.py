from models.connection import Connection


class Drone:
    def __init__(
            self,
            drone_id: int,
            current_zone: str,
    ) -> None:
        self.drone_id = drone_id
        self.current_zone = current_zone

        self.in_transit_connection: Connection | None = None
        self.destination_zone: str | None = None
        self.turns_remaining: int = 0

    @property
    def is_in_transit(self) -> bool:
        return self.in_transit_connection is not None

    def is_delivered(self, end_zone: str) -> bool:
        return (
            not self.is_in_transit
            and self.current_zone == end_zone
        )

    def start_transit(
        self,
        connection: Connection,
        destination_zone: str,
        movement_cost: int,
    ) -> None:
        if self.is_in_transit:
            raise ValueError(
                f"Drone {self.drone_id} is already in transit"
            )

        if movement_cost <= 0:
            raise ValueError(
                "Movement cost must be positive"
            )

        self.in_transit_connection = connection
        self.destination_zone = destination_zone
        self.turns_remaining = movement_cost

        if not connection.connects(self.current_zone):
            raise ValueError(
                f"Connection does not include the drone's current "
                f"zone '{self.current_zone}'"
            )

        expected_destination = connection.other_end(
            self.current_zone
        )
        if destination_zone != expected_destination:
            raise ValueError(
                f"Zone '{destination_zone}' is not the other end of this"
                "connection"
            )

    def advance_transit(self) -> bool:
        """
        Advance the drone by one turn.

        Returns True when the drone reaches its destination.
        """
        if not self.is_in_transit:
            raise ValueError(
                f"Drone {self.drone_id} is not in transit"
            )

        self.turns_remaining -= 1

        if self.turns_remaining > 0:
            return False

        if self.destination_zone is None:
            raise RuntimeError(
                "Transit destination is missing"
            )

        self.current_zone = self.destination_zone
        self.in_transit_connection = None
        self.destination_zone = None
        self.turns_remaining = 0

        return True

    def __repr__(self) -> str:
        if self.is_in_transit:
            return (
                "Drone("
                f"id={self.drone_id}, "
                f"source={self.current_zone!r}, "
                f"destination={self.destination_zone!r}, "
                f"turns_remaining={self.turns_remaining}"
                ")"
            )

        return (
            "Drone("
            f"id={self.drone_id}, "
            f"current_zone={self.current_zone!r}"
            ")"
        )

