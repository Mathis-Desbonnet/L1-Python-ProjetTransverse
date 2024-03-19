def ySerieBasicJump(g: float, y: int, initialSpeed: int, timeDelta: int) -> float:
    """
    Returns the height 'u(n+1)' of the player
    """
    newSpeed = int(g * timeDelta + initialSpeed)
    y += int(-(1/2) * g * timeDelta + initialSpeed * timeDelta )
    return y, newSpeed