#!/usr/bin/env python3
'''
Agency Fusion Network
Author: Abdelrahman Elbashandy - AR
'''

import argparse
import pygame
import random


MAX_DISTANCE = 40.0
COLOR_DISTANCE_RATIO = 30.0/(256+256+256)
NODE_RADIUS = 7

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

        reach = COLOR_DISTANCE_RATIO * (r + g + b)
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
    new_x = x + random.randint(-bx, bx)
    new_y = y + random.randint(-by, by)
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
    print("n1:", n1)
    print("n2:", n2)
    c1 = circles[n1]
    c2 = circles[n2]

    return (c1.reach + c2.reach) >= MAX_DISTANCE

def draw_edges(surface, circles):
    edges = {}
    for i, c1 in enumerate(circles):
        for j, c2 in enumerate(circles):
            if j <= i:
                continue
            if edge_id(i, j) not in edges and nodes_are_close(circles, i, j):
                pygame.draw.line(surface, (255, 255, 255), c1.coords(), c2.coords())
                edges[edge_id(i, j)] = 1

def main():
    pygame.init()

    info_object = pygame.display.Info()

    screen_w = int(info_object.current_w/2.5)
    screen_h = int(info_object.current_h/2.5)

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

    '''
    circles.append(NetworkCircle(
            screen_w/2+60,
            screen_h/2,
            (255, 255, 255),
            radius=NODE_RADIUS
        ))
    '''

    t = pygame.time.get_ticks()
    last_tick = t

    #pygame.mixer.music.load(audiofile)
    #pygame.mixer.music.play(0)

    # Run until the music finishes or let the user quits
    running = True
    while running:
        t = pygame.time.get_ticks()
        #delta_time = (t - last_tick) / 1000.0
        last_tick = t

        screen.fill((0, 0, 0))

        for c in circles:
            c.update()

        new_c = new_circle(circles[random.randint(0, len(circles) - 1)].coords())
        circles.append(new_c)

        draw_edges(screen, circles)

        for c in circles:
            c.render(screen)

        # update the full display surface to the screen
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Agency Fusion between Objects')
    main()
