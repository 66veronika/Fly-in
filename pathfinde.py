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

    def assign_paths(
        self,
        paths: list[list[str]],
        nb_drones: int,
    ) -> list[list[str]]:

        if not paths:
            raise RuntimeError(
                "Cannot assign drones: no paths available"
            )

        assignments: list[list[str]] = []

        zone_loads: dict[str, int] = {
            zone_name: 0
            for zone_name in self.network.zones
        }

        connection_loads: dict[tuple[str, str], int] = {}

        for connection in self.network.connections:
            key = tuple(sorted((
                connection.zone_a,
                connection.zone_b,
            )))
            connection_loads[key] = 0

        for _ in range(nb_drones):
            best_index = 0

            best_score = (
                self.path_cost(paths[0])
                + self.path_congestion(
                    paths[0],
                    zone_loads,
                    connection_loads,
                )
            )

            for index in range(1, len(paths)):
                score = (
                    self.path_cost(paths[index])
                    + self.path_congestion(
                        paths[index],
                        zone_loads,
                        connection_loads,
                    )
                )

                if score < best_score:
                    best_score = score
                    best_index = index

            chosen_path = paths[best_index]
            assignments.append(chosen_path)

            for zone_name in chosen_path[1:-1]:
                zone_loads[zone_name] += 1

            for index in range(len(chosen_path) - 1):
                key = tuple(sorted((
                    chosen_path[index],
                    chosen_path[index + 1],
                )))
                connection_loads[key] += 1

        return assignments

    def path_congestion(
        self,
        path: list[str],
        zone_loads: dict[str, int],
        connection_loads: dict[tuple[str, str], int],
    ) -> float:
        worst_congestion = 0.0

        for zone_name in path[1:-1]:
            zone = self.network.get_zone(zone_name)

            congestion = (
                zone_loads[zone_name] + 1
            ) / zone.max_drones

            worst_congestion = max(
                worst_congestion,
                congestion,
            )

        for index in range(len(path) - 1):
            zone_a = path[index]
            zone_b = path[index + 1]

            connection = self.network.get_connection(
                zone_a,
                zone_b,
            )

            if connection is None:
                raise RuntimeError(
                    "Path contains zones that are not connected"
                )

            key = tuple(sorted((zone_a, zone_b)))

            congestion = (
                connection_loads[key] + 1
            ) / connection.max_link_capacity

            worst_congestion = max(
                worst_congestion,
                congestion,
            )

        return worst_congestion

    def path_bottleneck_capacity(
        self,
        path: list[str],
    ) -> int:
        capacities: list[int] = []

        for index in range(len(path) - 1):
            connection = self.network.get_connection(
                path[index],
                path[index + 1],
            )

            if connection is None:
                raise RuntimeError(
                    "Path contains zones that are not connected"
                )

            capacities.append(
                connection.max_link_capacity
            )

        for zone_name in path[1:-1]:
            zone = self.network.get_zone(zone_name)
            capacities.append(zone.max_drones)

        return min(capacities)

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
