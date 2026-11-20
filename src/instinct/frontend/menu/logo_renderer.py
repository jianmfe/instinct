
import pygame


class LogoRenderer:
    """Renderiza el logotipo y subtítulo de Instinct."""

    def __init__(self):
        self.title_font = pygame.font.SysFont(
            "georgia",
            76,
            bold=True,
        )

        self.subtitle_font = pygame.font.SysFont(
            "georgia",
            22,
        )

    def draw(self, screen, center_x, y):
        title = self.title_font.render(
            "INSTINCT",
            True,
            (222, 190, 119),
        )

        subtitle = self.subtitle_font.render(
            "UN MUNDO QUE EVOLUCIONA",
            True,
            (195, 185, 211),
        )

        title_rect = title.get_rect(
            center=(center_x, y)
        )

        subtitle_rect = subtitle.get_rect(
            center=(center_x, y + 65)
        )

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        # Línea decorativa.
        pygame.draw.line(
            screen,
            (118, 84, 168),
            (center_x - 140, y + 88),
            (center_x + 140, y + 88),
            2,
        )
