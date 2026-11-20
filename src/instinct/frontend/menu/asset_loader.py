from pathlib import Path

import pygame


class AssetLoader:
    """Centraliza la carga de recursos gráficos de Instinct."""

    def __init__(self):
        self.assets_path = (
            Path(__file__).resolve().parent.parent / "assets"
        )
        self.cache = {}

    def load_image(
        self,
        relative_path,
        size=None,
        convert_alpha=True,
        pixel_art=True,
    ):
        """Carga una imagen desde la carpeta assets."""

        path = self.assets_path / relative_path

        cache_key = (
            str(path),
            size,
            convert_alpha,
            pixel_art,
        )

        if cache_key in self.cache:
            return self.cache[cache_key]

        if not path.is_file():
            print(f"No se encontró el recurso gráfico: '{path}'.")
            return None

        try:
            image = pygame.image.load(str(path))

            if convert_alpha:
                image = image.convert_alpha()
            elif pygame.display.get_surface() is not None:
                image = image.convert()

            if size is not None:
                scaler = (
                    pygame.transform.scale
                    if pixel_art
                    else pygame.transform.smoothscale
                )
                image = scaler(image, size)

            self.cache[cache_key] = image
            return image

        except (pygame.error, OSError) as error:
            print(
                f"No se pudo cargar el recurso gráfico "
                f"'{path}': {error}"
            )
            return None

    def load_sprite_sheet(
        self,
        relative_path,
        frame_width,
        frame_height,
        scale=1,
    ):
        """Carga una spritesheet horizontal y separa sus fotogramas."""

        if frame_width <= 0 or frame_height <= 0:
            raise ValueError(
                "Las dimensiones de los fotogramas deben ser positivas."
            )

        if scale <= 0:
            raise ValueError(
                "La escala de los fotogramas debe ser positiva."
            )

        image = self.load_image(relative_path)

        if image is None:
            return []

        if image.get_width() % frame_width != 0:
            raise ValueError(
                f"La spritesheet '{relative_path}' no tiene "
                "un ancho divisible por el fotograma."
            )

        if image.get_height() % frame_height != 0:
            raise ValueError(
                f"La spritesheet '{relative_path}' no tiene "
                "una altura divisible por el fotograma."
            )

        frames = []

        columns = image.get_width() // frame_width
        rows = image.get_height() // frame_height

        for row in range(rows):
            for column in range(columns):
                rect = pygame.Rect(
                    column * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height,
                )

                frame = image.subsurface(rect).copy()

                if scale != 1:
                    frame = pygame.transform.scale(
                        frame,
                        (
                            frame_width * scale,
                            frame_height * scale,
                        ),
                    )

                frames.append(frame)

        return frames

    def load_terrain(self, terrain_name, size=None):
        return self.load_image(
            Path("biomes") / terrain_name.lower()
            / f"{terrain_name.lower()}.png",
            size=size,
        )

    def load_object(self, object_name, size=None):
        return self.load_image(
            Path("objects") / f"{object_name.lower()}.png",
            size=size,
        )

    def load_creature_portrait(self, creature_name, size=None):
        return self.load_image(
            Path("creatures") / "portraits"
            / f"{creature_name.lower()}.png",
            size=size,
        )

    def clear_cache(self):
        self.cache.clear()
