from models.network import Network
from algorithm import Schedule
from logger import Logger


class Simulator:
    """
    Converts precomputed drone schedules into turn-by-turn simulation output.
    Pathfinding and conflict resolution are handled before the simulation.
    """

    def __init__(
        self,
        network: Network,
        schedules: list[Schedule],
        logger: Logger
    ) -> None:
        """Initialize the simulator with network, schedules, and logger."""
        self.network = network
        self.schedules = schedules
        self.logger = logger

    def build_turn_events(self) -> list[list[str]]:
        """
        Build the drone movements that should be printed for each turn.
        Returns list of turns and each turn has a list of drone movements.
        """
        max_turn = 0
        for schedule in self.schedules:
            max_turn = max(max_turn, schedule[-1][1])

        events: list[list[str]] = [
            [] for _ in range(max_turn + 1)
        ]

        for drone_id, schedule in enumerate(self.schedules):
            for i in range(len(schedule) - 1):
                zone_a, turn_a = schedule[i]
                zone_b, turn_b = schedule[i + 1]

                if zone_a == zone_b:
                    continue  # waiting: drone does not move, omit from output

                duration = turn_b - turn_a

                if duration == 1:
                    events[turn_b].append(
                        f"D{drone_id + 1}-{zone_b}"
                    )
                else:
                    connection_name = f"{zone_a}-{zone_b}"

                    for mid_turn in range(
                        turn_a + 1,
                        turn_b,
                    ):
                        events[mid_turn].append(
                            f"D{drone_id + 1}-{connection_name}"
                        )

                    events[turn_b].append(
                        f"D{drone_id + 1}-{zone_b}"
                    )

        return events

    def run(self) -> None:
        """Run the simulation output turn by turn."""
        events = self.build_turn_events()

        for turn in range(1, len(events)):
            movements = events[turn]
            if movements:
                self.logger.log(
                    " ".join(movements)
                )
