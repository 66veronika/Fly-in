import heapq

from models.network import Network


class Pathfinder:
    def __init__(self, network: Network) -> None:
        self.network = network

    def find_path(self) -> list[str]:
        start = self.network.get_start_zone().name
        end = self.network.get_end_zone().name

        distances: dict[str, int] = {
            zone_name: float("inf")
            for zone_name in self.network.zones
        }

        previous: dict[str, str | None] = {
            start: None
        }

        distances[start] = 0

        queue: list[tuple[int, str]] = [
            (0, start)
        ]

        while queue:
            current_distance, current = heapq.heappop(queue)

            if current == end:
                break

            if current_distance > distances[current]:
                continue

            for neighbor_name in self.network.neighbors(
                current,
                accessible_only=True,
            ):
                neighbor = self.network.zones[neighbor_name]

                new_distance = (
                    current_distance
                    + neighbor.movement_cost()
                )

                if new_distance < distances[neighbor_name]:
                    distances[neighbor_name] = new_distance
                    previous[neighbor_name] = current

                    heapq.heappush(
                        queue,
                        (
                            new_distance,
                            neighbor_name,
                        ),
                    )

        if distances[end] == float("inf"):
            return []

        path: list[str] = []
        current: str | None = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return path
