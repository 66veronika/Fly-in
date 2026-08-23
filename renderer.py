class TerminalRenderer:
    def render(
        self,
        events: list[list[str]],
    ) -> None:
        for turn in range(1, len(events)):
            movements = events[turn]

            if movements:
                print(" ".join(movements))