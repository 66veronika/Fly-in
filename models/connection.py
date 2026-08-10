class Connection:
    def __init__(
            self,
            zone_a: str,
            zone_b: str,
            max_link_capacity: int = 1,
    ) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
        # drones in currect zone
        self.occupants: set[int] = set()

    def connects(self, zone_name: str) -> bool:
        return zone_name in (self.zone_a, self.zone_b)

    def connects_both(
        self,
        zone_a: str,
        zone_b: str,
    ) -> bool:
        """
        Return True if this connection joins the two given zones.

        The connection is undirected, so A-B and B-A
        are considered the same connection.
        """
        return (
            (
                self.zone_a == zone_a
                and self.zone_b == zone_b
            )
            or
            (
                self.zone_a == zone_b
                and self.zone_b == zone_a
            )
        )

    def other_end(self, zone_name: str) -> bool:
        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        raise ValueError(
            f"Zone '{zone_name}' is not part of this connection"
        )

    def has_capacity(self) -> bool:
        return len(self.occupants) < self.max_link_capacity

    def add_drone(self, drone_id: int) -> None:
        """
        Add a drone to the connection.
        """
        if drone_id in self.occupants:
            raise ValueError(
                f"Drone {drone_id} is already "
                f"on connection "
                f"'{self.zone_a}-{self.zone_b}'"
            )

        if not self.has_capacity():
            raise ValueError(
                f"Connection "
                f"'{self.zone_a}-{self.zone_b}' "
                "has reached its capacity"
            )

        self.occupants.add(drone_id)

    def remove_drone(self, drone_id: int) -> None:
        """
        Remove a drone from the connection.
        """
        if drone_id not in self.occupants:
            raise ValueError(
                f"Drone {drone_id} is not on "
                f"connection "
                f"'{self.zone_a}-{self.zone_b}'"
            )

        self.occupants.remove(drone_id)

    def __repr__(self) -> str:
        return (
            "Connection("
            f"{self.zone_a!r} <-> "
            f"{self.zone_b!r}, "
            f"capacity={self.max_link_capacity}, "
            f"occupants={len(self.occupants)}"
            ")"
        )
