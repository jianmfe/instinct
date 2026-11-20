"""Clase base para las acciones del lenguaje Instinct."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from instinct.runtime.execution_context import ExecutionContext


class Action(ABC):
    """Interfaz común de todas las acciones."""

    name: str
    arity: int

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
        args: list[int | str],
    ) -> None:
        """Ejecuta la acción dentro del contexto de una criatura."""
        raise NotImplementedError

    def validate_arguments(
        self,
        args: list[int | str],
    ) -> None:
        """Comprueba que la acción reciba la cantidad correcta de argumentos."""

        if len(args) != self.arity:
            raise RuntimeError(
                f"Error de ejecución: la acción '{self.name}' "
                f"requiere {self.arity} argumento(s), "
                f"pero recibió {len(args)}."
            )

    @staticmethod
    def require_integer(
        value: int | str,
        argument_name: str,
        action_name: str,
    ) -> int:
        """Comprueba que un argumento sea un entero y no un booleano."""

        if type(value) is not int:
            raise RuntimeError(
                f"Error de ejecución: el argumento '{argument_name}' "
                f"de la acción '{action_name}' debe ser un número entero."
            )

        return value

    @staticmethod
    def require_direction(
        dx: int,
        dy: int,
        action_name: str,
    ) -> None:
        """Comprueba que una dirección sea válida."""

        if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
            raise RuntimeError(
                f"Error de ejecución: la dirección de la acción "
                f"'{action_name}' debe estar entre -1 y 1."
            )