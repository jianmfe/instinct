"""
Paquete de ejecución de Instinct.

Contiene el intérprete, los programas ejecutables,
los entornos de variables y los contextos de ejecución.
"""

from importlib import import_module


_EXPORTS = {
    "Environment": (".environment", "Environment"),
    "ExecutionContext": (".execution_context", "ExecutionContext"),
    "Interpreter": (".interpreter", "Interpreter"),
    "Program": (".program", "Program"),
}

__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name not in _EXPORTS:
        raise AttributeError(
            f"El módulo '{__name__}' no contiene el atributo '{name}'."
        )

    module_name, attribute_name = _EXPORTS[name]
    module = import_module(module_name, __name__)
    value = getattr(module, attribute_name)

    globals()[name] = value
    return value