from pathlib import Path

from instinct.backend.compiler import compile_file
from instinct.runtime.program import Program
from instinct.world.entities import Creature


class CreatureLoader:
    """Carga criaturas a partir de programas escritos en Instinct."""

    def load_file(self, filepath: str | Path) -> Creature:
        path = Path(filepath)

        try:
            ast = compile_file(str(path))
        except FileNotFoundError as error:
            raise ValueError(
                f"No se encontró el archivo de criatura: '{path}'."
            ) from error
        except UnicodeDecodeError as error:
            raise ValueError(
                f"El archivo de criatura '{path}' no contiene texto UTF-8 válido."
            ) from error
        except OSError as error:
            raise ValueError(
                f"No se pudo leer el archivo de criatura '{path}': {error}."
            ) from error
        except Exception as error:
            raise ValueError(
                f"No se pudo compilar la criatura '{path}': {error}"
            ) from error

        return self.load_ast(ast, source=str(path))

    def load_ast(self, ast, source: str = "<memoria>") -> Creature:
        """Construye una criatura a partir de un AST compilado."""

        if ast is None or not hasattr(ast, "header"):
            raise ValueError(
                f"El archivo '{source}' no contiene una cabecera válida."
            )

        header = ast.header
        program = Program(ast)

        try:
            return Creature(
                name=header.creature,
                faction=header.faction,
                health=header.health,
                vision=header.vision,
                lifespan=header.lifespan,
                program=program,
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Error en la cabecera de la criatura '{source}': {error}"
            ) from error
