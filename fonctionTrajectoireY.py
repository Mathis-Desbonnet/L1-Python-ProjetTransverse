from math import sin, cos, pi, sqrt

def ySerieBasicJump(g: float, y: int, initialSpeed: int, timeDelta: int) -> tuple:
    """
    Returns the height 'u(n+1)' of the player
    """
    if timeDelta == 0:
        timeDelta = 1
    newSpeed = int(g * timeDelta + initialSpeed)
    y += int(-(1/2) * g * timeDelta + initialSpeed * timeDelta)
    return y, newSpeed

def defineSpeedWithAngle(angle: int, platformSpeed: int) -> tuple:
    """
    Returns the x initial speed and the y initial speed for a bumper jump
    """
    angle = angle * pi / 180
    return int(cos(angle) * platformSpeed), int(sin(angle) * platformSpeed)