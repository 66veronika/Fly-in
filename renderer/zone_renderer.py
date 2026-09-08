import math

import arcade

from models.enums import ZoneType
from models.zone import Zone

ZONE_RADIUS = 22


class ZoneRenderer:
    """Draw zones using their type (shape)."""

    def _resolve_color(
        self,
        color_name: str | None
    ) -> arcade.types.Color | None:
        """Recieve color name from map and turn it into Arcade color object."""
        if not color_name:
            return None

        attr_name = color_name.strip().upper()

        return getattr(arcade.color, attr_name, None) or getattr(
            arcade.csscolor, attr_name, None)

    def draw_zone(
            self,
            zone: Zone,
            x: float,
            y: float,
            is_selected: bool
    ) -> None:
        """Draw a zone based on its type"""
        color = self._resolve_color(zone.color)

        if zone.is_start:
            self._draw_circle(x, y, color, label="Start")
        elif zone.is_end:
            self._draw_circle(x, y, color, label="End")
        elif zone.zone_type == ZoneType.PRIORITY:
            self._draw_star(x, y, color)
        elif zone.zone_type == ZoneType.BLOCKED:
            self._draw_cross(x, y, color)
        elif zone.zone_type == ZoneType.RESTRICTED:
            self._draw_rectangle(x, y, color)
        else:
            self._draw_circle(x, y, color)

        if is_selected:
            self._draw_label(zone.name, x, y)

    def _draw_circle(
        self,
        x: float,
        y: float,
        color: arcade.types.Color | None,
        label: str | None = None,
    ) -> None:
        """Draw a normal zone (if label then Start or End zone)."""
        if color is not None:
            arcade.draw_circle_filled(x, y, ZONE_RADIUS, color)
        arcade.draw_circle_outline(x, y, ZONE_RADIUS, arcade.color.WHITE, 3)

        if label is not None:
            arcade.draw_text(
                label, x, y, arcade.color.WHITE, 10,
                anchor_x="center", anchor_y="center", bold=True,
            )

    def _draw_star(
            self,
            x: float,
            y: float,
            color: arcade.types.Color | None
    ) -> None:
        """Draw a priority zone."""
        outer, inner = ZONE_RADIUS + 5, ZONE_RADIUS / 2
        points = []
        for i in range(10):
            angle = math.radians(-90 + i * 36)
            radius = outer if i % 2 == 0 else inner
            points.append((
                x + math.cos(angle) * radius,
                y + math.sin(angle) * radius
                ))

        if color is not None:
            arcade.draw_polygon_filled(points, color)
        arcade.draw_polygon_outline(points, arcade.color.WHITE, 3)

    def _draw_cross(
            self,
            x: float,
            y: float,
            color: arcade.types.Color | None
    ) -> None:
        """Draw a blocked zone"""
        line_color = color if color is not None else arcade.color.WHITE
        size = ZONE_RADIUS
        arcade.draw_line(x - size, y - size, x + size, y + size, line_color, 5)
        arcade.draw_line(x - size, y + size, x + size, y - size, line_color, 5)

    def _draw_rectangle(
            self,
            x: float,
            y: float,
            color: arcade.types.Color | None
    ) -> None:
        """Draw a restricted zone."""
        rect = arcade.XYWH(x, y, ZONE_RADIUS * 2, ZONE_RADIUS * 1.3)
        if color is not None:
            arcade.draw_rect_filled(rect, color)
        arcade.draw_rect_outline(rect, arcade.color.WHITE, 3)
        arcade.draw_text(
            "2T", x, y, arcade.color.WHITE, 10,
            anchor_x="center", anchor_y="center", bold=True,
        )

    def _draw_label(self, name: str, x: float, y: float) -> None:
        """Draw a zone's name after being selected."""
        arcade.draw_text(
            name, x, y + ZONE_RADIUS + 15, arcade.color.WHITE, 13,
            anchor_x="center", bold=True,
        )
