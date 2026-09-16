from models.connection import Connection
from models.enums import HubType, ZoneType
from models.network import Network
from models.zone import Zone
from typing import Dict, Any


class NetworkBuilder:
    """Build a Network from validated map data."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize the builder with validated data."""
        self.data = data

    def build(self) -> Network:
        """Build and return the complete network."""
        network = Network(
            nb_drones=self.data["nb_drones"]["number"]
        )

        self._build_zones(network)
        self._build_connections(network)

        return network

    def _build_zones(self, network: Network) -> None:
        """Add all zone objects to Network."""
        for zone_data in self.data["zones"]:
            metadata = zone_data["metadata"]

            zone = Zone(
                name=zone_data["name"],
                x=int(zone_data["x"]),
                y=int(zone_data["y"]),
                hub_type=HubType(zone_data["type"]),
                zone_type=ZoneType(
                    metadata.get("zone", "normal")
                ),
                color=metadata.get("color", "none"),
                max_drones=int(
                    metadata.get("max_drones", "1")
                ),
            )

            network.add_zone(zone)

    def _build_connections(self, network: Network) -> None:
        """Add all connections to Network."""
        for connection_data in self.data["connections"]:
            metadata = connection_data["metadata"]

            connection = Connection(
                zone_a=connection_data["from"],
                zone_b=connection_data["to"],
                max_link_capacity=int(
                    metadata.get("max_link_capacity", "1")
                ),
            )

            network.add_connection(connection)
