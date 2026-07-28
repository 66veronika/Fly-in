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
