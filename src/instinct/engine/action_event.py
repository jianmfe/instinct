"""Registro de eventos estructurados producidos durante la simulación."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from instinct.world.entities import Creature


@dataclass(frozen=True, slots=True)
class ActionEvent:
    """Representa un acontecimiento producido durante la simulación."""

    tick: int
    event_type: str

    actor_id: int
    actor_name: str
    x: int
    y: int

    target_id: int | None = None
    target_name: str | None = None
    target_x: int | None = None
    target_y: int | None = None

    data: Mapping[str, Any] | None = None

    # Referencias a las criaturas originales.
    # Las coordenadas anteriores siguen siendo snapshots del momento del evento.
    actor_ref: Creature | None = None
    target_ref: Creature | None = None

    def __post_init__(self) -> None:
        if type(self.tick) is not int or self.tick < 0:
            raise ValueError("El número de tick no es válido.")

        if not isinstance(self.event_type, str) or not self.event_type:
            raise ValueError("El tipo de evento no es válido.")

        if type(self.actor_id) is not int or self.actor_id <= 0:
            raise ValueError("El identificador de la criatura no es válido.")

        if not isinstance(self.actor_name, str) or not self.actor_name:
            raise ValueError("El nombre de la criatura no es válido.")

        if type(self.x) is not int or type(self.y) is not int:
            raise ValueError("Las coordenadas de la criatura no son válidas.")

        if self.target_id is not None and (type(self.target_id) is not int or self.target_id <= 0):
            raise ValueError("El identificador del objetivo no es válido.")

        if (self.target_x is None) != (self.target_y is None):
            raise ValueError("Las coordenadas del objetivo están incompletas.")

        if self.target_x is not None and (type(self.target_x) is not int or type(self.target_y) is not int):
                raise ValueError("Las coordenadas del objetivo no son válidas.")

        if self.actor_ref is not None:
            if not isinstance(self.actor_ref, Creature):
                raise TypeError("La referencia de la criatura emisora no es válida.")

            if id(self.actor_ref) != self.actor_id:
                raise ValueError("La referencia de la criatura emisora no coincide.")

        if self.target_ref is not None:
            if not isinstance(self.target_ref, Creature):
                raise TypeError("La referencia de la criatura objetivo no es válida.")

            if self.target_id != id(self.target_ref):
                raise ValueError("La referencia de la criatura objetivo no coincide.")

        if self.target_id is None and self.target_ref is not None:
            raise ValueError("No puede existir una referencia sin un objetivo.")

        if self.data is not None:
            if not isinstance(self.data, Mapping):
                raise TypeError("Los datos del evento deben ser un diccionario.")

            object.__setattr__(
                self,
                "data",
                MappingProxyType(dict(self.data)),
            )


class ActionEventLog:
    """Almacena los acontecimientos estructurados de la simulación."""

    def __init__(self) -> None:
        self._events: list[ActionEvent] = []

    def publish(
        self,
        tick: int,
        event_type: str,
        actor: Creature,
        target: Creature | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> ActionEvent:
        if not isinstance(actor, Creature):
            raise TypeError("La criatura que origina el evento no es válida.")

        if target is not None and not isinstance(target, Creature):
            raise TypeError("La criatura objetivo no es válida.")

        event = ActionEvent(
            tick=tick,
            event_type=event_type,
            actor_id=id(actor),
            actor_name=actor.name,
            x=actor.x,
            y=actor.y,
            target_id=id(target) if target is not None else None,
            target_name=target.name if target is not None else None,
            target_x=target.x if target is not None else None,
            target_y=target.y if target is not None else None,
            data=data,
            actor_ref=actor,
            target_ref=target,
        )

        self._events.append(event)
        return event

    @property
    def events(self) -> tuple[ActionEvent, ...]:
        return tuple(self._events)

    def get_since(self, cursor: int) -> tuple[ActionEvent, ...]:
        if type(cursor) is not int or cursor < 0:
            raise ValueError("La posición de lectura no es válida.")

        return tuple(self._events[cursor:])

    def clear(self) -> None:
        self._events.clear()

    def __len__(self) -> int:
        return len(self._events)
