import pygame


class BiomeRenderer:
    """Representa visualmente los terrenos del mundo."""

    # Colores provisionales mientras no estén disponibles los tiles.
    TERRAIN_COLORS = {
        "grass": (83, 142, 76),
        "desert": (211, 178, 112),
        "sand": (211, 178, 112),
        "water": (55, 112, 166),
        "mountain": (112, 112, 120),
        "rock": (112, 112, 120),
        "swamp": (83, 112, 83),
        "plains": (148, 166, 91),
        "forest": (48, 105, 63),
        "snow": (220, 225, 230),
    }

    DEFAULT_COLOR = (105, 105, 105)

    def __init__(self, asset_loader=None):
        self.asset_loader = asset_loader
        self.terrain_images = {}

    def get_terrain_color(self, terrain):
        """Obtiene el color provisional correspondiente al terreno."""

        name = terrain.name.lower()
        return self.TERRAIN_COLORS.get(name, self.DEFAULT_COLOR)

    def get_terrain_image(self, terrain):
        """Obtiene la imagen del terreno, si está disponible."""

        if self.asset_loader is None:
            return None

        name = terrain.name

        if name not in self.terrain_images:
            image = self.asset_loader.load_terrain(name)
            self.terrain_images[name] = image

        return self.terrain_images[name]

    def draw_tile(self, screen, tile, rect):
        """Dibuja el terreno de una casilla."""

        terrain = tile.terrain
        image = self.get_terrain_image(terrain)

        if image is not None:
            if image.get_size() != rect.size:
                image = pygame.transform.scale(image, rect.size)

            screen.blit(image, rect)
        else:
            pygame.draw.rect(
                screen,
                self.get_terrain_color(terrain),
                rect,
            )
