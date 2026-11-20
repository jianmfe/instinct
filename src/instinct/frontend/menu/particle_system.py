
import math
import random

import pygame


class Particle:
    """Partícula luminosa que flota sobre el fondo."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.reset(initial=True)

    def reset(self, initial=False):
        self.x = random.uniform(0, self.width)

        if initial:
            self.y = random.uniform(0, self.height)
        else:
            self.y = self.height + random.uniform(5, 40)

        self.speed = random.uniform(12, 35)
        self.size = random.choice([1, 2, 2, 3])
        self.phase = random.uniform(0, math.tau)
        self.frequency = random.uniform(1.0, 3.0)

        self.color = random.choice([
            (212, 174, 98),
            (150, 119, 204),
            (190, 177, 220),
        ])

    def update(self, dt):
        self.y -= self.speed * dt
        self.phase += self.frequency * dt
        self.x += math.sin(self.phase) * 8 * dt

        if self.y < -5:
            self.reset()

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (
                int(self.x),
                int(self.y),
                self.size,
                self.size,
            ),
        )


class ParticleSystem:
    """Administra las partículas decorativas del menú."""

    def __init__(self, width, height, particle_count=45):
        self.width = width
        self.height = height

        self.particles = [
            Particle(width, height)
            for _ in range(particle_count)
        ]

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def resize(self, width, height):
        self.width = width
        self.height = height

        self.particles = [
            Particle(width, height)
            for _ in range(len(self.particles))
        ]
