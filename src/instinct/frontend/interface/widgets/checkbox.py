
import pygame


class Checkbox:
    """Control de selección activado/desactivado."""

    def __init__(
        self,
        rect,
        text,
        checked=False,
        callback=None,
        box_color=(118, 84, 168),
        text_color=(242, 239, 250),
    ):
        self.rect = pygame.Rect(rect)
        self.text = text

        self.checked = checked
        self.callback = callback

        self.box_color = box_color
        self.text_color = text_color

        self.font = pygame.font.Font(None, 28)

        self.box_size = 22

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
                self.checked = not self.checked

                if self.callback:
                    self.callback(self.checked)

    def draw(self, surface):
        box = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.box_size,
            self.box_size,
        )

        pygame.draw.rect(
            surface,
            self.box_color,
            box,
            width=2,
            border_radius=4,
        )

        if self.checked:
            pygame.draw.rect(
                surface,
                self.box_color,
                box.inflate(-6, -6),
                border_radius=2,
            )

        label = self.font.render(
            self.text,
            True,
            self.text_color,
        )

        surface.blit(
            label,
            (self.rect.x + self.box_size + 10, self.rect.y),
        )
