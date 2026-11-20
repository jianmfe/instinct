
"""
Administrador de turnos de la simulación de Instinct.

Determina el orden aleatorio en que las criaturas ejecutan
sus programas durante cada tick.
"""

import random
from collections.abc import Callable

from instinct.world.entities import Creature
from instinct.world.world_grid import WorldGrid


TurnExecutor = Callable[[Creature, int], None]


class TurnManager:
    """Gestiona el orden de ejecución de las criaturas."""

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def execute_turns(
        self,
        world: WorldGrid,
        tick: int,
        execute_turn: TurnExecutor,
    ) -> None:
        """
        Ejecuta el turno de cada criatura presente al inicio del tick.

        Las criaturas nuevas no participan hasta el siguiente tick.
        Las criaturas que hayan muerto antes de su turno son omitidas.
        """

        creatures = self._get_creatures(world)

        # El orden se mezcla utilizando el generador compartido.
        self.rng.shuffle(creatures)

        for creature in creatures:
            if not self._is_alive_in_world(world, creature):
                continue

            execute_turn(creature, tick)

    @staticmethod
    def _get_creatures(world: WorldGrid) -> list[Creature]:
        """Obtiene una copia de las criaturas presentes en el mundo."""

        creatures: list[Creature] = []

        for row in world.tiles:
            for tile in row:
                if tile.creature is not None:
                    creatures.append(tile.creature)

        return creatures

    @staticmethod
    def _is_alive_in_world(
        world: WorldGrid,
        creature: Creature,
    ) -> bool:
        """Comprueba que la criatura siga ocupando su casilla."""

        if not world.in_bounds(creature.x, creature.y):
            return False

        tile = world.get_tile(creature.x, creature.y)

        return tile.creature is creature
