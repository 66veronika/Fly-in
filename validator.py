

class Validator:
    def __init__(self, data: dict) -> None:
        self.data = data

    def validate(self) -> None:
        self.validate_nb_drones()
        self.validate_zones()
        self.validate_connections()
    
    def validate_nb_drones() -> None:
        nb_drones = self.data["nb_drones"]

        if nb_drones is None:
            raise ValueError(
                "nb_drones is missing"
            )
        if nb_drones <= 0:
            raise ValueError(
                "Number of drones must be a positive integer"
            )

    def validate_zones(self) -> None:
        zones = self.data["zones"]
        names = set()
        start_hubs = 0
        end_hubs = 0

        if not zones:
            raise ValueError(
                "No zones defined"
            )
        for zone in zones:
            line = zone["line_number"]
            name = zone["name"]

            if not name:
                raise ValueError(
                    f"Line {line}: zone name cannot be empty"
                )
            if name in names:
                raise ValueError(
                    f"Line {line}: duplicate zone name ({name})"
                )
            names.add(name)

            try:
                zone["x"] = int(zone["x"])
                zone["y"] = int(zone["y"])
            except ValueError:
                raise ValueError(
                    f"Line {line}: zone coordinates must be integers"
                )

            if zone["type"] == "start_hub":
                start_hubs += 1
            elif zone["type"] == "end_hub":
                end_hubs += 1
            elif zone["type"] != "hub":
                raise ValueError(
                    f"Line {line}: invalid zone type ({zone["type"]})"
                )

        if start_hubs == 0:
            raise ValueError(
                "Map must contain one start_hub"
            )
        elif start_hubs > 1:
            raise ValueError(
                f"{line}: there must be only one start_hub"
            )
        if end_hubs == 0:
            raise ValueError(
                "Map must contain one end_hub"
            )
        elif end_hubs > 1:
            raise ValueError(
                f"{line}: there must be only one end_hub"
            )
        
    def validate_connections(self) -> None:
        zone_names = set()

        for zone in self.data["zones"]:
            zone_names.add(zone["name"])

        for connection in self.data["connections"]:
            from_zone = connection["from"]
            to_zone = connection["to"]
            line_number = connection["line_number"]

            if not from_zone:
                raise ValueError(
                    f"Line {line_number}: source zone cannot be empty"
                )
            if not to_zone:
                raise ValueError(
                    f"Line {line_number}: destination zone cannot be empty"
                )
            if from_zone not in zone_names:
                raise ValueError(
                    f"Line {line_number}: unknown zone ({from_zone})"
                )
            if to_zone not in zone_names:
                raise ValueError(
                    f"Line {line_number}: unknown zone ({to_zone})"
                )
            if from_zone == to_zone:
                raise ValueError(
                    f"Line {line_number}: a zone cannot connect to itself"
                )
            


?????????????????
key = frozenset((conn["from"], conn["to"]))
            if key in seen:
                raise ValueError(
                    f"Line {line}: duplicate connection between '{conn['from']}' and '{conn['to']}'"
                )
            seen.add(key)