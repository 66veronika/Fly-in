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

    def has_capacity(self) -> bool:
        """Return whether the zone can accept another drone.
        End zone accepts al drones."""
        if self.is_end:
            return True

        return (
            len(self.occupants)
            + len(self.reservations)
            < self.max_drones
        )

    def movement_cost(self) -> int:
        """Return the cost in turns it takes to move into this zone."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1

    def is_accessible(self) -> bool:
        """Return whether drones are allowed to enter this zone."""
        return self.zone_type != ZoneType.BLOCKED

    def add_drone(self, drone_id: int) -> None:
        """Add a drone to the zone."""
        if drone_id in self.occupants:
            raise ValueError(
                f"Drone {drone_id} is already inside zone '{self.name}'"
            )

        if not self.has_capacity():
            raise ValueError(
                f"Zone '{self.name}' has reached its capacity"
            )

        self.occupants.add(drone_id)

    def remove_drone(self, drone_id: int) -> None:
        """Remove a drone fron a zone."""
        if drone_id not in self.occupants:
            raise ValueError(
                f"Drone {drone_id} is not in zone '{self.name}'"
            )

        self.occupants.remove(drone_id)

    def reserve(self, drone_id: int) -> None:
        """Reserve space in the zone for a drone."""
        if drone_id in self.reservations:
            raise ValueError(
                f"Drone {drone_id} already has a reservation "
                f"in zone '{self.name}'"
            )

        if not self.has_capacity():
            raise ValueError(
                f"Zone '{self.name}' has no capacity to reserve"
            )

        self.reservations.add(drone_id)

    def remove_reservation(self, drone_id: int) -> None:
        """Remove a drone's reservation from the zone."""
        if drone_id not in self.reservations:
            raise ValueError(
                f"Drone {drone_id} has no reservation "
                f"in zone '{self.name}'"
            )

        self.reservations.remove(drone_id)

    def __repr__(self) -> str:
        """Return a readable representation of the zone."""
        return (
            "Zone("
            f"name={self.name!r}, "
            f"hub_type={self.hub_type.value!r}, "
            f"zone_type={self.zone_type.value!r}, "
            f"occupants={len(self.occupants)}/{self.max_drones}"
            ")"
        )
