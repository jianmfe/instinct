
"""Registro central de funciones de Instinct."""

from instinct.functions.base import Function, FunctionValue
from instinct.functions.basic import NameFunction, SeeFunction
from instinct.runtime.execution_context import ExecutionContext


class FunctionRegistry:
    """Almacena y ejecuta las funciones disponibles."""

    def __init__(self, include_basic: bool = True) -> None:
        self._functions: dict[str, Function] = {}

        if include_basic:
            self.register_basic_functions()

    def register(self, function: Function) -> None:
        """Registra una función nueva."""

        if not isinstance(function, Function):
            raise TypeError(
                "Solo se pueden registrar objetos de tipo Function."
            )

        if not isinstance(function.name, str) or not function.name:
            raise ValueError("El nombre de la función no es válido.")

        if function.name in self._functions:
            raise ValueError(
                f"La función '{function.name}' ya está registrada."
            )

        if (
            not isinstance(function.arity, int)
            or isinstance(function.arity, bool)
            or function.arity < 0
        ):
            raise ValueError(
                f"La cantidad de argumentos de '{function.name}' "
                "no es válida."
            )

        self._functions[function.name] = function

    def register_basic_functions(self) -> None:
        """Registra las funciones obligatorias."""

        for function in (SeeFunction(), NameFunction()):
            self.register(function)

    def get(self, name: str) -> Function:
        """Obtiene una función por su nombre."""

        if name not in self._functions:
            raise RuntimeError(
                f"Error de ejecución: la función '{name}' no existe."
            )

        return self._functions[name]

    def execute(
        self,
        context: ExecutionContext,
        name: str,
        args: list[FunctionValue],
    ) -> FunctionValue:
        """Ejecuta una función y devuelve su resultado."""

        function = self.get(name)
        return function.execute(context, args)

    def has_function(self, name: str) -> bool:
        """Indica si una función está registrada."""
        return name in self._functions

    @property
    def functions(self) -> tuple[str, ...]:
        """Devuelve los nombres de las funciones registradas."""
        return tuple(self._functions.keys())

    def __len__(self) -> int:
        return len(self._functions)
