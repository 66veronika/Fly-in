from .enums import ZoneType, HubType


class Zone:
    def __init__( 
        self,
        name: str,
        x: int,
        y: int,
        hub_type: HubType,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str = "none",
        max_drones: int = 1
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.hub_type = hub_type
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones

        # drones in currect zone
        self.occupants: set[int] = set()

    @property
    def is_start(self) -> bool:
        return self.hub_type == HubType.START

    @property
    def is_end(self) -> bool:
        return self.hub_type == HubType.END

    def has_capacity(self) -> bool:
        """End zone accepts all drones"""
        if self.is_end:
            return True

        return len(self.occupants) < self.max_drones

    def movement_cost(self) -> int:
        """Cost in turns to move into this zone."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1

    def is_accessible(self) -> bool:
        return self.zone_type != ZoneType.BLOCKED
