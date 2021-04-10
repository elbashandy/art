#!/usr/bin/env python3
'''
Agency Fusion Network
Author: Abdelrahman Elbashandy - AR
'''

import argparse
import pygame
import random
import math


WIDTH = 800
HEIGHT = 600
PADDING = 50
MAX_DISTANCE = 70.0
COLOR_DISTANCE_RATIO = MAX_DISTANCE/(256+256+256)
EXTRA_RATIO_FACTOR = 1
NODE_RADIUS = 7
REMOVE_CIRCLE_TURN = 2

class NetworkCircle:
    def __init__(self, x, y, color, radius=3):
        self.x, self.y = x, y
        self.color = color
        self.radius = radius

        self.reach = self.calculate_reach()

    def coords(self):
        return tuple((self.x, self.y))

    def calculate_reach(self):
        r, g, b = self.color

        reach = COLOR_DISTANCE_RATIO * (r + g + b) * EXTRA_RATIO_FACTOR
        #print("reach:", reach)
        return reach

    def update(self):
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        self.reach = self.calculate_reach()

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

def new_circle(coords: tuple, bounds: tuple = (80, 80)):
    x, y = coords
    bx, by = bounds
    new_x = min(max(x + random.randint(-bx, bx), 0 + PADDING), WIDTH - PADDING)
    new_y = min(max(y + random.randint(-by, by), 0 + PADDING), HEIGHT - PADDING)
    return NetworkCircle(
        new_x, new_y,
        (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ),
        radius=NODE_RADIUS
    )

def edge_id(n1, n2): return tuple(sorted((n1, n2)))

def nodes_are_close(circles, n1, n2):
    c1 = circles[n1]
    c2 = circles[n2]

    x1, y1 = c1.coords()
    x2, y2 = c2.coords()

    distance = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))

    return distance <= MAX_DISTANCE and (c1.reach + c2.reach) >= distance

def draw_edges(surface, circles):
    edges = {}
    for i, c1 in enumerate(circles):
        for j, c2 in enumerate(circles):
            if j <= i:
                continue
            if edge_id(i, j) not in edges and nodes_are_close(circles, i, j):
                pygame.draw.line(
                    surface,
                    (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    ),
                    c1.coords(),
                    c2.coords()
                )
                edges[edge_id(i, j)] = 1

def main():
    pygame.init()

    info_object = pygame.display.Info()

    #screen_w = int(info_object.current_w/2.5)
    #screen_h = int(info_object.current_h/2.5)

    screen_w = WIDTH
    screen_h = HEIGHT

    screen = pygame.display.set_mode([screen_w, screen_h])

    circles = []

#    for freq in frequencies:
    circles.append(
        NetworkCircle(
            screen_w/2,
            screen_h/2,
            (255, 255, 255),
            radius=NODE_RADIUS
        )
    )

    # Run until the music finishes or let the user quits
    running = True
    del_index = 0
    while running:
        screen.fill((0, 0, 0))

        for c in circles:
            c.update()

        draw_edges(screen, circles)

        for c in circles:
            c.render(screen)

        # update the full display surface to the screen
        pygame.display.flip()
        pygame.time.wait(200)

        new_c = new_circle(circles[random.randint(0, len(circles) - 1)].coords())
        circles.append(new_c)

        del_index += 1
        if del_index % REMOVE_CIRCLE_TURN == 0:
            del_index = 0
            del circles[random.randint(0, len(circles) - 1)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Agency Fusion between Objects')
    main()
