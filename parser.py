
class Parser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

        self.data = {
            "nb_drones": None,
            "zones": [],
            "connections": [],
        }

    def parse(self) -> dict:
        with open(self.filepath, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

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
                "line_number": line_number
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
        if len(part) > 5:
            raise ValueError(
                f"Line {line_number}: Too many zone arguments"
            )
        zone_type = part[0].removesuffix(":")
        metadata_arg = " ".join(part[4:])

        zone_data = {
            "type": zone_type,
            "name": part[1],
            "x": part[2],
            "y": part[3],
            "metadata": metadata_arg,
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

        from_zone = splitted_connections[0]
        to_zone = splitted_connections[1]
        metadata_arg = " ".join(part[2:])
        connection_data = {
            "from": from_zone,
            "to": to_zone,
            "metadata": metadata_arg,
            "line_number": line_number,
        }
        self.data["connections"].append(connection_data)

