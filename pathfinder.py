from collections import deque

from models.network import Network


class Pathfinder:
    def __init__(self, network: Network) -> None:
        self.network = network

    def find_path(self) -> list[str]:
        start = self.network.get_start_zone().name
        end = self.network.get_end_zone().name

        queue = deque([start])
        visited = {start}
        previous: dict[str, str | None] = {
            start: None
        }

        while queue:
            current = queue.popleft()

            if current == end:
                break

            for neighbor in self.network.neighbors(
                current,
                accessible_only=True,
            ):
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                previous[neighbor] = current
                queue.append(neighbor)

        if end not in visited:
            return []

        path: list[str] = []
        current: str | None = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return path
