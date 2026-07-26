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
        self.occupants: set[int] = set()