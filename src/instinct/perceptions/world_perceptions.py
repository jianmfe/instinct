
"""Percepciones relacionadas con el mundo completo."""

from instinct.perceptions.base import PerceptionGroup, PerceptionValue
from instinct.runtime.execution_context import ExecutionContext


class WorldPerceptions(PerceptionGroup):
    """Calcula las percepciones globales del mundo."""

    def calculate(
        self,
        context: ExecutionContext,
    ) -> dict[str, PerceptionValue]:

        world = context.world
        creature = context.creature_obj

        creatures = [
            tile.creature
            for row in world.tiles
            for tile in row
            if tile.creature is not None
        ]

        allies = sum(
            other.faction == creature.faction
            for other in creatures
            if other is not creature
        )

        enemies = sum(
            other.faction != creature.faction
            for other in creatures
            if other is not creature
        )

        return {
            "width": world.width,
            "height": world.height,
            "tick": context.current_tick,
            "total_creatures": len(creatures) - (
                1 if creature in creatures else 0
            ),
            "total_allies": allies,
            "total_enemies": enemies,
        }
