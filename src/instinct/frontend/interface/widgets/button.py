
import pygame


class Button:
    """Botón interactivo reutilizable."""

    def __init__(
        self,
        rect,
        text,
        callback=None,
        font_size=30,
        background=(41, 39, 71),
        hover_color=(76, 65, 112),
        text_color=(242, 239, 250),
        border_color=(118, 84, 168),
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

        self.font = pygame.font.Font(None, font_size)

        self.background = background
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color

        self.hovered = False
        self.pressed = False
        self.enabled = True

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.pressed = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = (
                    self.pressed
                    and self.rect.collidepoint(event.pos)
                )

                self.pressed = False

                if clicked and self.callback is not None:
                    self.callback()

    def draw(self, surface):
        color = self.background

        if not self.enabled:
            color = (65, 65, 75)
        elif self.pressed:
            color = self.border_color
        elif self.hovered:
            color = self.hover_color

        pygame.draw.rect(
            surface,
            color,
            self.rect,
            border_radius=10,
        )

        pygame.draw.rect(
            surface,
            self.border_color,
            self.rect,
            width=2,
            border_radius=10,
        )

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color,
        )

        surface.blit(
            text_surface,
            text_surface.get_rect(center=self.rect.center),
        )
