
import pygame


class Panel:
    """Contenedor visual reutilizable."""

    def __init__(
        self,
        rect,
        background=(41, 39, 71),
        border_color=(118, 84, 168),
        border_width=2,
        radius=12,
    ):
        self.rect = pygame.Rect(rect)
        self.background = background
        self.border_color = border_color
        self.border_width = border_width
        self.radius = radius

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.background,
            self.rect,
            border_radius=self.radius,
        )

        if self.border_width > 0:
            pygame.draw.rect(
                surface,
                self.border_color,
                self.rect,
                width=self.border_width,
                border_radius=self.radius,
            )

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def set_size(self, width, height):
        self.rect.size = (width, height)
