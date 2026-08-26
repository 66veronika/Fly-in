import arcade


class DroneRenderer:
    def draw_drone(
        self,
        x: float,
        y: float,
    ) -> None:
        size = 9

        points = [
            (x - size, y - size / 2),
            (x, y - size / 2),
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x, y + size / 2),
            (x - size, y + size / 2),
        ]

        arcade.draw_polygon_filled(
            points,
            arcade.color.WHITE,
        )

        arcade.draw_polygon_outline(
            points,
            arcade.color.BLACK,
            2,
        )