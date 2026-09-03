from enum import Enum


class ZoneType(Enum):
    """Define the possible functional types of a zone."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubType(Enum):
    """Define the structural role of a zone in the map."""

    START = "start_hub"
    NORMAL = "hub"
    END = "end_hub"
