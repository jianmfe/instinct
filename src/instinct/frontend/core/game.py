
import pygame

from instinct.frontend.settings import (
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    RESIZABLE,
    FULLSCREEN,
    TARGET_FPS,
)

from instinct.frontend.core.scene_manager import SceneManager


class Game:
    """Coordina el funcionamiento general de Instinct."""

    def __init__(self):
        pygame.init()

        flags = 0

        if RESIZABLE:
            flags |= pygame.RESIZABLE

        if FULLSCREEN:
            flags |= pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            flags,
        )

        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager(self)

    def run(self):
        """Bucle principal de la aplicación."""

        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                self.scene_manager.handle_event(event)

            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def quit(self):
        """Solicita el cierre de la aplicación."""
        self.running = False
