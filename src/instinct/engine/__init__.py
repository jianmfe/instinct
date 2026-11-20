"""
Paquete del motor de simulación de Instinct.

Coordina los turnos, las leyes naturales,
el registro de acontecimientos y la simulación.
"""

from importlib import import_module


_EXPORTS = {
    "Event": (".event_log", "Event"),
    "EventLog": (".event_log", "EventLog"),
    "NaturalLaws": (".natural_laws", "NaturalLaws"),
    "Simulation": (".simulation", "Simulation"),
    "TurnManager": (".turn_manager", "TurnManager"),
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