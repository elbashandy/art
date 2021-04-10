import sys
import pygame
import math
from pygame.locals import *

WIDTH = 800
HEIGHT = 600

BLACK = Color(0, 0, 0)
BLUE = Color(0, 0, 200)
LIGHT_BLUE = Color(30, 30, 230)
LIGHTER_BLUE = Color(80, 80, 245)
BROWN = Color(100, 70, 50)

TWO_PI = 2.0 * math.pi

WATER_START_X = 300
WATER_WIDTH = 200
WATER_BOX_START_Y = 300
WATER_BOX_HEIGHT = 200
AMPLITUDE = 5
WAVE_OFFSET_INCREMENT = 2.0

BASE_Y = WATER_BOX_START_Y - (2 * AMPLITUDE)

CONTAINER_POINTS = ((WATER_START_X - 6, WATER_BOX_START_Y - 30), \
	(WATER_START_X - 6, WATER_BOX_START_Y + WATER_BOX_HEIGHT + 4), \
	(WATER_START_X + 4 + WATER_WIDTH, WATER_BOX_START_Y + WATER_BOX_HEIGHT + 4), \
	(WATER_START_X + 4 + WATER_WIDTH, WATER_BOX_START_Y - 30))

WATER_BOX_RECT = Rect(WATER_START_X, WATER_BOX_START_Y, WATER_WIDTH, WATER_BOX_HEIGHT)


def handleEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
			sys.exit()

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
offset = 0.0

while 1:
	handleEvents()

	screen.fill(BLACK)
	pygame.draw.lines(screen, BROWN, False, CONTAINER_POINTS, 10)
	pygame.draw.rect(screen, BLUE, WATER_BOX_RECT)

	for i in range(WATER_WIDTH):
		pixelX = i + WATER_START_X

		rad = ((float(i) + offset) / 90.0) * TWO_PI
		mod = math.sin(rad) * AMPLITUDE
		pixelY = round(BASE_Y + mod)
		pygame.draw.line(screen, BLUE, (pixelX, pixelY + 7), (pixelX, WATER_BOX_START_Y), 1)
		pygame.draw.line(screen, LIGHT_BLUE, (pixelX, pixelY + 3), (pixelX, pixelY + 6), 2)
		pygame.draw.line(screen, LIGHTER_BLUE, (pixelX, pixelY), (pixelX, pixelY + 2), 2)

	offset += WAVE_OFFSET_INCREMENT
	if offset > 90.0:
		offset -= 90.0

	pygame.display.flip()
	pygame.time.wait(10)
