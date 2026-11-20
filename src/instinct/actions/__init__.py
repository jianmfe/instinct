
"""
Paquete de acciones de Instinct.

Contiene la clase base, las acciones básicas
y el registro de acciones.
"""

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
from instinct.actions.registry import ActionRegistry


__all__ = [
    "Action",
    "ActionRegistry",
    "WaitAction",
    "MoveAction",
    "AttackAction",
    "ConsumeAction",
    "ReproduceAction",
    "RoarAction",
    "SayAction",
]
