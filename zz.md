3. Then understand find_path_with_reservations() properly

This is the most important thing for you now.

Your algorithm can actually be explained pretty simply:

For each drone:

    start at:
    (start, turn 0)

            ↓

    use Dijkstra to explore possibilities:

    move
    OR
    wait

            ↓

    every possible state is:

    (zone, turn)

            ↓

    before moving, check:

    Is the connection free at those turns?
    Is the destination free on arrival?

            ↓

    choose earliest feasible arrival

    if equal:
    prefer priority zones

            ↓

    reserve that drone's schedule

            ↓

    plan the next drone

That's what I suggest we do next together: go through this function piece by piece, not just line-by-line mechanically.

For example, we'll start with:

start_state = (start, start_turn)

and answer:

Why isn't the state just "start"?

Because:

("A", turn 2)

and:

("A", turn 7)

are completely different situations. A might be occupied at turn 2 and empty at turn 7.

Then:

queue
best_rank
previous

We'll establish exactly what each one is doing and why you need it.

Then move to:

waiting
moving
reservations
priority tie-breaking
reconstruction

Once you understand that function, I think you'll feel much better about the 43-turn challenger result, because it won't feel like some mysterious algorithm sitting in your project.