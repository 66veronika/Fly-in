class Logger:
    """Save simulation output."""

    def __init__(
        self,
        output_file: str | None = None,
    ) -> None:
        """Initialize the logger with an optional output file."""
        self.output_file = output_file

        if self.output_file is not None:
            with open(
                self.output_file,
                "w",
                encoding="utf-8",
            ):
                pass

    def log(self, turn_output: str) -> None:
        """Print each turn with its moves and save it into a file."""
        print(turn_output)

        if self.output_file is not None:
            with open(
                self.output_file,
                "a",
                encoding="utf-8",
            ) as file:
                file.write(turn_output + "\n")
