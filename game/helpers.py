
def is_adjacent(a, b):
    """
    Checks that two positions are adjacent.
    Diagonal counts as adjacent.

    Args:
        - a (tuple[int, int]):
            One of the positions
        - b (tuple[int, int]):
            The other position

    Returns:
        - boolean:
            True if they are adjacent
            False if not
    """
    (ax, ay) = a
    (bx, by) = b
    dx = abs(bx - ax)
    dy = abs(by - ay)

    return dx <= 1 and dy <= 1
