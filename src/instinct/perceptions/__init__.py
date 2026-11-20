
"""
Paquete de percepciones de Instinct.

Contiene los grupos de percepciones y su registro.
"""

from instinct.perceptions.base import PerceptionGroup, PerceptionValue
from instinct.perceptions.nearby_perceptions import NearbyPerceptions
from instinct.perceptions.registry import PerceptionRegistry
from instinct.perceptions.self_perceptions import SelfPerceptions
from instinct.perceptions.world_perceptions import WorldPerceptions


__all__ = [
    "PerceptionGroup",
    "PerceptionValue",
    "SelfPerceptions",
    "WorldPerceptions",
    "NearbyPerceptions",
    "PerceptionRegistry",
]
