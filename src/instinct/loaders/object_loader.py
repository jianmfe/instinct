from pathlib import Path

from instinct.world.entities import WorldObject


class ObjectLoader:
    """Carga y valida definiciones de objetos desde archivos .ob."""

    REQUIRED_FIELDS = {"char", "resource_max"}

    def load_file(self, filepath: str | Path) -> WorldObject:
        """Lee un archivo .ob y devuelve el objeto definido en él."""
        path = Path(filepath)

        try:
            content = path.read_text(encoding="utf-8")
        except FileNotFoundError as error:
            raise ValueError(
                f"No se encontró el archivo de objeto: '{path}'."
            ) from error
        except UnicodeDecodeError as error:
            raise ValueError(
                f"El archivo de objeto '{path}' no contiene texto UTF-8 válido."
            ) from error
        except OSError as error:
            raise ValueError(
                f"No se pudo leer el archivo de objeto '{path}': {error}."
            ) from error

        return self.load_string(content, source=str(path))

    def load_string(
        self,
        content: str,
        source: str = "<memoria>",
    ) -> WorldObject:
        """Analiza el contenido de un archivo .ob."""

        if not isinstance(content, str):
            raise TypeError("El contenido del objeto debe ser texto.")

        lines = content.splitlines()
        declaration = None
        declaration_line = 0
        fields: dict[str, tuple[str, int]] = {}

        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(maxsplit=1)
            key = parts[0]

            if declaration is None:
                if key != "object" or len(parts) != 2:
                    self._error(
                        source,
                        line_number,
                        "Se esperaba una declaración 'object Nombre'.",
                    )

                name = parts[1].strip()

                if not name or len(name.split()) != 1:
                    self._error(
                        source,
                        line_number,
                        "El nombre del objeto debe ser una sola palabra.",
                    )

                declaration = name
                declaration_line = line_number
                continue

            if key not in self.REQUIRED_FIELDS:
                self._error(
                    source,
                    line_number,
                    f"Propiedad desconocida '{key}' en el objeto.",
                )

            if key in fields:
                self._error(
                    source,
                    line_number,
                    f"La propiedad '{key}' está duplicada.",
                )

            if len(parts) != 2 or not parts[1].strip():
                self._error(
                    source,
                    line_number,
                    f"Falta el valor de la propiedad '{key}'.",
                )

            fields[key] = (parts[1].strip(), line_number)

        if declaration is None:
            self._error(source, 1, "El archivo no declara ningún objeto.")

        for field in self.REQUIRED_FIELDS:
            if field not in fields:
                self._error(
                    source,
                    declaration_line,
                    f"Falta la propiedad obligatoria '{field}'.",
                )

        char = fields["char"][0]

        if len(char) != 1:
            self._error(
                source,
                fields["char"][1],
                "El carácter del objeto debe tener exactamente un símbolo.",
            )

        resource_max = self._parse_integer(
            fields["resource_max"][0],
            "resource_max",
            source,
            fields["resource_max"][1],
        )

        if resource_max < 0:
            self._error(
                source,
                fields["resource_max"][1],
                "'resource_max' no puede ser negativo.",
            )

        return WorldObject(
            name=declaration,
            char=char,
            resource_max=resource_max,
        )

    @staticmethod
    def _parse_integer(
        value: str,
        field: str,
        source: str,
        line_number: int,
    ) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError(
                f"Error en '{source}', línea {line_number}: "
                f"'{field}' debe ser un número entero."
            ) from None

    @staticmethod
    def _error(source: str, line: int, message: str) -> None:
        raise ValueError(
            f"Error en '{source}', línea {line}: {message}"
        )
