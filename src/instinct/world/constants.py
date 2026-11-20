
"""
Constantes del mundo de Instinct.

Los valores de SeeResult representan los posibles resultados
de la función see(x, y), según la especificación oficial.
"""

from enum import IntEnum


class SeeResult(IntEnum):
    """Tipos de contenido que puede detectar una criatura."""

    NONE = -1
    GROUND = 0
    OBJECT = 1
    ALLY = 2
    ENEMY = 3
