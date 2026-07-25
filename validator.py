class Validator:
    ALLOWED_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}
    ALLOWED_ZONE_KEYS = {"zone", "color", "max_drones"}
    ALLOWED_CONNECTION_KEYS = {"max_link_capacity"}

    def __init__(self, data: dict) -> None:
        self.data = data

    def validate(self) -> None:
        self.validate_nb_drones()
        self.validate_zones()
        self.validate_connections()

    def validate_nb_drones(self) -> None:
        nb_drones = self.data["nb_drones"]
        if not nb_drones:
            raise ValueError(
                "nb_drones is missing"
                )
        if nb_drones["number"] <= 0:
            raise ValueError(
                f"Line {nb_drones['line_number']}: "
                "Number of drones must be a positive integer"
            )

    def validate_zones(self) -> None:
        zones = self.data["zones"]
        names: set[str] = set()
        start_hub_line: int | None = None
        end_hub_line: int | None = None

        if not zones:
            raise ValueError("No zones defined")

        for zone in zones:
            line = zone["line_number"]
            name = zone["name"]

            if not name:
                raise ValueError(
                    f"Line {line}: zone name cannot be empty"
                    )
            if "-" in name:
                raise ValueError(
                    f"Line {line}: zone name cannot contain dashes ({name})"
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
                if start_hub_line is not None:
                    raise ValueError(
                        f"Line {line}: duplicate start_hub "
                        f"(already defined at line {start_hub_line})"
                    )
                start_hub_line = line

            elif zone["type"] == "end_hub":
                if end_hub_line is not None:
                    raise ValueError(
                        f"Line {line}: duplicate end_hub "
                        f"(already defined at line {end_hub_line})"
                    )
                end_hub_line = line

            elif zone["type"] != "hub":
                raise ValueError(
                    f"Line {line}: invalid zone type ({zone['type']})"
                    )

            self.validate_zone_metadata(zone)

        if start_hub_line is None:
            raise ValueError("Map must contain one start_hub")
        if end_hub_line is None:
            raise ValueError("Map must contain one end_hub")

    def validate_zone_metadata(self, zone: dict) -> None:
        metadata = zone["metadata"]
        line = zone["line_number"]

        for key in metadata:
            if key not in self.ALLOWED_ZONE_KEYS:
                raise ValueError(
                    f"Line {line}: unknown zone metadata key '{key}'"
                    )

        zone_type = metadata.get("zone", "normal")
        if zone_type not in self.ALLOWED_ZONE_TYPES:
            raise ValueError(
                f"Line {line}: invalid zone type '{zone_type}'"
                )
        zone["zone_type"] = zone_type

        raw_max_drones = metadata.get("max_drones", "1")
        try:
            max_drones = int(raw_max_drones)
        except ValueError:
            raise ValueError(
                f"Line {line}: max_drones must be an integer"
                )
        if max_drones <= 0:
            raise ValueError(
                f"Line {line}: max_drones must be a positive integer"
                )
        zone["max_drones"] = max_drones

        zone["color"] = metadata.get("color", "none")

        zone.pop("metadata")

    def validate_connections(self) -> None:
        seen_connections: set[tuple[str, str]] = set()

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

            known_zones = {
                z["name"] for z in self.data["zones"]
                if z["line_number"] < line_number
            }

            if from_zone not in known_zones:
                raise ValueError(
                    f"Line {line_number}: unknown zone ({from_zone})"
                    )
            if to_zone not in known_zones:
                raise ValueError(
                    f"Line {line_number}: unknown zone ({to_zone})"
                    )
            if from_zone == to_zone:
                raise ValueError(
                    f"Line {line_number}: a zone cannot connect to itself"
                    )

            connection_key = tuple(sorted((from_zone, to_zone)))

            if connection_key in seen_connections:
                raise ValueError(
                    f"Line {line_number}: duplicate connection "
                    f"between ({from_zone}) and ({to_zone})"
                )
            seen_connections.add(connection_key)

            self.validate_connection_metadata(connection)

    def validate_connection_metadata(self, connection: dict) -> None:
        metadata = connection["metadata"]
        line = connection["line_number"]

        for key in metadata:
            if key not in self.ALLOWED_CONNECTION_KEYS:
                raise ValueError(
                    f"Line {line}: unknown connection metadata key '{key}'"
                    )

        raw_capacity = metadata.get("max_link_capacity", "1")
        try:
            capacity = int(raw_capacity)
        except ValueError:
            raise ValueError(
                f"Line {line}: max_link_capacity must be an integer"
                )
        if capacity <= 0:
            raise ValueError(
                f"Line {line}: max_link_capacity must be a positive integer"
                )
        connection["max_link_capacity"] = capacity
        connection.pop("metadata")
