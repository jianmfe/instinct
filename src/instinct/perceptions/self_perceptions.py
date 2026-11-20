
"""Percepciones relacionadas con la propia criatura."""

from instinct.perceptions.base import PerceptionGroup, PerceptionValue
from instinct.runtime.execution_context import ExecutionContext


class SelfPerceptions(PerceptionGroup):
    """Calcula las percepciones de la propia criatura."""

    def calculate(
        self,
        context: ExecutionContext,
    ) -> dict[str, PerceptionValue]:

        creature = context.creature_obj
        tile = context.world.get_tile(creature.x, creature.y)

        return {
            "health": creature.health,
            "age": creature.age,
            "lifespan": creature.lifespan,
            "vision": creature.vision,
            "species": creature.name,
            "faction": creature.faction,
            "x": creature.x,
            "y": creature.y,
            "terrain_here": tile.terrain.name,
            "reserve_here": tile.terrain.reserve,
        }
