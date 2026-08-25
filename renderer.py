import arcade

from models.network import Network
from pathfinder_dik import Schedule

ZONE_COLORS = {
    "normal": arcade.color.BLUE_YONDER,
    "priority": arcade.color.EMERALD,
    "restricted": arcade.color.RED_ORANGE,
    "blocked": arcade.color.GRAY,
}
START_COLOR = arcade.color.SUNGLOW
END_COLOR = arcade.color.AMETHYST
DRONE_COLOR = arcade.color.DARK_SLATE_GRAY
CONNECTION_COLOR = arcade.color.LIGHT_GRAY

ZONE_RADIUS = 22
DRONE_RADIUS = 7
MARGIN = 60
SCREEN_W = 900
SCREEN_H = 650


class Renderer(arcade.Window):
    def __init__(self, network: Network, schedules: list[Schedule]) -> None:
        super().__init__(SCREEN_W, SCREEN_H, "Fly-in Simulation")
        arcade.set_background_color(arcade.color.WHITE)

        self.network = network
        self.schedules = schedules
        self.max_turn = max(schedule[-1][1] for schedule in schedules)
        self.current_turn: float = 0
        self.playing = False
        self.time_since_last_step = 0.0
        self.step_interval = 0.6  # seconds per turn during autoplay

        self.positions = self._compute_layout()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _compute_layout(self) -> dict[str, tuple[float, float]]:
        """Scales raw zone.x/zone.y coordinates to screen pixel positions."""
        zones = list(self.network.zones.values())
        xs = [z.x for z in zones]
        ys = [z.y for z in zones]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)

        usable_w = SCREEN_W - 2 * MARGIN
        usable_h = SCREEN_H - 2 * MARGIN - 40  # leave room for UI text at top

        positions: dict[str, tuple[float, float]] = {}
        for zone in zones:
            norm_x = (zone.x - min_x) / span_x
            norm_y = (zone.y - min_y) / span_y
            px = MARGIN + norm_x * usable_w
            py = MARGIN + norm_y * usable_h  # arcade y-axis points up already
            positions[zone.name] = (px, py)

        return positions

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def on_draw(self) -> None:
        self.clear()
        self._draw_connections()
        self._draw_zones()
        self._draw_drones()
        self._draw_ui()

    def _draw_connections(self) -> None:
        for connection in self.network.connections:
            x1, y1 = self.positions[connection.zone_a]
            x2, y2 = self.positions[connection.zone_b]
            arcade.draw_line(x1, y1, x2, y2, CONNECTION_COLOR, 2)

            if connection.max_link_capacity > 1:
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                arcade.draw_text(
                    f"x{connection.max_link_capacity}",
                    mid_x, mid_y, arcade.color.GRAY, 9,
                    anchor_x="center", anchor_y="center",
                )

    def _draw_zones(self) -> None:
        for zone in self.network.zones.values():
            x, y = self.positions[zone.name]

            # soft shadow
            arcade.draw_circle_filled(x + 2, y - 4, ZONE_RADIUS, (0, 0, 0, 40))

            fill = ZONE_COLORS.get(zone.zone_type.value, arcade.color.BLUE_YONDER)
            if zone.is_start:
                fill = START_COLOR
            if zone.is_end:
                fill = END_COLOR

            arcade.draw_circle_filled(x, y, ZONE_RADIUS, fill)
            arcade.draw_circle_outline(x, y, ZONE_RADIUS, arcade.color.DARK_SLATE_GRAY, 2)

            arcade.draw_text(
                zone.name, x, y - ZONE_RADIUS - 16,
                arcade.color.DARK_SLATE_GRAY, 11, bold=True,
                anchor_x="center",
            )

            if zone.max_drones != 1 and not zone.is_start and not zone.is_end:
                arcade.draw_text(
                    str(zone.max_drones), x, y,
                    arcade.color.WHITE, 10,
                    anchor_x="center", anchor_y="center",
                )

    def _draw_ui(self) -> None:
        arcade.draw_text(
            f"Turn: {int(self.current_turn)} / {self.max_turn}"
            f"   [SPACE: play/pause]  [\u2190/\u2192: step]",
            10, SCREEN_H - 25,
            arcade.color.DARK_SLATE_GRAY, 13, bold=True,
        )

    # ------------------------------------------------------------------
    # Drone position lookup (same interpolation logic as before)
    # ------------------------------------------------------------------

    def _drone_position_at_turn(
        self, schedule: Schedule, turn: float
    ) -> tuple[float, float] | None:
        """
        Returns the interpolated pixel position of a drone at a given turn,
        or None if the drone has already been delivered.
        """
        if turn >= schedule[-1][1]:
            return None  # delivered, don't draw

        if turn <= schedule[0][1]:
            zone_name, _ = schedule[0]
            return self.positions[zone_name]

        for i in range(len(schedule) - 1):
            zone_a, turn_a = schedule[i]
            zone_b, turn_b = schedule[i + 1]

            if turn_a <= turn <= turn_b:
                if zone_a == zone_b or turn_b == turn_a:
                    return self.positions[zone_a]

                fraction = (turn - turn_a) / (turn_b - turn_a)
                x1, y1 = self.positions[zone_a]
                x2, y2 = self.positions[zone_b]
                x = x1 + (x2 - x1) * fraction
                y = y1 + (y2 - y1) * fraction
                return (x, y)

        return None

    def _draw_drones(self) -> None:
        for drone_id, schedule in enumerate(self.schedules):
            pos = self._drone_position_at_turn(schedule, self.current_turn)
            if pos is None:
                continue
            x, y = pos
            arcade.draw_circle_filled(x, y, DRONE_RADIUS, DRONE_COLOR)
            arcade.draw_circle_outline(x, y, DRONE_RADIUS, arcade.color.WHITE, 1)

    # ------------------------------------------------------------------
    # Input / playback
    # ------------------------------------------------------------------

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.SPACE:
            self.playing = not self.playing
        elif key == arcade.key.RIGHT:
            self.playing = False
            self.current_turn = min(self.current_turn + 1, self.max_turn)
        elif key == arcade.key.LEFT:
            self.playing = False
            self.current_turn = max(self.current_turn - 1, 0)

    def on_update(self, delta_time: float) -> None:
        if not self.playing:
            return

        self.time_since_last_step += delta_time
        if self.time_since_last_step >= self.step_interval:
            self.time_since_last_step = 0.0
            if self.current_turn < self.max_turn:
                self.current_turn += 1
            else:
                self.playing = False