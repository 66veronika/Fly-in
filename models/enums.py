from enum import Enum


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
