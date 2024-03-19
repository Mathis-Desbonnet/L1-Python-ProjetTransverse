def ySerieBasicJump(g: float, y: int, initialSpeed: int) -> float:
    """
    Returns the height 'u(n+1)' of the player
    """
    timeDelta = 1
    newSpeed = int(g * timeDelta + initialSpeed)
    y += int(-(1/2) * g * timeDelta + initialSpeed * timeDelta )
    return y, newSpeed



"""
g = 9.8
y = 1000
currentSpeed = -100
nextPlatformHeight = 1000
y = ySerieBasicJump(g, y, currentSpeed)[0]
print(y)
while y < nextPlatformHeight:
    y = ySerieBasicJump(g, y, currentSpeed)[0]
    currentSpeed = ySerieBasicJump(g, y, currentSpeed)[1]
    print(y)
"""
