
from pathlib import Path

import pygame


class AssetLoader:
    """Centraliza la carga de recursos gráficos de Instinct."""

    def __init__(self):
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        self.cache = {}

    def load_image(
        self,
        relative_path,
        size=None,
        convert_alpha=True,
    ):
        """
        Carga una imagen desde assets.

        relative_path:
            Ruta relativa a la carpeta assets.

        size:
            Tamaño opcional (ancho, alto).

        Devuelve None si el archivo no existe o no puede cargarse.
        """

        path = self.assets_path / relative_path
        cache_key = (str(path), size, convert_alpha)

        if cache_key in self.cache:
            return self.cache[cache_key]

        if not path.is_file():
            return None

        try:
            image = pygame.image.load(str(path))

            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()

            if size is not None:
                image = pygame.transform.smoothscale(image, size)

            self.cache[cache_key] = image

            return image

        except (pygame.error, OSError) as error:
            print(f"Error al cargar el recurso gráfico '{path}': {error}")
            return None

    def load_creature_portrait(self, creature_name, size=None):
        """
        Carga el retrato de una criatura.

        Ejemplo:
            load_creature_portrait('dragon', (256, 256))

        Busca:
            assets/creatures/portraits/dragon.png
        """

        filename = f"{creature_name}.png"

        return self.load_image(
            Path("creatures") / "portraits" / filename,
            size=size,
        )

    def clear_cache(self):
        self.cache.clear()
