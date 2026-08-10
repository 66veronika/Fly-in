from models.connection import Connection
from models.enums import HubType, ZoneType
from models.network import Network
from models.zone import Zone


class NetworkBuilder:
    def __init__(self, data: dict) -> None:
        self.data = data

    def build(self) -> Network:
        network = Network(
            nb_drones=self.data["nb_drones"]["number"]
        )

        self.build_zones(network)
        self.build_connections(network)

        return network

    def build_zones(self, network: Network) -> None:
        for zone_data in self.data["zones"]:
            zone = Zone(
                name=zone_data["name"],
                x=zone_data["x"],
                y=zone_data["y"],
                hub_type=HubType(zone_data["type"]),
                zone_type=ZoneType(zone_data["zone_type"]),
                color=zone_data["color"],
                max_drones=zone_data["max_drones"],
            )

            network.add_zone(zone)

    def build_connections(self, network: Network) -> None:
        for connection_data in self.data["connections"]:
            connection = Connection(
                zone_a=connection_data["from"],
                zone_b=connection_data["to"],
                max_link_capacity=connection_data[
                    "max_link_capacity"
                ],
            )

            network.add_connection(connection)
