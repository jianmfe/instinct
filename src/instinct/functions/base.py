
"""Clase base para las funciones del lenguaje Instinct."""

from abc import ABC, abstractmethod

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from instinct.runtime.execution_context import ExecutionContext


FunctionValue = int | str


class Function(ABC):
    """Interfaz común de las funciones del lenguaje."""

    name: str
    arity: int

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
        args: list[FunctionValue],
    ) -> FunctionValue:
        """Evalúa la función y devuelve su resultado."""
        raise NotImplementedError

    def validate_arguments(
        self,
        args: list[FunctionValue],
    ) -> None:
        """Comprueba la cantidad de argumentos recibidos."""

        if len(args) != self.arity:
            raise RuntimeError(
                f"Error de ejecución: la función '{self.name}' "
                f"requiere {self.arity} argumento(s), "
                f"pero recibió {len(args)}."
            )

    @staticmethod
    def require_integer(
        value: FunctionValue,
        argument_name: str,
        function_name: str,
    ) -> int:
        """Comprueba que un argumento sea un entero."""

        if type(value) is not int:
            raise RuntimeError(
                f"Error de ejecución: el argumento '{argument_name}' "
                f"de la función '{function_name}' debe ser un entero."
            )

        return value
