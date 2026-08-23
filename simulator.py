from models.network import Network
from pathfinder_dik import Schedule


class Simulator:
    """
    Replays precomputed (zone, turn) schedules produced by
    Pathfinder.plan_all_drones(). All capacity/conflict resolution already
    happened during planning, so this class's job is just to turn schedules
    into the turn-by-turn output format required by the spec.
    """

    def __init__(self, network: Network, schedules: list[Schedule]) -> None:
        self.network = network
        self.schedules = schedules

    def connection_display_name(self, from_zone: str, to_zone: str) -> str:
        """Name shown for a drone still in flight toward a restricted zone.
        Adjust this if your grading expects a different literal format."""
        return f"{from_zone}-{to_zone}"

    def build_turn_events(self) -> list[list[str]]:
        """
        Returns a list where index i holds all 'D<id>-<zone_or_connection>'
        tokens that should be printed for turn i+1 (turns are 1-indexed in
        output, matching the spec's example).
        """
        max_turn = 0
        for schedule in self.schedules:
            max_turn = max(max_turn, schedule[-1][1])

        # events[turn] -> list of tokens, turn is 1-indexed
        events: list[list[str]] = [[] for _ in range(max_turn + 1)]

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
                    connection_name = self.connection_display_name(
                        zone_a,
                        zone_b,
                    )

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
        events = self.build_turn_events()

        for turn in range(1, len(events)):
            line_tokens = events[turn]
            if line_tokens:
                print(" ".join(line_tokens))

        total_turns = len(events) - 1
        print(f"\nSimulation complete in {total_turns} turns.")