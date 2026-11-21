
"""Implementación de las siete acciones básicas de Instinct."""

from instinct.actions.base import Action
from instinct.runtime.execution_context import ExecutionContext
from instinct.world.entities import Creature


class WaitAction(Action):
    name = "wait"
    arity = 1

    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        self.validate_arguments(args)
        self.require_integer(args[0], "n", self.name)

        # El intérprete administra los turnos de espera.
        # Esta acción no necesita modificar el mundo.
        return


class MoveAction(Action):
    name = "move"
    arity = 3

    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        self.validate_arguments(args)

        dx = self.require_integer(args[0], "dx", self.name)
        dy = self.require_integer(args[1], "dy", self.name)
        speed = self.require_integer(args[2], "speed", self.name)

        self.require_direction(dx, dy, self.name)

        creature = context.creature_obj
        world = context.world

        if dx == 0 and dy == 0:
            return

        start_x = creature.x
        start_y = creature.y

        # Avanza casilla por casilla hasta alcanzar speed
        # o encontrar un obstáculo.
        for _ in range(max(0, speed)):
            next_x = creature.x + dx
            next_y = creature.y + dy

            if not world.in_bounds(next_x, next_y):
                break

            next_tile = world.get_tile(next_x, next_y)

            if next_tile.is_occupied:
                break

            current_x = creature.x
            current_y = creature.y

            world.remove_creature(current_x, current_y)
            world.place_creature(creature, next_x, next_y)

        distance = max(
            abs(creature.x - start_x),
            abs(creature.y - start_y),
        )

        if distance > 0:
            context.publish_action_event(
                "move",
                data={
                    "start": (start_x, start_y),
                    "end": (creature.x, creature.y),
                    "distance": distance,
                    "dx": dx,
                    "dy": dy,
                    "speed": speed,
                },
            )


class AttackAction(Action):
    name = "attack"
    arity = 3

    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        self.validate_arguments(args)

        dx = self.require_integer(args[0], "dx", self.name)
        dy = self.require_integer(args[1], "dy", self.name)
        damage = self.require_integer(args[2], "damage", self.name)

        self.require_direction(dx, dy, self.name)

        context.publish_action_event(
            "attack",
            data={
                "dx": dx,
                "dy": dy,
                "damage": damage,
            },
        )

        self._attack_target(context, dx, dy, damage)

    @staticmethod
    def _attack_target(
        context: ExecutionContext,
        dx: int,
        dy: int,
        damage: int,
    ) -> Creature | None:
        """Aplica daño al objetivo y registra sus consecuencias."""

        creature = context.creature_obj
        world = context.world

        target_x = creature.x + dx
        target_y = creature.y + dy

        if not world.in_bounds(target_x, target_y):
            return None

        tile = world.get_tile(target_x, target_y)

        if dx == 0 and dy == 0:
            tile.terrain.reserve = max(
                0,
                tile.terrain.reserve - damage,
            )
            return None

        # Si hay una criatura, recibe el daño.
        target_creature = tile.creature

        if target_creature is not None:
            target_creature.health -= damage

            context.publish_action_event(
                "damage",
                target=target_creature,
                data={
                    "damage": damage,
                    "remaining_health": target_creature.health,
                },
            )

            if target_creature.health <= 0:
                tile.remove_creature()

                context.event_log.add(
                    context.current_tick,
                    (
                        f"La criatura '{target_creature.name}' "
                        f"ha muerto por el ataque de '{creature.name}'."
                    ),
                    "muerte",
                )

                context.publish_action_event(
                    "death",
                    target=target_creature,
                    data={
                        "cause": "attack",
                        "damage": damage,
                    },
                )

            return target_creature

        # Si hay un objeto, pierde reserva.
        target_object = tile.object

        if target_object is not None:
            target_object.reserve = max(
                0,
                target_object.reserve - damage,
            )

            if target_object.reserve <= 0:
                tile.remove_object()

            return None

        # Si no hay ocupante, el objetivo es el terreno.
        tile.terrain.reserve = max(
            0,
            tile.terrain.reserve - damage,
        )

        return None



class ConsumeAction(Action):
    name = "consume"
    arity = 4

    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        self.validate_arguments(args)

        dx = self.require_integer(args[0], "dx", self.name)
        dy = self.require_integer(args[1], "dy", self.name)
        damage = self.require_integer(args[2], "damage", self.name)
        heal = self.require_integer(args[3], "heal", self.name)

        self.require_direction(dx, dy, self.name)

        creature = context.creature_obj
        world = context.world

        target_x = creature.x + dx
        target_y = creature.y + dy

        # No se puede consumir fuera del mundo.
        if not world.in_bounds(target_x, target_y):
            return

        target_tile = world.get_tile(target_x, target_y)
        target_object = target_tile.object

        # Solo se pueden consumir objetos existentes.
        if target_object is None:
            return

        if damage <= 0 or target_object.reserve <= 0:
            return

        # Consumir los recursos disponibles del objeto.
        consumed = min(damage, target_object.reserve)

        target_object.reserve -= consumed

        # Eliminar el objeto cuando se agoten sus recursos.
        if target_object.reserve <= 0:
            target_tile.remove_object()

        # Aplicar la curación.
        creature.health += heal

        # Publicar el evento después de consumir correctamente.
        context.publish_action_event(
            "consume",
            data={
                "dx": dx,
                "dy": dy,
                "damage": consumed,
                "heal": heal,
                "object": target_object.name,
                "remaining_reserve": target_object.reserve,
            },
        )

class ReproduceAction(Action):
    name = "reproduce"
    arity = 3

    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        self.validate_arguments(args)

        dx = self.require_integer(args[0], "dx", self.name)
        dy = self.require_integer(args[1], "dy", self.name)
        child_health = self.require_integer(args[2], "health", self.name)

        self.require_direction(dx, dy, self.name)

        if dx == 0 and dy == 0:
            raise RuntimeError(
                "Error de ejecución: reproduce requiere una casilla "
                "adyacente distinta de la posición de la madre."
            )

        if child_health <= 0:
            return

        mother = context.creature_obj
        world = context.world

        target_x = mother.x + dx
        target_y = mother.y + dy

        # La reproducción falla si el destino no es válido
        # o no contiene únicamente terreno.
        if not world.in_bounds(target_x, target_y):
            return

        target_tile = world.get_tile(target_x, target_y)

        if target_tile.is_occupied:
            return

        # La madre debe tener más vida que la que entrega.
        if mother.health <= child_health:
            return

        child = Creature(
            name=mother.name,
            faction=mother.faction,
            health=child_health,
            vision=mother.vision,
            lifespan=mother.lifespan,
            x=target_x,
            y=target_y,
            age=0,
            program=context.program,
        )

        # Primero se descuenta la vida y luego nace la criatura.
        mother.health -= child_health
        world.place_creature(child, target_x, target_y)

        context.publish_action_event(
            "reproduce",
            target=child,
            data={
                "child_health": child_health,
                "position": (target_x, target_y),
            },
        )


class RoarAction(Action):
    name = "roar"
    arity = 1

    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        self.validate_arguments(args)

        value = str(args[0])
        creature = context.creature_obj

        context.event_log.add(
            context.current_tick,
            f"{creature.name}: {value}",
            "rugido",
            x=creature.x,
            y=creature.y,
        )

        context.publish_action_event(
            "roar",
            data={
                "message": value,
            },
        )


class SayAction(Action):
    name = "say"
    arity = 1

    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        self.validate_arguments(args)

        value = str(args[0])
        creature = context.creature_obj

        context.event_log.add(
            context.current_tick,
            f"{creature.name}: {value}",
            "mensaje",
        )
