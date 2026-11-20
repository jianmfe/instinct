
import pygame

from instinct.frontend.scenes.base_scene import BaseScene


class SimulationScene(BaseScene):
    """Escena provisional de simulación."""

    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.Font(None, 65)
        self.info_font = pygame.font.Font(None, 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from instinct.frontend.scenes.main_menu import MainMenu

                self.game.scene_manager.change_scene(
                    MainMenu(self.game)
                )

    def draw(self, screen):
        screen.fill((17, 22, 41))

        title = self.title_font.render(
            "SIMULACION",
            True,
            (212, 174, 98),
        )

        info = self.info_font.render(
            "El mundo de Instinct aparecera aqui.",
            True,
            (242, 239, 250),
        )

        screen.blit(
            title,
            title.get_rect(center=(960, 450)),
        )

        screen.blit(
            info,
            info.get_rect(center=(960, 530)),
        )

        hint = self.info_font.render(
            "Pulsa ESC para volver al menu",
            True,
            (170, 166, 190),
        )

        screen.blit(
            hint,
            hint.get_rect(center=(960, 950)),
        )
