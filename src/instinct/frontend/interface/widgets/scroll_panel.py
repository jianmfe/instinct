
import pygame


class ScrollPanel:
    """Contenedor con desplazamiento vertical."""

    def __init__(
        self,
        rect,
        background=(41, 39, 71),
        scroll_speed=30,
    ):
        self.rect = pygame.Rect(rect)
        self.background = background
        self.scroll_speed = scroll_speed

        self.content_height = self.rect.height
        self.scroll_y = 0

        self.surface = pygame.Surface(
            (self.rect.width, self.content_height),
            pygame.SRCALPHA,
        )

    def set_content_height(self, height):
        self.content_height = max(height, self.rect.height)

        self.surface = pygame.Surface(
            (self.rect.width, self.content_height),
            pygame.SRCALPHA,
        )

        self.scroll_y = min(
            self.scroll_y,
            self.content_height - self.rect.height,
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_pos):
                self.scroll_y -= event.y * self.scroll_speed

                self.scroll_y = max(
                    0,
                    min(
                        self.scroll_y,
                        self.content_height - self.rect.height,
                    ),
                )

    def draw(self, screen, draw_content=None):
        self.surface.fill((0, 0, 0, 0))

        if draw_content:
            draw_content(self.surface)

        screen.set_clip(self.rect)

        screen.blit(
            self.surface,
            (
                self.rect.x,
                self.rect.y - self.scroll_y,
            ),
        )

        screen.set_clip(None)

        pygame.draw.rect(
            screen,
            self.background,
            self.rect,
            width=1,
            border_radius=6,
        )
