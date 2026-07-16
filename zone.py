# properties:
# type - start_hub, end_hub, hub
# name, x / y (coordinates), type2 (restricted/normal/blocked/priority),
# max_drones

class Zone:
    def __init__(self, name: str, x: int, y: int) -> None:
        self.name = name
        self.x = x
        self.y = y
