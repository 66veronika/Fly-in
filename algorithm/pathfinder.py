import heapq

from models.enums import ZoneType
from models.network import Network
from models.zone import Zone
from .reservation import ReservationTable

# A "state" in the search is (zone_name, turn).
# A schedule is the list of states a single drone passes through.
Schedule = list[tuple[str, int]]


class Pathfinder:
    """Find reservation-safe paths for all drones in the network."""

    def __init__(self, network: Network) -> None:
        """Initialize the pathfinder with a network."""
        self.network = network

    def _effective_capacity(self, zone: Zone) -> int | float:
        """
        Return the allowed capacity of a zone.
        Start and end zones have unlimited capacity.
        """
        if zone.is_start or zone.is_end:
            return float("inf")
        return zone.max_drones

    def find_path_with_reservations(
        self,
        reservations: ReservationTable,
        start: str,
        end: str,
        start_turn: int = 0,
    ) -> Schedule:
        """Find a reservation-safe schedule from start to end."""
        max_turn = (
            reservations.latest_reserved_turn()
            + 1
            + 2 * (len(self.network.zones) - 1)
        )
        start_state = (start, start_turn)

        # (travel cost, priority rank, move count)
        best_rank: dict[
            tuple[str, int],
            tuple[int, int, int],
        ] = {
            start_state: (0, 1, 0)
        }

        # key = current state, value = previous state
        previous: dict[
            tuple[str, int],
            tuple[str, int],
        ] = {}

        # (cost, priority_rank, move count, zone_name, turn)
        queue: list[
            tuple[int, int, int, str, int]
        ] = [
            (0, 1, 0, start, start_turn)
        ]

        while queue:
            cost, priority_rank, move_count, zone_name, turn = (
                heapq.heappop(queue)
            )

            state = (zone_name, turn)

            current_rank = (
                cost,
                priority_rank,
                move_count,
            )

            known_rank = best_rank.get(state)

            if (
                known_rank is not None
                and current_rank > known_rank
            ):
                continue
            if zone_name == end:
                return self._reconstruct(previous, state)

            if turn >= max_turn:
                continue

            zone = self.network.get_zone(zone_name)
            zone_capacity = self._effective_capacity(zone)

            # wait in place
            wait_turn = turn + 1

            if reservations.zone_free(
                zone_name,
                zone_capacity,
                wait_turn,
            ):
                wait_state = (
                    zone_name,
                    wait_turn,
                )

                new_cost = cost + 1

                new_rank = (
                    new_cost,
                    priority_rank,
                    move_count,
                )

                if new_rank < best_rank.get(
                    wait_state,
                    (float("inf"), 0, float("inf")),
                ):
                    best_rank[wait_state] = new_rank
                    previous[wait_state] = state

                    heapq.heappush(
                        queue,
                        (
                            new_cost,
                            priority_rank,
                            move_count,
                            zone_name,
                            wait_turn,
                        ),
                    )
            # --- move to a neighbor ---
            for neighbor_name in self.network.neighbors(
                zone_name
            ):
                neighbor = self.network.get_zone(neighbor_name)
                new_priority_rank = priority_rank

                new_priority_rank = (
                    0
                    if neighbor.zone_type == ZoneType.PRIORITY
                    else 1
                )
                neighbor_capacity = self._effective_capacity(neighbor)
                connection = self.network.get_connection(
                    zone_name,
                    neighbor_name
                )
                if connection is None:
                    continue

                duration = neighbor.movement_cost()
                arrival_turn = turn + duration

                if not reservations.connection_free(
                    zone_name,
                    neighbor_name,
                    connection.max_link_capacity,
                    turn,
                    arrival_turn,
                ):
                    continue
                if not reservations.zone_free(
                    neighbor_name,
                    neighbor_capacity,
                    arrival_turn
                ):
                    continue

                new_state = (
                    neighbor_name,
                    arrival_turn,
                )

                new_cost = cost + duration

                new_move_count = move_count + 1

                new_rank = (
                    new_cost,
                    new_priority_rank,
                    new_move_count,
                )
                if new_rank < best_rank.get(
                    new_state,
                    (float("inf"), 0, float("inf")),
                ):
                    best_rank[new_state] = new_rank
                    previous[new_state] = state

                    heapq.heappush(
                        queue,
                        (
                            new_cost,
                            new_priority_rank,
                            new_move_count,
                            neighbor_name,
                            arrival_turn,
                        ),
                    )

        return []

    def _reconstruct(
        self,
        previous: dict[
            tuple[str, int],
            tuple[str, int],
        ],
        end_state: tuple[str, int],
    ) -> Schedule:
        """Reconstruct a schedule by following previous states."""
        path = [end_state]

        while path[-1] in previous:
            path.append(
                previous[path[-1]]
            )

        path.reverse()

        return path

    def plan_all_drones(
            self,
            nb_drones: int,
    ) -> list[Schedule]:
        """Plan and reserve a schedule for every drone."""

        reservations = ReservationTable()
        start = self.network.get_start_zone().name
        end = self.network.get_end_zone().name

        schedules: list[Schedule] = []
        for drone_id in range(nb_drones):
            schedule = self.find_path_with_reservations(
                reservations, start, end, start_turn=0
            )
            if not schedule:
                raise RuntimeError(
                    f"No feasible path found for drone {drone_id + 1}"
                )
            self._commit_schedule(reservations, schedule)
            schedules.append(schedule)
        return schedules

    def _commit_schedule(
            self,
            reservations: ReservationTable,
            schedule: Schedule
    ) -> None:
        """Reserve all zones and connections used by a schedule."""

        first_zone, first_turn = schedule[0]
        reservations.reserve_zone(first_zone, first_turn)
        for i in range(len(schedule) - 1):
            zone_a, turn_a = schedule[i]
            zone_b, turn_b = schedule[i + 1]
            if zone_a == zone_b:
                reservations.reserve_zone(zone_b, turn_b)
            else:
                reservations.reserve_connection(
                    zone_a,
                    zone_b,
                    turn_a,
                    turn_b,
                )
                reservations.reserve_zone(zone_b, turn_b)
