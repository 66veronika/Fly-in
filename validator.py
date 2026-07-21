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

        if nb_drones