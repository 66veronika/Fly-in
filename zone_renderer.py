import math
import arcade

from models.enums import ZoneType
from models.zone import Zone

ZONE_RADIUS = 22


class ZoneRenderer:
    def draw_zone(
        self,
        zone: Zone,
        x: float,
        y: float,
        start_color: tuple[int, int, int],
        end_color: tuple[int, int, int],
        is_occupied: bool,
    ) -> None:
        if zone.is_start:
            self._draw_start(
                x,
                y,
                start_color,
            )
            return

        if zone.is_end:
            self._draw_end(
                x,
                y,
                end_color,
            )
            return

        if zone.zone_type == ZoneType.PRIORITY:
            self._draw_star(x, y, is_occupied)

        elif zone.zone_type == ZoneType.BLOCKED:
            self._draw_blocked(x, y)

        elif zone.zone_type == ZoneType.RESTRICTED:
            self._draw_restricted(x, y, is_occupied)

        else:
            self._draw_normal(x, y, is_occupied)

    def _draw_start(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int]
    ) -> None:

        arcade.draw_circle_filled(
            x,
            y,
            ZONE_RADIUS + 5,
            color,
        )
        arcade.draw_circle_outline(
            x,
            y,
            ZONE_RADIUS + 5,
            arcade.color.WHITE,
            3,
        )

        arcade.draw_text(
            "Start",
            x,
            y,
            arcade.color.BLACK,
            14,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def _draw_end(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
    ) -> None:

        arcade.draw_circle_filled(
            x,
            y,
            ZONE_RADIUS + 5,
            color,
        )

        arcade.draw_circle_outline(
            x,
            y,
            ZONE_RADIUS + 5,
            arcade.color.WHITE,
            3,
        )

        arcade.draw_text(
            "End",
            x,
            y,
            arcade.color.BLACK,
            14,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def _draw_normal(
        self,
        x: float,
        y: float,
        is_occupied: bool,
    ) -> None:

        if is_occupied:
            color = arcade.color.AFRICAN_VIOLET
        else:
            color = arcade.color.SOAP

        arcade.draw_circle_filled(
            x,
            y,
            ZONE_RADIUS,
            color,
        )
        arcade.draw_circle_outline(
            x,
            y,
            ZONE_RADIUS,
            arcade.color.WHITE,
            3,
        )
    
    def _draw_blocked(
        self,
        x: float,
        y: float,
    ) -> None:
        size = ZONE_RADIUS

        arcade.draw_line(
            x - size,
            y - size,
            x + size,
            y + size,
            arcade.color.RED,
            5,
        )

        arcade.draw_line(
            x - size,
            y + size,
            x + size,
            y - size,
            arcade.color.RED,
            5,
        )
    
    def _draw_restricted(
        self,
        x: float,
        y: float,
        is_occupied: bool,
    ) -> None:

        if is_occupied:
            color = arcade.color.BULGARIAN_ROSE
        else:
            color = arcade.color.BURGUNDY

        width = ZONE_RADIUS * 1.8
        height = ZONE_RADIUS * 1.2

        arcade.draw_rect_filled(
            arcade.XYWH(
                x,
                y,
                width,
                height,
            ),
            color,
        )

        arcade.draw_rect_outline(
            arcade.XYWH(
                x,
                y,
                width,
                height,
            ),
            arcade.color.WHITE,
            3,
        )

    def _draw_star(
        self,
        x: float,
        y: float,
        is_occupied: bool,
    ) -> None:

        if is_occupied:
            color = arcade.color.FUZZY_WUZZY
        else:
            color = arcade.color.CAMEO_PINK

        points: list[tuple[float, float]] = []

        outer_radius = ZONE_RADIUS + 5
        inner_radius = ZONE_RADIUS / 2.5

        for i in range(10):
            angle = math.radians(
                -90 + i * 36
            )

            if i % 2 == 0:
                radius = outer_radius
            else:
                radius = inner_radius

            point_x = x + math.cos(angle) * radius
            point_y = y + math.sin(angle) * radius

            points.append(
                (
                    point_x,
                    point_y,
                )
            )

        arcade.draw_polygon_filled(
            points,
            color,
        )

        arcade.draw_polygon_outline(
            points,
            arcade.color.WHITE,
            3,
        )
