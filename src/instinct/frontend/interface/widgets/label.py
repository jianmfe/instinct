
import pygame


class Label:
    """Componente de texto reutilizable."""

    def __init__(
        self,
        text,
        font_size=30,
        color=(242, 239, 250),
        font=None,
        align="left",
    ):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.align = align

        self.font = pygame.font.Font(font, font_size)

    def set_text(self, text):
        self.text = text

    def set_color(self, color):
        self.color = color

    def draw(self, surface, position):
        rendered = self.font.render(
            str(self.text),
            True,
            self.color,
        )

        rect = rendered.get_rect()

        if self.align == "center":
            rect.center = position
        elif self.align == "right":
            rect.midright = position
        else:
            rect.topleft = position

        surface.blit(rendered, rect)

        return rect
