
"""
Representación de una casilla del mundo de Instinct.

Cada casilla contiene obligatoriamente un terreno y puede contener
un objeto o una criatura, pero nunca ambos simultáneamente.
"""

from dataclasses import dataclass, field

from instinct.world.entities import Creature, Terrain, WorldObject


@dataclass
class Tile:
    """Casilla individual del mundo."""

    terrain: Terrain
    _object: WorldObject | None = field(default=None, repr=False)
    _creature: Creature | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.terrain, Terrain):
            raise TypeError("Una casilla debe tener un terreno válido.")

        if self._object is not None and not isinstance(
            self._object, WorldObject
        ):
            raise TypeError("El contenido debe ser un objeto válido.")

        if self._creature is not None and not isinstance(
            self._creature, Creature
        ):
            raise TypeError("El contenido debe ser una criatura válida.")

        if self._object is not None and self._creature is not None:
            raise ValueError(
                "Una casilla no puede contener un objeto y una criatura a la vez."
            )

    @property
    def object(self) -> WorldObject | None:
        """Devuelve el objeto de la casilla, si existe."""
        return self._object

    @property
    def creature(self) -> Creature | None:
        """Devuelve la criatura de la casilla, si existe."""
        return self._creature

    @property
    def is_occupied(self) -> bool:
        """Indica si la casilla está ocupada."""
        return self._object is not None or self._creature is not None

    @property
    def occupant(self) -> WorldObject | Creature | None:
        """Devuelve el contenido de la casilla, si existe."""
        if self._object is not None:
            return self._object

        return self._creature

    def set_object(self, obj: WorldObject) -> None:
        """Coloca un objeto si la casilla está libre."""
        if not isinstance(obj, WorldObject):
            raise TypeError("Solo se pueden colocar objetos válidos.")

        if self.is_occupied:
            raise ValueError("La casilla ya está ocupada.")

        self._object = obj

    def set_creature(self, creature: Creature) -> None:
        """Coloca una criatura si la casilla está libre."""
        if not isinstance(creature, Creature):
            raise TypeError("Solo se pueden colocar criaturas válidas.")

        if self.is_occupied:
            raise ValueError("La casilla ya está ocupada.")

        self._creature = creature

    def remove_object(self) -> WorldObject | None:
        """Retira y devuelve el objeto de la casilla."""
        obj = self._object
        self._object = None
        return obj

    def remove_creature(self) -> Creature | None:
        """Retira y devuelve la criatura de la casilla."""
        creature = self._creature
        self._creature = None
        return creature
