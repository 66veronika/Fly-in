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
        name = set()
        start_hub = 0
        end_hub = 0

        
