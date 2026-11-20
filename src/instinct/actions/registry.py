
"""Registro central de acciones de Instinct."""

from instinct.actions.base import Action
from instinct.actions.basic import (
    AttackAction,
    ConsumeAction,
    MoveAction,
    ReproduceAction,
    RoarAction,
    SayAction,
    WaitAction,
)
from instinct.runtime.execution_context import ExecutionContext


class ActionRegistry:
    """Almacena y ejecuta las acciones disponibles."""

    def __init__(self, include_basic: bool = True) -> None:
        self._actions: dict[str, Action] = {}

        if include_basic:
            self.register_basic_actions()

    def register(self, action: Action) -> None:
        """Registra una acción nueva."""

        if not isinstance(action, Action):
            raise TypeError(
                "Solo se pueden registrar objetos de tipo Action."
            )

        if not isinstance(action.name, str) or not action.name:
            raise ValueError("El nombre de la acción no es válido.")

        if action.name in self._actions:
            raise ValueError(
                f"La acción '{action.name}' ya está registrada."
            )

        if (
            not isinstance(action.arity, int)
            or isinstance(action.arity, bool)
            or action.arity < 0
        ):
            raise ValueError(
                f"La cantidad de argumentos de '{action.name}' no es válida."
            )

        self._actions[action.name] = action

    def register_basic_actions(self) -> None:
        """Registra las siete acciones obligatorias."""

        basic_actions = (
            WaitAction(),
            MoveAction(),
            AttackAction(),
            ConsumeAction(),
            ReproduceAction(),
            RoarAction(),
            SayAction(),
        )

        for action in basic_actions:
            self.register(action)

    def get(self, name: str) -> Action:
        """Obtiene una acción por su nombre."""

        if name not in self._actions:
            raise RuntimeError(
                f"Error de ejecución: la acción '{name}' no existe."
            )

        return self._actions[name]

    def execute(
        self,
        context: ExecutionContext,
        name: str,
        args: list[int | str],
    ) -> None:
        """Busca y ejecuta una acción."""

        action = self.get(name)
        action.execute(context, args)

    def has_action(self, name: str) -> bool:
        """Indica si una acción está registrada."""
        return name in self._actions

    @property
    def actions(self) -> tuple[str, ...]:
        """Devuelve los nombres de las acciones registradas."""
        return tuple(self._actions.keys())

    def __len__(self) -> int:
        return len(self._actions)
