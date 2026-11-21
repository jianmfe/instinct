
"""
Paquete de funciones de Instinct.

Contiene la clase base, las funciones básicas
y el registro de funciones.
"""

from instinct.functions.base import Function, FunctionValue
from instinct.functions.basic import NameFunction, SeeFunction
from instinct.functions.registry import FunctionRegistry

__all__ = [
    "Function",
    "FunctionRegistry",
    "FunctionValue",
    "NameFunction",
    "SeeFunction",
]
