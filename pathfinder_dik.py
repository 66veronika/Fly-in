# import heapq
from models.network import Network


class Pathfinder:
    def __init__(self, network: Network) -> None:
        self.network = network

    def path_cost(self, path: list[str]) -> int:
        cost = 0

        for zone_name in path[1:]:
            zone = self.network.get_zone(zone_name)
            cost += zone.movement_cost()

        return cost

    def find_all_paths(self) -> list[list[str]]:
        start = self.network.get_start_zone().name
        end = self.network.get_end_zone().name

        paths: list[list[str]] = []

        self._search_paths(
            current=start,
            end=end,
            path=[start],
            visited={start},
            paths=paths,
        )

        paths.sort(key=self.path_cost)

        return paths

    def _search_paths(
        self,
        current: str,
        end: str,
        path: list[str],
        visited: set[str],
        paths: list[list[str]],
    ) -> None:
        if current == end:
            paths.append(path.copy())
            return

        for neighbor in self.network.neighbors(
            current,
            accessible_only=True,
        ):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            path.append(neighbor)

            self._search_paths(
                current=neighbor,
                end=end,
                path=path,
                visited=visited,
                paths=paths,
            )

            path.pop()
            visited.remove(neighbor)
    # def find_path(self) -> list[str]:
    #     start = self.network.get_start_zone().name
    #     end = self.network.get_end_zone().name

    #     distances: dict[str, int] = {
    #         zone_name: float("inf")
    #         for zone_name in self.network.zones
    #     }

    #     previous: dict[str, str | None] = {
    #         start: None
    #     }

    #     distances[start] = 0

    #     queue: list[tuple[int, str]] = [
    #         (0, start)
    #     ]

    #     while queue:
    #         current_distance, current = heapq.heappop(queue)

    #         if current == end:
    #             break

    #         if current_distance > distances[current]:
    #             continue

    #         for neighbor_name in self.network.neighbors(
    #             current,
    #             accessible_only=True,
    #         ):
    #             neighbor = self.network.zones[neighbor_name]

    #             new_distance = (
    #                 current_distance
    #                 + neighbor.movement_cost()
    #             )

    #             if new_distance < distances[neighbor_name]:
    #                 distances[neighbor_name] = new_distance
    #                 previous[neighbor_name] = current

    #                 heapq.heappush(
    #                     queue,
    #                     (
    #                         new_distance,
    #                         neighbor_name,
    #                     ),
    #                 )

    #     if distances[end] == float("inf"):
    #         return []

    #     path: list[str] = []
    #     current: str | None = end

    #     while current is not None:
    #         path.append(current)
    #         current = previous[current]

    #     path.reverse()

    #     return path
