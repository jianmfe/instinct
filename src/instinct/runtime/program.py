"""
Representación ejecutable de un programa de Instinct.

Recibe el AST producido por el compilador y prepara
las instrucciones y las posiciones de sus etiquetas
para que el intérprete pueda ejecutarlo.
"""

from collections.abc import Mapping
from types import MappingProxyType

from instinct.backend.ast_nodes import LabelNode, ProgramNode


class Program:
    """Representa un programa compilado listo para ejecutarse."""

    def __init__(self, ast: ProgramNode) -> None:
        if not isinstance(ast, ProgramNode):
            raise TypeError("El AST proporcionado no es un programa válido.")

        self.ast = ast
        self.header = ast.header

        # Conservamos las instrucciones en el orden original.
        self.statements = tuple(ast.statements)

        # Construimos el índice de etiquetas.
        labels: dict[str, int] = {}

        for position, statement in enumerate(self.statements):
            if isinstance(statement, LabelNode):
                if statement.name in labels:
                    raise ValueError(
                        f"Error de ejecución: la etiqueta "
                        f"'{statement.name}' está duplicada."
                    )

                labels[statement.name] = position

        if "start" not in labels:
            raise ValueError(
                "Error de ejecución: el programa no contiene "
                "la etiqueta obligatoria 'start'."
            )

        # Evitamos que otros módulos modifiquen directamente el índice.
        self.labels: Mapping[str, int] = MappingProxyType(labels)

    @property
    def start_position(self) -> int:
        """Devuelve la posición de la etiqueta inicial."""
        return self.labels["start"]

    def has_label(self, name: str) -> bool:
        """Comprueba si existe una etiqueta."""
        return name in self.labels

    def get_label_position(self, name: str) -> int:
        """Obtiene la posición de una etiqueta."""

        if name not in self.labels:
            raise RuntimeError(
                f"Error de ejecución: la etiqueta '{name}' no existe."
            )

        return self.labels[name]

    def __len__(self) -> int:
        """Devuelve la cantidad de instrucciones y etiquetas."""
        return len(self.statements)
