
from dataclasses import dataclass
from typing import Any


@dataclass
class ASTNode:
    lineno: int


class ExpressionNode(ASTNode):
    """Base para los nodos del AST que pueden evaluarse."""

    def evaluate(self, memory: Any) -> Any:
        raise NotImplementedError(
            "Las expresiones deben implementar evaluate()."
        )


@dataclass
class HeaderNode(ASTNode):
    creature: str
    faction: str
    health: int
    vision: int
    lifespan: int


@dataclass
class ProgramNode(ASTNode):
    header: HeaderNode
    statements: list[ASTNode]


@dataclass
class LabelNode(ASTNode):
    name: str


@dataclass
class GotoNode(ASTNode):
    target: str


@dataclass
class IfGotoNode(ASTNode):
    condition: ExpressionNode
    target: str


@dataclass
class AssignNode(ASTNode):
    name: str
    value: ExpressionNode


@dataclass
class ActionNode(ASTNode):
    name: str
    args: list[ExpressionNode]


# NODOS DE EXPRESION

@dataclass
class NumberNode(ExpressionNode):
    value: int

    def evaluate(self, memory: Any) -> int:
        return self.value


@dataclass
class StringNode(ExpressionNode):
    value: str

    def evaluate(self, memory: Any) -> str:
        return self.value


@dataclass
class IdentifierNode(ExpressionNode):
    name: str

    def evaluate(self, memory: Any) -> Any:
        missing = object()

        if isinstance(memory, dict):
            value = memory.get(self.name, missing)
        else:
            value = getattr(memory, self.name, missing)

        if value is missing:
            raise RuntimeError(
                f"Error en la linea {self.lineno}: "
                f"La variable '{self.name}' no ha sido inicializada."
            )

        return value


@dataclass
class FunctionCallNode(ExpressionNode):
    name: str
    args: list[ExpressionNode]

    def evaluate(self, memory: Any) -> Any:
        evaluated_args = [
            arg.evaluate(memory)
            for arg in self.args
        ]

        if hasattr(memory, "call_function"):
            return memory.call_function(
                self.name,
                evaluated_args
            )

        raise RuntimeError(
            f"Error en la linea {self.lineno}: "
            f"Funcion o llamada desconocida '{self.name}'."
        )


@dataclass
class BinaryOpNode(ExpressionNode):
    left: ExpressionNode
    op: str
    right: ExpressionNode

    def evaluate(self, memory: Any) -> Any:
        left_val = self.left.evaluate(memory)

        # Los operadores logicos aceptan cualquier tipo
        # y utilizan cortocircuito.
        if self.op == "and":
            if not left_val:
                return 0

            return 1 if self.right.evaluate(memory) else 0

        if self.op == "or":
            if left_val:
                return 1

            return 1 if self.right.evaluate(memory) else 0

        right_val = self.right.evaluate(memory)

        # Todos los operadores no logicos exigen
        # operandos del mismo tipo.
        if type(left_val) is not type(right_val):
            raise RuntimeError(
                f"Error en la linea {self.lineno}: "
                f"Los operandos de '{self.op}' deben ser del mismo tipo."
            )

        # Igualdad y desigualdad admiten enteros y textos.
        if self.op in ("==", "!="):
            if type(left_val) not in (int, str):
                raise RuntimeError(
                    f"Error en la linea {self.lineno}: "
                    f"Tipo de dato no valido para '{self.op}'."
                )

            if self.op == "==":
                return 1 if left_val == right_val else 0

            return 1 if left_val != right_val else 0

        # A partir de aqui, todos los operadores
        # requieren numeros enteros.
        if type(left_val) is not int:
            raise RuntimeError(
                f"Error en la linea {self.lineno}: "
                f"El operador '{self.op}' requiere operandos numericos."
            )

        if self.op == "+":
            return left_val + right_val

        elif self.op == "-":
            return left_val - right_val

        elif self.op == "*":
            return left_val * right_val

        elif self.op == "/":
            if right_val == 0:
                raise RuntimeError(
                    f"Error en la linea {self.lineno}: Division por cero."
                )

            return left_val // right_val

        elif self.op == "%":
            if right_val == 0:
                raise RuntimeError(
                    f"Error en la linea {self.lineno}: Modulo por cero."
                )

            return left_val % right_val

        elif self.op == "<":
            return 1 if left_val < right_val else 0

        elif self.op == ">":
            return 1 if left_val > right_val else 0

        elif self.op == "<=":
            return 1 if left_val <= right_val else 0

        elif self.op == ">=":
            return 1 if left_val >= right_val else 0

        raise RuntimeError(
            f"Error en la linea {self.lineno}: "
            f"Operador binario desconocido '{self.op}'."
        )


@dataclass
class UnaryOpNode(ExpressionNode):
    op: str
    operand: ExpressionNode

    def evaluate(self, memory: Any) -> Any:
        val = self.operand.evaluate(memory)

        if self.op == "-":
            if type(val) is not int:
                raise RuntimeError(
                    f"Error en la linea {self.lineno}: "
                    "El menos unario requiere un numero entero."
                )

            return -val

        elif self.op in ("not", "!"):
            return 0 if val else 1

        raise RuntimeError(
            f"Error en la linea {self.lineno}: "
            f"Operador unario desconocido '{self.op}'."
        )


def dump_ast(node, indent=0):
    pad = " " * indent

    if hasattr(node, "__dataclass_fields__"):
        print(f"{pad}{node.__class__.__name__}:")

        for field in node.__dataclass_fields__:
            value = getattr(node, field)

            if isinstance(value, list):
                print(f"{pad} {field}: [")

                for item in value:
                    dump_ast(item, indent + 2)

                print(f"{pad} ]")

            elif hasattr(value, "__dataclass_fields__"):
                print(f"{pad} {field}:")
                dump_ast(value, indent + 2)

            else:
                print(f"{pad} {field}: {value}")

    else:
        print(f"{pad}{node}")
