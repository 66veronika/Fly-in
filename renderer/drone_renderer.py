import arcade


class DroneRenderer:
    """Draw drones with their numbers."""

    def draw_drone(
        self,
        x: float,
        y: float,
        drone_id: int,
    ) -> None:
        """Draw a drone at the given screen position."""
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
            y + 0.2,
            arcade.color.BLACK,
            6.5,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
