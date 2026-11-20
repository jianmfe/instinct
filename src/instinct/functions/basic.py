
"""Funciones básicas del lenguaje Instinct."""

from instinct.functions.base import Function, FunctionValue
from instinct.runtime.execution_context import ExecutionContext
from instinct.world.constants import SeeResult


class SeeFunction(Function):
    """Identifica qué hay en una coordenada del mapa."""

    name = "see"
    arity = 2

    def execute(
        self,
        context: ExecutionContext,
        args: list[FunctionValue],
    ) -> int:
        self.validate_arguments(args)

        x = self.require_integer(args[0], "x", self.name)
        y = self.require_integer(args[1], "y", self.name)

        creature = context.creature_obj
        world = context.world

        # Distancia Chebyshev: incluye las diagonales.
        distance = max(
            abs(x - creature.x),
            abs(y - creature.y),
        )

        # Primero se comprueba el radio de visión.
        if distance > creature.vision:
            return SeeResult.NONE

        # Fuera del mapa, pero dentro del radio de visión,
        # se considera un muro indestructible.
        if not world.in_bounds(x, y):
            return SeeResult.OBJECT

        tile = world.get_tile(x, y)

        if tile.creature is not None:
            if tile.creature.faction == creature.faction:
                return SeeResult.ALLY

            return SeeResult.ENEMY

        if tile.object is not None:
            return SeeResult.OBJECT

        return SeeResult.GROUND


class NameFunction(Function):
    """Devuelve el nombre de lo que hay en una coordenada."""

    name = "name"
    arity = 2

    def execute(
        self,
        context: ExecutionContext,
        args: list[FunctionValue],
    ) -> str:
        self.validate_arguments(args)

        x = self.require_integer(args[0], "x", self.name)
        y = self.require_integer(args[1], "y", self.name)

        creature = context.creature_obj
        world = context.world

        distance = max(
            abs(x - creature.x),
            abs(y - creature.y),
        )

        # Fuera del radio o fuera del mapa no se conoce el nombre.
        if distance > creature.vision or not world.in_bounds(x, y):
            return ""

        tile = world.get_tile(x, y)

        if tile.creature is not None:
            return tile.creature.name

        if tile.object is not None:
            return tile.object.name

        return tile.terrain.name
