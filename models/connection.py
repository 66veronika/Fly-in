class Connection:
    """Represent an undirected connection between two zones."""

    def __init__(
            self,
            zone_a: str,
            zone_b: str,
            max_link_capacity: int = 1,
    ) -> None:
        """Initialize a connection between two zones."""

        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

        self.occupants: set[int] = set()

    def connects(self, zone_name: str) -> bool:
        """Return whether the connection contains the given zone."""
        return zone_name in (self.zone_a, self.zone_b)

    def connects_both(
        self,
        zone_a: str,
        zone_b: str,
    ) -> bool:
        """Return whether the connection joins the two given zones."""

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
        """Return the zone on the other end of the connection."""

        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        raise ValueError(
            f"Zone '{zone_name}' is not part of this connection"
        )

    def has_capacity(self) -> bool:
        """Return whether the connection can accept another drone."""
        return len(self.occupants) < self.max_link_capacity

    def add_drone(self, drone_id: int) -> None:
        """Add a drone to the connection."""
        if drone_id in self.occupants:
            raise ValueError(
                f"Drone {drone_id} is already on connection "
                f"'{self.zone_a}-{self.zone_b}'"
            )

        if not self.has_capacity():
            raise ValueError(
                f"Connection '{self.zone_a}-{self.zone_b}' "
                "has reached its capacity"
            )

        self.occupants.add(drone_id)

    def remove_drone(self, drone_id: int) -> None:
        """Remove a drone from the connection."""
        if drone_id not in self.occupants:
            raise ValueError(
                f"Drone {drone_id} is not on connection "
                f"'{self.zone_a}-{self.zone_b}'"
            )

        self.occupants.remove(drone_id)

    def __repr__(self) -> str:
        """Return a readable representation of the connection."""
        return (
            "Connection("
            f"{self.zone_a!r} <-> "
            f"{self.zone_b!r}, "
            f"capacity={self.max_link_capacity}, "
            f"occupants={len(self.occupants)}"
            ")"
        )
