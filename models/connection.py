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

    def other_end(self, zone_name: str) -> str:
        """Return the zone on the other end of the connection."""
        if zone_name == self.zone_a:
            return self.zone_b

        if zone_name == self.zone_b:
            return self.zone_a

        raise ValueError(
            f"Zone '{zone_name}' is not part of this connection"
        )
