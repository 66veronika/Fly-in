from zone import Zone


class Parser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.nb_drones = 0

    def parse(self) -> None:
        with open(self.filepath, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                self.parse_line(line, line_number)

    def parse_line(self, line: str, line_number: int) -> None:
        if line.startswith("nb_drones:"):
            self.parse_nb_drones(line)
        elif line.startswith("start_hub:"):
            self.parse_zone(line)
        elif line.startswith("end_hub:"):
            self.parse_zone(line)
        elif line.startswith("hub:"):
            self.parse_zone(line)
        elif line.startswith("connection:"):
            self.parse_connection(line)
        else:
            raise ValueError(
                f"Line {line_number}: unknown line type"
            )

    def parse_nb_drones(self, line: str) -> None:
        part = line.split()
        if part < 2:
            raise ValueError(
                "Missing number of drones"
            )
        elif part > 2:
            raise ValueError(
                "Too many drone arguments"
            )
        self.nb_drones = int(part[1])

    def parse_zone(self, line: str) -> None:

    def parse_connection(self, line: str) -> None:
        print("niuushdi")

        

# zone = Zone(
#             name=part[1],
#             x=int(part[2]),
#             y=int(part[3]),
#         )