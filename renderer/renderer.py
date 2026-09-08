import arcade

from models.network import Network
from algorithm import Schedule
from .zone_renderer import ZoneRenderer
from .drone_renderer import DroneRenderer


PADDING = 80
ZONE_RADIUS = 22


class Renderer(arcade.Window):
    """Display and animate the drone simulation."""

    def __init__(
        self,
        network: Network,
        schedules: list[Schedule],
    ) -> None:
        """Initialize the simulation window and renderer state."""
        screen_width, screen_height = arcade.get_display_size()

        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)

        super().__init__(
            window_width,
            window_height,
            "Fly-in",
            resizable=True,
            center_window=True,
        )

        self.network = network
        self.schedules = schedules

        self.current_turn = 0
        self.turn_progress = 0.0
        self.turn_duration = 0.7

        self.paused = False

        self.selected_zone: str | None = None

        self.max_turn = max(
            (
                schedule[-1][1]
                for schedule in self.schedules
            ),
            default=0,
        )

        self.zone_positions = self._calculate_zone_positions()
        self.zone_renderer = ZoneRenderer()
        self.drone_renderer = DroneRenderer()

        arcade.set_background_color(
            arcade.color.RUSSIAN_VIOLET
        )

    def _calculate_zone_positions(
        self,
    ) -> dict[str, tuple[float, float]]:
        """
        Convert map coordinates and
        turn them into screen coordinates (positions)
        """

        zones = list(self.network.zones.values())

        x_values = [zone.x for zone in zones]
        y_values = [zone.y for zone in zones]

        # min and max for full size of the map
        min_x = min(x_values)
        max_x = max(x_values)

        min_y = min(y_values)
        max_y = max(y_values)

        positions: dict[str, tuple[float, float]] = {}

        for zone in zones:
            if max_x == min_x:
                screen_x = self.width / 2
            else:
                screen_x = PADDING + (
                    (zone.x - min_x)
                    / (max_x - min_x)
                    * (self.width - 2 * PADDING)
                )

            if max_y == min_y:
                screen_y = self.height / 2
            else:
                screen_y = PADDING + (
                    (zone.y - min_y)
                    / (max_y - min_y)
                    * (self.height - 2 * PADDING)
                )

            positions[zone.name] = (
                screen_x,
                screen_y,
            )

        return positions

    def on_resize(
        self,
        width: int,
        height: int,
    ) -> None:
        """Recalculate zone positions when changing the size of the window."""
        self.zone_positions = (
            self._calculate_zone_positions()
        )

    def _delivered_drones(self) -> int:
        """Return the number of drones which reached End zone."""
        delivered = 0

        for schedule in self.schedules:
            arrival_turn = schedule[-1][1]

            if arrival_turn <= self.current_turn:
                delivered += 1

        return delivered

    def _drone_position(
        self,
        schedule: Schedule,
    ) -> tuple[float, float] | None:
        """
        Calculate a drone's screen position
        at the current simulation time.
        """
        simulation_time = (
            self.current_turn
            + self.turn_progress
        )

        final_turn = schedule[-1][1]

        if simulation_time >= final_turn:
            return None

        for i in range(len(schedule) - 1):
            zone_a, turn_a = schedule[i]
            zone_b, turn_b = schedule[i + 1]

            if turn_a <= simulation_time < turn_b:
                x1, y1 = self.zone_positions[zone_a]
                x2, y2 = self.zone_positions[zone_b]

                if zone_a == zone_b:
                    return x1, y1

                progress = (
                    simulation_time - turn_a
                ) / (turn_b - turn_a)

                x = x1 + (x2 - x1) * progress
                y = y1 + (y2 - y1) * progress

                return x, y

        return None

    def _draw_connections(self) -> None:
        """Draw all connections between zones."""
        for connection in self.network.connections:
            x1, y1 = self.zone_positions[
                connection.zone_a
            ]

            x2, y2 = self.zone_positions[
                connection.zone_b
            ]

            arcade.draw_line(
                x1,
                y1,
                x2,
                y2,
                arcade.color.GRAY,
                2,
            )

    def _draw_zones(self) -> None:
        """Draw all zones in the network."""
        for zone in self.network.zones.values():
            x, y = self.zone_positions[zone.name]

            is_selected = (zone.name == self.selected_zone)

            self.zone_renderer.draw_zone(zone, x, y, is_selected)

    def _draw_drones(self) -> None:
        """Draw all drones that are still in transit."""
        for drone_id, schedule in enumerate(
            self.schedules,
            start=1,
        ):
            position = self._drone_position(
                schedule
            )

            if position is None:
                continue

            x, y = position

            self.drone_renderer.draw_drone(
                x,
                y,
                drone_id,
            )

    def _draw_legend(self) -> None:
        """Draw the zone legend and keyboard controls."""
        arcade.draw_text(
            "○ Normal   ★ Priority   ▬ Restricted (2 turns)   X Blocked",
            20,
            40,
            arcade.color.WHITE,
            12,
        )

        arcade.draw_text(
            "SPACE: Pause/Resume   R: Restart   S: Skip",
            20,
            18,
            arcade.color.WHITE,
            12,
        )

    def _draw_completion_message(self) -> None:
        """Draw a completion message when all drones are delivered."""
        total = len(self.schedules)

        if total == 0:
            return

        if self._delivered_drones() != total:
            return

        center_x = self.width / 2
        center_y = self.height / 2

        arcade.draw_text(
            "ALL DRONES DELIVERED!",
            center_x,
            center_y + 30,
            arcade.color.CHAMPAGNE,
            45,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        arcade.draw_text(
            f"Completed in {self.max_turn} turns",
            center_x,
            center_y - 25,
            arcade.color.LIGHT_GREEN,
            16,
            anchor_x="center",
            anchor_y="center",
        )

    def on_draw(self) -> None:
        """Draw the current simulation frame."""
        self.clear()

        self._draw_connections()
        self._draw_zones()
        self._draw_drones()
        self._draw_legend()
        self._draw_status()
        self._draw_completion_message()

    def on_mouse_press(
        self,
        x: int,
        y: int,
        button: int,
        modifiers: int,
    ) -> None:
        """Handle mouse clicks and select a zone when the user clicks on it."""
        self.selected_zone = None

        click_radius = ZONE_RADIUS + 10

        for zone_name, position in self.zone_positions.items():
            zone_x, zone_y = position

            distance_x = x - zone_x
            distance_y = y - zone_y

            distance_squared = (
                distance_x * distance_x
                + distance_y * distance_y
            )

            if distance_squared <= click_radius * click_radius:
                self.selected_zone = zone_name
                return
        self.selected_zone = None

    def on_key_press(
        self,
        symbol: int,
        modifiers: int,
    ) -> None:
        """Handle simulation keyboard controls."""
        if symbol == arcade.key.SPACE:
            self.paused = not self.paused

        elif symbol == arcade.key.R:
            self.current_turn = 0
            self.turn_progress = 0.0
            self.paused = False

        elif symbol == arcade.key.S:
            self.current_turn = self.max_turn
            self.turn_progress = 0.0
            self.paused = True

        elif symbol == arcade.key.ESCAPE:
            self.selected_zone = None

    def _draw_status(self) -> None:
        """Draw the current simulation status."""
        delivered = self._delivered_drones()
        total = len(self.schedules)

        display_turn = min(
            self.current_turn + 1,
            self.max_turn,
        )

        if self.paused:
            state = "PAUSED"
        else:
            state = "RUNNING"

        arcade.draw_text(
            f"Drones: {total}",
            20,
            self.height - 35,
            arcade.color.WHITE,
            14,
        )

        arcade.draw_text(
            f"Delivered: {delivered}/{total}",
            20,
            self.height - 60,
            arcade.color.WHITE,
            14,
        )

        arcade.draw_text(
            f"Turn: {display_turn}/{self.max_turn}",
            20,
            self.height - 85,
            arcade.color.WHITE,
            14,
        )

        arcade.draw_text(
            state,
            20,
            self.height - 110,
            arcade.color.WHITE,
            14,
            bold=True,
        )

    def on_update(
        self,
        delta_time: float,
    ) -> None:
        """
        Advance the simulation based on elapsed time.
        A full turn is reached when turn_progress reaches 1.0.
        """
        if self.paused:
            return

        if self.current_turn >= self.max_turn:
            return

        self.turn_progress += (
            delta_time / self.turn_duration
        )

        if self.turn_progress >= 1.0:
            self.turn_progress = 0.0
            self.current_turn += 1

            if self.current_turn >= self.max_turn:
                self.current_turn = self.max_turn
                self.paused = True
