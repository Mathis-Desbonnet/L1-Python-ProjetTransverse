from math import sin, cos, sqrt, pi

def ySerieBasicJump(g: float, y: int, initialSpeed: int) -> float:
    """
    Returns the height 'u(n+1)' of the player
    """
    timeDelta = 1
    newSpeed = int(g * timeDelta + initialSpeed)
    y += int(-(1/2) * g * timeDelta + initialSpeed * timeDelta )
    return y, newSpeed

def defineSpeedWithAngle(angle: int, platformSpeed: int, initialYSpeedForBasicJump: int) -> tuple:
    """
    Returns the x speed and the y speed for a bumper jump
    """
    angle = angle * pi / 180
    return int(cos(angle) * platformSpeed), int(sin(angle) * platformSpeed)

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

print(defineSpeedWithAngle(80, 40, 10))
print(defineSpeedWithAngle(0, 40, 10))
print(defineSpeedWithAngle(45, 40, 10))
print(45*pi/180)