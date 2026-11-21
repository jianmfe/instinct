
"""Clase base para los grupos de percepciones de Instinct."""

from abc import ABC, abstractmethod

from instinct.runtime.execution_context import ExecutionContext

PerceptionValue = int | str


class PerceptionGroup(ABC):
    """Interfaz de un grupo de percepciones."""

    @abstractmethod
    def calculate(
        self,
        context: ExecutionContext,
    ) -> dict[str, PerceptionValue]:
        """Calcula las percepciones pertenecientes al grupo."""
        raise NotImplementedError
