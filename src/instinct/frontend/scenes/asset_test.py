
import pygame

from instinct.frontend.menu.asset_loader import AssetLoader
from instinct.frontend.scenes.base_scene import BaseScene


class AssetTestScene(BaseScene):

    def __init__(self, game):
        super().__init__(game)

        self.assets = AssetLoader()

        self.grass = self.assets.load_terrain("grass")
        self.naruto = self.assets.load_sprite_sheet(
            "creatures/sprites/naruto/idle.png",
            frame_width=64,
            frame_height=64,
            scale=3,
        )

        self.font = pygame.font.Font(None, 32)

    def draw(self, screen):
        screen.fill((17, 22, 41))

        if self.grass:
            for y in range(3):
                for x in range(5):
                    screen.blit(
                        self.grass,
                        (100 + x * 32, 150 + y * 32),
                    )

        if self.naruto:
            screen.blit(self.naruto[0], (400, 150))

        message = self.font.render(
            "Prueba de recursos graficos",
            True,
            (242, 239, 250),
        )

        screen.blit(message, (100, 70))
