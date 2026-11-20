
import pygame


class ObjectRenderer:
    """Representa visualmente los objetos del mundo."""

    DEFAULT_COLOR = (125, 125, 135)
    OUTLINE_COLOR = (65, 65, 75)

    def __init__(self, asset_loader=None):
        self.asset_loader = asset_loader
        self.object_images = {}

    def get_object_image(self, obj):
        """Obtiene la imagen de un objeto, si está disponible."""

        if self.asset_loader is None:
            return None

        name = obj.name

        if name not in self.object_images:
            image = self.asset_loader.load_object(name)
            self.object_images[name] = image

        return self.object_images[name]

    def draw_object(self, screen, obj, rect):
        """Dibuja un objeto sobre la casilla correspondiente."""

        if obj is None:
            return

        image = self.get_object_image(obj)

        if image is not None:
            if image.get_size() != rect.size:
                image = pygame.transform.scale(image, rect.size)

            screen.blit(image, rect)
        else:
            self._draw_placeholder(screen, rect)

    def _draw_placeholder(self, screen, rect):
        """Dibuja una representación provisional del objeto."""

        object_rect = rect.inflate(-8, -8)

        pygame.draw.ellipse(
            screen,
            self.DEFAULT_COLOR,
            object_rect,
        )

        pygame.draw.ellipse(
            screen,
            self.OUTLINE_COLOR,
            object_rect,
            2,
        )
