import pygame


class TopBar:
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.title_font = pygame.font.Font(None, 38)
        self.info_font = pygame.font.Font(None, 25)

    def draw(self, screen, map_name, tick, paused, speed):
        colors = self.theme_manager.colors
        width = screen.get_width()

        pygame.draw.rect(
            screen,
            colors["panel"],
            pygame.Rect(0, 0, width, 76),
        )

        pygame.draw.line(
            screen,
            colors["accent"],
            (0, 75),
            (width, 75),
            2,
        )

        title = self.title_font.render(
            "INSTINCT",
            True,
            colors["gold"],
        )

        screen.blit(title, (25, 17))

        map_text = self.info_font.render(
            f"Mapa: {map_name}",
            True,
            colors["text"],
        )

        screen.blit(map_text, (210, 27))

        status = "PAUSADA" if paused else "EN EJECUCIÓN"

        info = self.info_font.render(
            f"Tick: {tick}   |   {status}   |   Velocidad: {speed}x",
            True,
            colors["secondary_text"],
        )

        screen.blit(
            info,
            (width - info.get_width() - 30, 28),
        )