class Parser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.data = {
            "nb_drones": None,
            "zones": [],
            "connections": [],
        }

    def parse(self) -> dict:
        first_directive_seen = False
        with open(self.filepath, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if not first_directive_seen and not line.startswith(
                     "nb_drones:"):
                    raise ValueError(
                        f"Line {line_number}: "
                        "the first line must define nb_drones"
                    )
                first_directive_seen = True

                self.parse_line(line, line_number)
        return self.data

    def parse_line(self, line: str, line_number: int) -> None:
        if line.startswith("nb_drones:"):
            self.parse_nb_drones(line, line_number)
        elif line.startswith("start_hub:"):
            self.parse_zone(line, line_number)
        elif line.startswith("end_hub:"):
            self.parse_zone(line, line_number)
        elif line.startswith("hub:"):
            self.parse_zone(line, line_number)
        elif line.startswith("connection:"):
            self.parse_connection(line, line_number)
        else:
            raise ValueError(
                f"Line {line_number}: unknown line type"
                )

    def parse_nb_drones(self, line: str, line_number: int) -> None:
        part = line.split()

        if self.data["nb_drones"] is not None:
            raise ValueError(
                f"Line {line_number}: nb_drones already defined"
                )
        if len(part) < 2:
            raise ValueError(
                f"Line {line_number}: Missing number of drones"
                )
        elif len(part) > 2:
            raise ValueError(
                f"Line {line_number}: Too many drone arguments"
                )

        try:
            self.data["nb_drones"] = {
                "number": int(part[1]),
                "line_number": line_number,
            }
        except ValueError:
            raise ValueError(
                f"Line {line_number}: number of drones must be an integer"
                )

    def parse_zone(self, line: str, line_number: int) -> None:
        part = line.split()

        if len(part) < 4:
            raise ValueError(
                f"Line {line_number}: Missing zone arguments"
                )

        zone_type_prefix = part[0].removesuffix(":")
        metadata_raw = " ".join(part[4:])
        metadata = self.parse_metadata(metadata_raw, line_number)

        zone_data = {
            "type": zone_type_prefix,   # "start_hub" / "end_hub" / "hub"
            "name": part[1],
            "x": part[2],
            "y": part[3],
            "metadata": metadata,       # dict, ne string!
            "line_number": line_number,
        }
        self.data["zones"].append(zone_data)

    def parse_connection(self, line: str, line_number: int) -> None:
        part = line.split()

        if len(part) < 2:
            raise ValueError(
                f"Line {line_number}: Missing connections"
                )

        splitted_connections = part[1].split("-")

        if len(splitted_connections) != 2:
            raise ValueError(
                f"Line {line_number}: connection must have two zones"
                )

        metadata_raw = " ".join(part[2:])
        metadata = self.parse_metadata(metadata_raw, line_number)

        connection_data = {
            "from": splitted_connections[0],
            "to": splitted_connections[1],
            "metadata": metadata,
            "line_number": line_number,
        }
        self.data["connections"].append(connection_data)

    def parse_metadata(self, raw: str, line_number: int) -> dict[str, str]:
        """Parsuje '[key=value key2=value2]' na dict. Nevaliduje POVOLENÉ
        klíče/hodnoty - to je práce Validatoru, tady jen syntax."""
        raw = raw.strip()
        if not raw:
            return {}

        if not (raw.startswith("[") and raw.endswith("]")):
            raise ValueError(
                f"Line {line_number}: metadata must be enclosed in brackets"
            )

        inner = raw[1:-1].strip()
        if not inner:
            return {}

        metadata: dict[str, str] = {}
        for token in inner.split():
            if token.count("=") != 1:
                raise ValueError(
                    f"Line {line_number}: invalid metadata token '{token}'"
                    )

            key, _, value = token.partition("=")
            if not key or not value:
                raise ValueError(
                    f"Line {line_number}: invalid metadata token '{token}'"
                    )
            if key in metadata:
                raise ValueError(
                    f"Line {line_number}: duplicate metadata key '{key}'"
                    )

            metadata[key] = value

        return metadata
