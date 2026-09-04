from enum import Enum


class ZoneType(Enum):
    """Define the functional types of a zone."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubType(Enum):
    """Define the structural type of a zone."""

    START = "start_hub"
    NORMAL = "hub"
    END = "end_hub"
