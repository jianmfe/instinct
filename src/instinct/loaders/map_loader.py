
from copy import deepcopy
from pathlib import Path

from instinct.world.entities import Terrain, WorldObject
from instinct.world.world_grid import WorldGrid


class MapLoader:
    """Carga mapas .map y construye sus correspondientes mundos."""

    def load_file(
        self,
        filepath: str | Path,
        terrains: list[Terrain],
        objects: list[WorldObject],
    ) -> tuple[str, WorldGrid]:
        path = Path(filepath)

        try:
            content = path.read_text(encoding="utf-8")
        except FileNotFoundError as error:
            raise ValueError(
                f"No se encontró el archivo de mapa: '{path}'."
            ) from error
        except UnicodeDecodeError as error:
            raise ValueError(
                f"El archivo de mapa '{path}' no contiene texto UTF-8 válido."
            ) from error
        except OSError as error:
            raise ValueError(
                f"No se pudo leer el archivo de mapa '{path}': {error}."
            ) from error

        return self.load_string(content, terrains, objects, str(path))

    def load_string(
        self,
        content: str,
        terrains: list[Terrain],
        objects: list[WorldObject],
        source: str = "<memoria>",
    ) -> tuple[str, WorldGrid]:
        if not isinstance(content, str):
            raise TypeError("El contenido del mapa debe ser texto.")

        if not terrains:
            raise ValueError(
                "No se puede cargar un mapa sin terrenos disponibles."
            )

        lines = content.splitlines()

        if len(lines) < 2:
            self._error(source, 1, "El mapa debe tener un nombre y al menos una fila.")

        map_name = lines[0].strip()

        if not map_name:
            self._error(source, 1, "El mapa debe tener un nombre.")

        rows = lines[1:]

        width = len(rows[0])

        if width == 0:
            self._error(source, 2, "Las filas del mapa no pueden estar vacías.")

        for line_number, row in enumerate(rows, start=2):
            if len(row) != width:
                self._error(
                    source,
                    line_number,
                    f"La fila tiene {len(row)} caracteres; se esperaban {width}.",
                )

        terrain_by_char = {}
        object_by_char = {}

        for terrain in terrains:
            if terrain.char in terrain_by_char:
                raise ValueError(
                    f"El carácter '{terrain.char}' está asignado "
                    "a más de un terreno."
                )
            terrain_by_char[terrain.char] = terrain

        for obj in objects:
            if obj.char in object_by_char:
                raise ValueError(
                    f"El carácter '{obj.char}' está asignado "
                    "a más de un objeto."
                )

            if obj.char in terrain_by_char:
                raise ValueError(
                    f"El carácter '{obj.char}' está asignado "
                    "a un terreno y a un objeto."
                )

            object_by_char[obj.char] = obj

        default_terrain = terrains[0]

        world = WorldGrid(
            width=width,
            height=len(rows),
            default_terrain=default_terrain,
        )

        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                tile = world.get_tile(x, y)

                if char in terrain_by_char:
                    tile.terrain = deepcopy(terrain_by_char[char])

                elif char in object_by_char:
                    tile.terrain = deepcopy(default_terrain)
                    world.place_object(x, y, deepcopy(object_by_char[char]))

                else:
                    self._error(
                        source,
                        y + 2,
                        f"El carácter '{char}' no corresponde "
                        "a ningún terreno ni objeto cargado.",
                    )

        return map_name, world

    @staticmethod
    def _error(source: str, line: int, message: str) -> None:
        raise ValueError(
            f"Error en '{source}', línea {line}: {message}"
        )
