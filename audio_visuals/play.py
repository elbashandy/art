#!/usr/bin/env python3
'''
Audio Visualizer
Author: Abdelrahman Elbashandy
'''

import librosa
import numpy as np
import pygame
import argparse
import random


class FreqCircle:
    def __init__(self, freq, x, y, color, min_radius=3, max_radius=100, min_decibel=-80, max_decibel=0):
        self.freq = freq
        self.x, self.y = x, y
        self.color = color
        self.min_radius, self.max_radius = min_radius, max_radius
        self.radius = min_radius
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.decibel_radius_ratio = (self.max_radius - self.min_radius)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):
        desired_radius = decibel * self.decibel_radius_ratio + self.max_radius
        speed = (desired_radius - self.radius)/0.07
        self.radius += speed * dt
        self.radius = clamp(self.min_radius, self.max_radius, self.radius)

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

    screen_w = int(infoObject.current_w/2.5)
    screen_h = int(infoObject.current_h/2.5)

    screen = pygame.display.set_mode([screen_w, screen_h])

    circles = []

    frequencies = np.arange(100, 11000, 100)

    freq_len = len(frequencies)

    width = screen_w/freq_len

    x = (screen_w - width*freq_len)/2

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
                ),
                max_radius=200
            )
        )
        x += width

    t = pygame.time.get_ticks()
    last_tick = t

    pygame.mixer.music.load(audiofile)
    pygame.mixer.music.play(0)

    # Run until the music finishes or let the user quits
    running = True
    while running:
        t = pygame.time.get_ticks()
        delta_time = (t - last_tick) / 1000.0
        last_tick = t

        screen.fill((255, 255, 255))

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
            c.render(screen)

        # update the full display surface to the screen
        pygame.display.flip()

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
