import arcade


class DroneRenderer:
    def draw_drone(
        self,
        x: float,
        y: float,
        drone_id: int,
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

        arcade.draw_text(
            str(drone_id),
            x,
            y + 1,
            arcade.color.BLACK,
            7,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
