from parser import Parser


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

            if zone["name"] in names:
                raise ValueError(
                    f"Line {line}: duplicate zone name ({zone['name']})"
                )
            names.add(zone["name"])

            try:
                int(zone["x"])
                int(zone["y"])
            except ValueError:
                raise ValueError(
                    f"Line {line}: zone coordinates must be integers"
                )

            if zone["type"] == "start_hub":
                start_hubs += 1
            elif zone["type"] == "end_hub":
                end_hubs += 1

        if start_hubs != 1:
            raise ValueError(
                f"{line}: there must be only one start_hub"
            )
        elif end_hubs != 1:
            raise ValueError(
                f"{line}: there must be only one end_hub"
            )
