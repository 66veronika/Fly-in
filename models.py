from enum import Enum
from typing import Optional


class ZoneType(Enum):
    """Zone type provided from zone metadata."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubType(Enum):
    """Structural role of a zone in the map."""

    START = "start_hub"
    NORMAL = "hub"
    END = "end_hub"


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
    self.name = name,
    