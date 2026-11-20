
import pygame


class Dropdown:
    """Lista desplegable de opciones."""

    def __init__(
        self,
        rect,
        options,
        selected=None,
        callback=None,
        background=(41, 39, 71),
        text_color=(242, 239, 250),
        accent=(118, 84, 168),
    ):
        self.rect = pygame.Rect(rect)
        self.options = list(options)

        self.selected = selected if selected in self.options else (
            self.options[0] if self.options else None
        )

        self.callback = callback

        self.background = background
        self.text_color = text_color
        self.accent = accent

        self.font = pygame.font.Font(None, 28)
        self.opened = False
        self.option_height = self.rect.height

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        if self.rect.collidepoint(event.pos):
            self.opened = not self.opened
            return

        if self.opened:
            for index, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + index * self.option_height,
                    self.rect.width,
                    self.option_height,
                )

                if option_rect.collidepoint(event.pos):
                    self.selected = option
                    self.opened = False

                    if self.callback:
                        self.callback(option)

                    return

            self.opened = False

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.background,
            self.rect,
            border_radius=6,
        )

        pygame.draw.rect(
            surface,
            self.accent,
            self.rect,
            width=2,
            border_radius=6,
        )

        label = self.font.render(
            str(self.selected or "Seleccionar"),
            True,
            self.text_color,
        )

        surface.blit(
            label,
            (self.rect.x + 10, self.rect.y + 8),
        )

        if self.opened:
            for index, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + index * self.option_height,
                    self.rect.width,
                    self.option_height,
                )

                pygame.draw.rect(
                    surface,
                    self.background,
                    option_rect,
                )

                pygame.draw.rect(
                    surface,
                    self.accent,
                    option_rect,
                    width=1,
                )

                text = self.font.render(
                    str(option),
                    True,
                    self.text_color,
                )

                surface.blit(
                    text,
                    (option_rect.x + 10, option_rect.y + 8),
                )
