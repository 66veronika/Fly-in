from models.connection import Connection
from models.zone import Zone


class Network:
    def __init__(self, nb_drones: int) -> None:
        if nb_drones <= 0:
            raise ValueError(
                "Number of drones must be a positive integer"
            )

        self.nb_drones = nb_drones

        # Zone name -> Zone object
        self.zones: dict[str, Zone] = {}

        # All undirected connections in the network
        self.connections: list[Connection] = []

        # Names of the structural start and end zones
        self.start_zone: str | None = None
        self.end_zone: str | None = None

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the network."""
        if zone.name in self.zones:
            raise ValueError(
                f"Zone '{zone.name}' already exists"
            )

        if zone.is_start:
            if self.start_zone is not None:
                raise ValueError(
                    "Network already contains a start zone"
                )

            self.start_zone = zone.name

        if zone.is_end:
            if self.end_zone is not None:
                raise ValueError(
                    "Network already contains an end zone"
                )

            self.end_zone = zone.name

        self.zones[zone.name] = zone

    def add_connection(
        self,
        connection: Connection,
    ) -> None:
        """Add an undirected connection to the network."""
        if connection.zone_a not in self.zones:
            raise ValueError(
                f"Unknown zone '{connection.zone_a}'"
            )

        if connection.zone_b not in self.zones:
            raise ValueError(
                f"Unknown zone '{connection.zone_b}'"
            )

        existing_connection = self.get_connection(
            connection.zone_a,
            connection.zone_b,
        )

        if existing_connection is not None:
            raise ValueError(
                "Connection already exists between "
                f"'{connection.zone_a}' and "
                f"'{connection.zone_b}'"
            )

        self.connections.append(connection)

    def get_zone(self, zone_name: str) -> Zone:
        """Return a zone object using its name."""
        if zone_name not in self.zones:
            raise ValueError(
                f"Unknown zone '{zone_name}'"
            )

        return self.zones[zone_name]

    def get_start_zone(self) -> Zone:
        """Return the start Zone object."""
        if self.start_zone is None:
            raise RuntimeError(
                "Network does not contain a start zone"
            )

        return self.zones[self.start_zone]

    def get_end_zone(self) -> Zone:
        """Return the end Zone object."""
        if self.end_zone is None:
            raise RuntimeError(
                "Network does not contain an end zone"
            )

        return self.zones[self.end_zone]

    def get_connection(
        self,
        zone_a: str,
        zone_b: str,
    ) -> Connection | None:
        """
        Return the connection between two zones.

        Returns None when no such connection exists.
        """
        for connection in self.connections:
            if connection.connects_both(
                zone_a,
                zone_b,
            ):
                return connection

        return None

    def neighbors(
        self,
        zone_name: str,
        accessible_only: bool = False,
    ) -> list[str]:
        """
        Return the names of all zones directly connected
        to the given zone.

        When accessible_only is True, blocked zones
        are excluded.
        """
        if zone_name not in self.zones:
            raise ValueError(
                f"Unknown zone '{zone_name}'"
            )

        result: list[str] = []

        for connection in self.connections:
            if not connection.connects(zone_name):
                continue

            neighbor_name = connection.other_end(
                zone_name
            )

            neighbor = self.zones[neighbor_name]

            if (
                accessible_only
                and not neighbor.is_accessible()
            ):
                continue

            result.append(neighbor_name)

        return result

    def __repr__(self) -> str:
        return (
            "Network("
            f"nb_drones={self.nb_drones}, "
            f"zones={len(self.zones)}, "
            f"connections={len(self.connections)}, "
            f"start_zone={self.start_zone!r}, "
            f"end_zone={self.end_zone!r}"
            ")"
        )