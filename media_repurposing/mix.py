#!/usr/bin/env python3
'''
Audio Visualizer
Author: Abdelrahman Elbashandy
'''

import librosa
import numpy as np
import math
import pygame
import argparse
import random

WIDTH = 800
HEIGHT = 600
PADDING = 50
MAX_DISTANCE = 70.0
MIN_RADIUS = 3
MAX_RADIUS = 25
DECIBEL_SPEED = 0.03
COLOR_DISTANCE_RATIO = MAX_DISTANCE/(256+256+256)
EXTRA_RATIO_FACTOR = 1
REMOVE_CIRCLE_TURN = 2

class FreqCircle:
    def __init__(self, freq, x, y, color, min_radius=MIN_RADIUS, max_radius=MAX_RADIUS, min_decibel=-80, max_decibel=0):
        self.freq = freq
        self.x, self.y = x, y
        self.color = color
        self.min_radius, self.max_radius = min_radius, max_radius
        self.radius = min_radius
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.decibel_radius_ratio = (self.max_radius - self.min_radius)/(self.max_decibel - self.min_decibel)

        # From agency_fusion/life.py
        self.reach = self.calculate_reach()

    def coords(self):
        return tuple((self.x, self.y))

    def update(self, dt, decibel):
        desired_radius = decibel * self.decibel_radius_ratio + self.max_radius
        speed = (desired_radius - self.radius) / DECIBEL_SPEED
        self.radius += speed * dt
        self.radius = clamp(self.min_radius, self.max_radius, self.radius)

        self.reach = self.calculate_reach()

    def update_ontology(self, bounds: tuple = (80, 80)):
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        #bx, by = bounds
        #self.x = min(max(self.x + random.randint(-bx, bx), 0 + PADDING), WIDTH - PADDING)
        #self.y = min(max(self.y + random.randint(-by, by), 0 + PADDING), HEIGHT - PADDING)

        self.x = min(max(random.randint(0, WIDTH), 0 + PADDING), WIDTH - PADDING)
        self.y = min(max(random.randint(0, HEIGHT), 0 + PADDING), HEIGHT - PADDING)

    def calculate_reach(self):
        r, g, b = self.color

        reach = COLOR_DISTANCE_RATIO * (r + g + b + self.radius) * EXTRA_RATIO_FACTOR
        #print("reach:", reach)
        return reach

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def clamp(min_value, max_value, value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value

    return value

def get_decibel(spectrogram, freq, frequencies_index_ratio, target_time, time_index_ratio):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]

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


def main(audiofile):
    fft_window_size = 2048

    time_series, sample_rate = librosa.load(audiofile)

    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=fft_window_size))
    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
    frequencies = librosa.core.fft_frequencies(n_fft=fft_window_size)
    times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=fft_window_size)

    time_index_ratio = len(times)/times[len(times) - 1]
    frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

    pygame.init()

    infoObject = pygame.display.Info()

    #screen_w = int(infoObject.current_w/2.5)
    #screen_h = int(infoObject.current_h/2.5)

    screen_w = WIDTH
    screen_h = HEIGHT

    screen = pygame.display.set_mode([screen_w, screen_h])

    frequencies = np.arange(100, 11000, 100)

    freq_len = len(frequencies)

    width = screen_w/freq_len

    # x = 0, unless there's subscreen in the middle of the main screen
    x = (screen_w - width*freq_len)/2

    circles = []
    for freq in frequencies:
        circles.append(
            FreqCircle(
                freq,
                random.randint(0, screen_w),
                random.randint(0, screen_h),
                (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            )
        )
        x += width

    t = pygame.time.get_ticks()
    last_tick = t

    pygame.mixer.music.load(audiofile)
    pygame.mixer.music.play()

    # Run until the music finishes or let the user quits
    del_index = 0
    running = True
    while running:
        t = pygame.time.get_ticks()
        delta_time = (t - last_tick) / 1000.0
        last_tick = t

        screen.fill((0, 0, 0))

        for c in circles:
            c.update(
                delta_time,
                get_decibel(
                    spectrogram,
                    c.freq,
                    frequencies_index_ratio,
                    pygame.mixer.music.get_pos()/1000.0,
                    time_index_ratio
                )
            )

        draw_edges(screen, circles)

        for c in circles:
            c.render(screen)

        # update the full display surface to the screen
        pygame.display.flip()

        del_index += 1
        if del_index % REMOVE_CIRCLE_TURN == 0:
            del_index = 0
            circles[random.randint(0, len(circles) - 1)].update_ontology()

        if not pygame.mixer.music.get_busy():
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize your audio')
    parser.add_argument('--audio',
                            help='audio filepath chosen for visualization')

    args = parser.parse_args()
    main(args.audio)
