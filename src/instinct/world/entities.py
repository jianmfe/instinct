
"""
Entidades que pueden existir en el mundo de Instinct.

Terrain: terreno que recupera sus recursos con el paso de los ticks.
WorldObject: objeto cuyos recursos no se regeneran.
Creature: criatura que participa en la simulación.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from instinct.runtime.program import Program


@dataclass
class ResourceEntity:
    """Entidad que posee una reserva limitada de recursos."""

    name: str
    char: str
    resource_max: int
    reserve: int | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("El nombre de la entidad no puede estar vacío.")

        if len(self.char) != 1:
            raise ValueError(
                "El símbolo de la entidad debe ser exactamente un carácter."
            )

        if not isinstance(self.resource_max, int) or isinstance(
            self.resource_max, bool
        ):
            raise TypeError("La reserva máxima debe ser un número entero.")

        if self.resource_max < 0:
            raise ValueError("La reserva máxima no puede ser negativa.")

        if self.reserve is None:
            self.reserve = self.resource_max

        if not isinstance(self.reserve, int) or isinstance(self.reserve, bool):
            raise TypeError("La reserva debe ser un número entero.")

        if not 0 <= self.reserve <= self.resource_max:
            raise ValueError(
                "La reserva debe estar entre cero y la reserva máxima."
            )


@dataclass
class Terrain(ResourceEntity):
    """Terreno que regenera sus recursos durante la simulación."""

    regen: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()

        if not isinstance(self.regen, int) or isinstance(self.regen, bool):
            raise TypeError("La regeneración debe ser un número entero.")

        if self.regen < 0:
            raise ValueError("La regeneración no puede ser negativa.")


@dataclass
class WorldObject(ResourceEntity):
    """Objeto del mundo que no regenera sus recursos."""


@dataclass
class Creature:
    """Criatura individual que participa en la simulación."""

    name: str
    faction: str
    health: int
    vision: int
    lifespan: int
    x: int = 0
    y: int = 0
    age: int = 0
    program: "Program | None" = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("El nombre de la criatura no puede estar vacío.")

        if not self.faction:
            raise ValueError("La facción de la criatura no puede estar vacía.")

        integer_fields = {
            "La vida": self.health,
            "La visión": self.vision,
            "La esperanza de vida": self.lifespan,
            "La coordenada x": self.x,
            "La coordenada y": self.y,
            "La edad": self.age,
        }

        for field_name, value in integer_fields.items():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{field_name} debe ser un número entero.")

        if self.health <= 0:
            raise ValueError("La vida inicial debe ser mayor que cero.")

        if self.vision < 1:
            raise ValueError("La visión debe ser como mínimo uno.")

        if self.lifespan <= 0:
            raise ValueError("La esperanza de vida debe ser mayor que cero.")

        if self.age < 0:
            raise ValueError("La edad no puede ser negativa.")
