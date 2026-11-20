
import math
import random
from pathlib import Path

import pygame


class BackgroundRenderer:
    """
    Renderiza el fondo del menú principal.

    Si existe un PNG externo, lo utiliza.
    Si no existe, genera un paisaje provisional.
    """

    def __init__(self, size):
        self.width, self.height = size
        self.time = 0.0

        self.assets_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "backgrounds"
            / "main_menu"
            / "menu_background.png"
        )

        self.background = None
        self.stars = []

        self._load_background()

    def _load_background(self):
        """Carga el PNG o genera el fondo provisional."""

        if self.assets_path.is_file():
            try:
                self.background = pygame.image.load(
                    str(self.assets_path)
                ).convert()

                self.background = pygame.transform.smoothscale(
                    self.background,
                    (self.width, self.height),
                )

                print("Fondo del menú cargado correctamente.")
                return

            except (pygame.error, OSError) as error:
                print(f"Error al cargar el fondo: {error}")

        print("Usando fondo provisional.")
        self._generate_stars()
        self._build_background()

    def _generate_stars(self):
        rng = random.Random(42)

        for _ in range(100):
            self.stars.append({
                "x": rng.randint(0, self.width - 1),
                "y": rng.randint(0, int(self.height * 0.55)),
                "size": rng.choice([1, 1, 2, 2, 3]),
                "phase": rng.uniform(0, math.tau),
                "speed": rng.uniform(1.0, 3.0),
            })

    def _build_background(self):
        top_color = (12, 15, 38)
        bottom_color = (55, 39, 82)

        self.background = pygame.Surface(
            (self.width, self.height)
        )

        for y in range(self.height):
            ratio = y / max(1, self.height - 1)

            color = tuple(
                int(
                    top_color[i]
                    + (bottom_color[i] - top_color[i]) * ratio
                )
                for i in range(3)
            )

            pygame.draw.line(
                self.background,
                color,
                (0, y),
                (self.width, y),
            )

        moon_x = int(self.width * 0.78)
        moon_y = int(self.height * 0.19)
        moon_radius = max(18, int(self.height * 0.035))

        pygame.draw.circle(
            self.background,
            (222, 207, 173),
            (moon_x, moon_y),
            moon_radius,
        )

        pygame.draw.polygon(
            self.background,
            (42, 42, 76),
            [
                (0, int(self.height * 0.55)),
                (int(self.width * 0.15), int(self.height * 0.30)),
                (int(self.width * 0.28), int(self.height * 0.52)),
                (int(self.width * 0.43), int(self.height * 0.34)),
                (int(self.width * 0.60), int(self.height * 0.56)),
                (int(self.width * 0.78), int(self.height * 0.32)),
                (self.width, int(self.height * 0.55)),
                (self.width, self.height),
                (0, self.height),
            ],
        )

        pygame.draw.polygon(
            self.background,
            (34, 38, 65),
            [
                (0, int(self.height * 0.68)),
                (int(self.width * 0.20), int(self.height * 0.48)),
                (int(self.width * 0.38), int(self.height * 0.66)),
                (int(self.width * 0.58), int(self.height * 0.45)),
                (int(self.width * 0.78), int(self.height * 0.67)),
                (self.width, int(self.height * 0.48)),
                (self.width, self.height),
                (0, self.height),
            ],
        )

        pygame.draw.rect(
            self.background,
            (20, 37, 42),
            (
                0,
                int(self.height * 0.83),
                self.width,
                self.height,
            ),
        )

    def update(self, dt):
        self.time += dt

    def draw(self, screen):
        if self.background.get_size() != screen.get_size():
            self.resize(screen.get_size())

        screen.blit(self.background, (0, 0))

        # Las estrellas solo se dibujan en el fondo provisional.
        if self.stars:
            for star in self.stars:
                brightness = (
                    math.sin(
                        self.time * star["speed"] + star["phase"]
                    ) + 1
                ) / 2

                intensity = int(130 + brightness * 125)

                color = (
                    intensity,
                    int(intensity * 0.91),
                    int(intensity * 0.72),
                )

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        star["x"],
                        star["y"],
                        star["size"],
                        star["size"],
                    ),
                )

    def resize(self, size):
        """Adapta el fondo al tamaño actual de la ventana."""

        self.width, self.height = size

        if self.assets_path.is_file():
            try:
                original = pygame.image.load(
                    str(self.assets_path)
                ).convert()

                self.background = pygame.transform.smoothscale(
                    original,
                    size,
                )

                self.stars = []
                return

            except (pygame.error, OSError):
                pass

        self.stars = []
        self._generate_stars()
        self._build_background()
