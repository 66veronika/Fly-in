from .enums import ZoneType, HubType


class Zone:
    """Represent a zone in the drone network."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        hub_type: HubType,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str = "none",
        max_drones: int = 1,
    ) -> None:
        """Initialize a zone with its position, type, and capacity."""
        self.name = name
        self.x = x
        self.y = y
        self.hub_type = hub_type
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones

        # drones in currect zone
        self.occupants: set[int] = set()
        self.reservations: set[int] = set()

    @property
    def is_start(self) -> bool:
        """Return whether this zone is the start hub."""
        return self.hub_type == HubType.START

    @property
    def is_end(self) -> bool:
        """Return whether this zone is the end hub."""
        return self.hub_type == HubType.END

    def movement_cost(self) -> int:
        """Return the cost in turns it takes to move into this zone."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1

    def is_accessible(self) -> bool:
        """Return whether drones are allowed to enter this zone."""
        return self.zone_type != ZoneType.BLOCKED
