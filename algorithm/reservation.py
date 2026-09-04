class ReservationTable:
    """Tracks which zone/turn and connection/turn slots are reserved."""

    def __init__(self) -> None:
        self.zone_reservations: dict[
            tuple[str, int],
            int,
        ] = {}

        self.connection_reservations: dict[
            tuple[tuple[str, str], int],
            int,
        ] = {}

    def zone_free(
        self,
        zone_name: str,
        max_drones: int | float,
        turn: int,
    ) -> bool:
        used = self.zone_reservations.get(
            (zone_name, turn),
            0,
        )

        return used < max_drones

    def connection_free(
        self,
        zone_a: str,
        zone_b: str,
        max_link_capacity: int,
        start_turn: int,
        end_turn: int,
    ) -> bool:
        connection = tuple(sorted((
            zone_a,
            zone_b,
        )))

        for turn in range(
            start_turn,
            end_turn,
        ):
            key = (
                connection,
                turn,
            )

            used = self.connection_reservations.get(
                key,
                0,
            )

            if used >= max_link_capacity:
                return False

        return True

    def reserve_zone(
        self,
        zone_name: str,
        turn: int,
    ) -> None:
        key = (
            zone_name,
            turn,
        )

        self.zone_reservations[key] = (
            self.zone_reservations.get(
                key,
                0,
            )
            + 1
        )

    def reserve_connection(
        self,
        zone_a: str,
        zone_b: str,
        start_turn: int,
        end_turn: int,
    ) -> None:
        connection = tuple(sorted((
            zone_a,
            zone_b,
        )))

        for turn in range(
            start_turn,
            end_turn,
        ):
            key = (
                connection,
                turn,
            )

            self.connection_reservations[key] = (
                self.connection_reservations.get(
                    key,
                    0,
                )
                + 1
            )
