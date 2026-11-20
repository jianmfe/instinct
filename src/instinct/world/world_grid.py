
"""
Representación del mundo de Instinct mediante una grilla rectangular.

La grilla almacena las casillas utilizando la convención:
    tiles[y][x]

Cada casilla posee su propio terreno y puede contener
un objeto o una criatura.
"""

from copy import deepcopy

from instinct.world.entities import Creature, Terrain, WorldObject
from instinct.world.tile import Tile


class WorldGrid:
    """Grilla rectangular que representa el mundo de la simulación."""

    def __init__(
        self,
        width: int,
        height: int,
        default_terrain: Terrain,
    ) -> None:
        if not isinstance(width, int) or isinstance(width, bool):
            raise TypeError("El ancho del mundo debe ser un número entero.")

        if not isinstance(height, int) or isinstance(height, bool):
            raise TypeError("El alto del mundo debe ser un número entero.")

        if width <= 0 or height <= 0:
            raise ValueError("Las dimensiones del mundo deben ser positivas.")

        if not isinstance(default_terrain, Terrain):
            raise TypeError("El terreno predeterminado no es válido.")

        self.width = width
        self.height = height

        self.tiles: list[list[Tile]] = [
            [
                Tile(terrain=deepcopy(default_terrain))
                for _ in range(width)
            ]
            for _ in range(height)
        ]

    def in_bounds(self, x: int, y: int) -> bool:
        """Comprueba si una coordenada pertenece al mundo."""
        return (
            isinstance(x, int)
            and not isinstance(x, bool)
            and isinstance(y, int)
            and not isinstance(y, bool)
            and 0 <= x < self.width
            and 0 <= y < self.height
        )

    def get_tile(self, x: int, y: int) -> Tile:
        """Devuelve la casilla situada en las coordenadas indicadas."""
        if not self.in_bounds(x, y):
            raise IndexError(
                f"La posición ({x}, {y}) está fuera de los límites del mundo."
            )

        return self.tiles[y][x]

    def place_creature(self, creature: Creature, x: int, y: int) -> None:
        """Coloca una criatura en una casilla libre."""
        tile = self.get_tile(x, y)
        tile.set_creature(creature)

        creature.x = x
        creature.y = y

    def place_object(self, obj: WorldObject, x: int, y: int) -> None:
        """Coloca un objeto en una casilla libre."""
        tile = self.get_tile(x, y)
        tile.set_object(obj)

    def remove_creature(self, x: int, y: int) -> Creature | None:
        """Retira y devuelve la criatura de una casilla."""
        return self.get_tile(x, y).remove_creature()

    def remove_object(self, x: int, y: int) -> WorldObject | None:
        """Retira y devuelve el objeto de una casilla."""
        return self.get_tile(x, y).remove_object()
