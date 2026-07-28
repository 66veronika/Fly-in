from .connection import Connection


class Drone:
    def __init__(
            self,
            drone_id: int,
            current_zone: str,
    ) -> None:
        self.drone_id = drone_id
        self.current_zone = current_zone

        self.in_transit_connection: Connection | None = None
        self.destination_zone: str | None = None
        self.turns_remaining = 0

#    @property
#     def is_in_transit(self) -> bool:
#         return self.in_transit_connection is not None

#     def is_delivered(self, end_zone: str) -> bool:
#         return (
#             not self.is_in_transit
#             and self.current_zone == end_zone
#         )

#     def start_transit(
#         self,
#         connection: Connection,
#         destination_zone: str,
#         movement_cost: int,
#     ) -> None:
#         if self.is_in_transit:
#             raise ValueError(
#                 f"Drone {self.drone_id} is already in transit"
#             )

#         if movement_cost <= 0:
#             raise ValueError(
#                 "Movement cost must be positive"
#             )

#         self.in_transit_connection = connection
#         self.destination_zone = destination_zone
#         self.turns_remaining = movement_cost

#     def advance_transit(self) -> bool:
#         """
#         Advance the drone by one turn.

#         Returns True when the drone reaches its destination.
#         """
#         if not self.is_in_transit:
#             raise ValueError(
#                 f"Drone {self.drone_id} is not in transit"
#             )

#         self.turns_remaining -= 1

#         if self.turns_remaining > 0:
#             return False

#         if self.destination_zone is None:
#             raise RuntimeError(
#                 "Transit destination is missing"
#             )

#         self.current_zone = self.destination_zone
#         self.in_transit_connection = None
#         self.destination_zone = None
#         self.turns_remaining = 0

        # return True
