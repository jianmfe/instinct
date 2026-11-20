from .tokens import TokenType
from .ast_nodes import (
    ProgramNode, HeaderNode, LabelNode,
    GotoNode, IfGotoNode, AssignNode,
    ActionNode, NumberNode, StringNode,
    IdentifierNode, FunctionCallNode,
    BinaryOpNode, UnaryOpNode
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None
        return self.current

    def match(self, token_type):
        return self.current and self.current.type == token_type


    def consume(self, token_type, error_msg):
        if self.match(token_type):
            token = self.current
            self.advance()
            return token
        raise SyntaxError(
            f"Error sintáctico en la línea {getattr(self.current, 'line', '?')}: "
            f"{error_msg}"
        )

    def peek_type(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1].type
        return None


    def parse(self):
        header = self.parse_header()
        statements = self.parse_body()
        has_start = any(isinstance(stmt, LabelNode) and stmt.name == 'start' for stmt in statements)
        if not has_start:
            raise SyntaxError(
                "Error de compilación: el programa no contiene la etiqueta "
                "obligatoria 'start:'."
            )

        return ProgramNode(header=header, statements=statements, lineno=getattr(header, 'lineno', 1))



    def parse_header(self):
        header_data = {}
        required_keys = {
            'creature', 'faction', 'health', 'vision', 'lifespan'
        }

        first_nonempty_line = True
        header_lineno = 1

        while self.current:
            # Ignorar saltos de línea y tokens vacíos.
            if self.current.type == TokenType.NEWLINE:
                self.advance()
                continue

            if not self.current.value or str(self.current.value).strip() == "":
                self.advance()
                continue

            # La primera línea no vacía debe comenzar con creature.
            if first_nonempty_line:
                if (
                    not self.match(TokenType.IDENTIFIER)
                    or self.current.value != 'creature'
                ):
                    raise SyntaxError(
                        f"Error sintáctico en la línea {getattr(self.current, 'line', 1)}: "
                        "la primera línea de la cabecera debe ser "
                        "'creature Nombre'."
                    )

                first_nonempty_line = False

            # La cabecera termina cuando aparece start.
            if self.match(TokenType.IDENTIFIER) and self.current.value == 'start':
                break

            if not self.match(TokenType.IDENTIFIER):
                raise SyntaxError(
                    f"Error sintáctico en la línea {getattr(self.current, 'line', 1)}: "
                    f"token inesperado en la cabecera: '{self.current.value}'."
                )

            key_token = self.current
            key = key_token.value
            header_lineno = getattr(key_token, 'line', 1)
            self.advance()

            if key not in required_keys:
                raise SyntaxError(
                    f"Error sintáctico en la línea {header_lineno}: "
                    f"atributo de cabecera desconocido '{key}'."
                )

            if key in header_data:
                raise SyntaxError(
                    f"Error sintáctico en la línea {header_lineno}: "
                    f"el atributo '{key}' está repetido."
                )

            if key in ('creature', 'faction'):
                val_token = self.consume(
                    TokenType.IDENTIFIER,
                    f"se esperaba un nombre para '{key}'."
                )
                header_data[key] = val_token.value

            else:
                val_token = self.consume(
                    TokenType.NUMBER,
                    f"se esperaba un número entero para '{key}'."
                )

                value = int(val_token.value)

                if value <= 0:
                    raise SyntaxError(
                        f"Error sintáctico en la línea {getattr(val_token, 'line', header_lineno)}: "
                        f"el atributo '{key}' debe ser mayor que cero."
                    )

                header_data[key] = value

            # Cada atributo debe ocupar su propia línea.
            if self.current and self.current.type != TokenType.NEWLINE:
                raise SyntaxError(
                    f"Error sintáctico en la línea {getattr(self.current, 'line', header_lineno)}: "
                    "contenido inesperado después del atributo de cabecera."
                )

        missing = required_keys - set(header_data.keys())

        if missing:
            raise SyntaxError(
                "Error de compilación: faltan atributos obligatorios: "
                + ", ".join(sorted(missing))
            )

        if not self.current:
            raise SyntaxError(
                "Error de compilación: falta la etiqueta obligatoria 'start:'."
            )

        return HeaderNode(
            creature=header_data['creature'],
            faction=header_data['faction'],
            health=header_data['health'],
            vision=header_data['vision'],
            lifespan=header_data['lifespan'],
            lineno=1
        )

    def parse_body(self):
        statements = []
        while self.current:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements

    def parse_statement(self):
    # Ignorar saltos de línea y tokens vacíos
        while self.current and (
            not self.current.value
            or str(self.current.value).strip() == ""
        ):
            self.advance()

        if not self.current:
            return None

        statement_line = getattr(self.current, 'line', 1)

        # LABEL:
        if self.match(TokenType.IDENTIFIER) and self.peek_type() == TokenType.COLON:
            label_token = self.current
            label_name = label_token.value

            self.advance()
            self.advance()

            return LabelNode(
                name=label_name,
                lineno=getattr(label_token, 'line', 1)
            )

        # GOTO LABEL
        if self.match(TokenType.GOTO):
            goto_token = self.current
            self.advance()

            target_token = self.consume(
                TokenType.IDENTIFIER,
                "se esperaba una etiqueta después de 'goto'."
            )

            return GotoNode(
                target=target_token.value,
                lineno=getattr(goto_token, 'line', 1)
            )

        # IF condition GOTO LABEL
        if self.match(TokenType.IF):
            if_token = self.current
            self.advance()

            condition = self.parse_expr()

            self.consume(
                TokenType.GOTO,
                "se esperaba 'goto' después de la condición."
            )

            target_token = self.consume(
                TokenType.IDENTIFIER,
                "se esperaba una etiqueta después de 'goto'."
            )

            return IfGotoNode(
                condition=condition,
                target=target_token.value,
                lineno=getattr(if_token, 'line', 1)
            )

        # ASSIGNMENT OR FUNCTION/ACTION CALL
        if self.match(TokenType.IDENTIFIER):
            ident_token = self.current
            self.advance()

            # Assignment: variable = expression
            if self.match(TokenType.ASSIGN):
                self.advance()

                expr = self.parse_expr()

                return AssignNode(
                    name=ident_token.value,
                    value=expr,
                    lineno=getattr(ident_token, 'line', 1)
                )

            # Function/action call: name(arguments)
            if self.match(TokenType.LPAREN):
                self.advance()

                args = self.parse_arguments()

                self.consume(
                    TokenType.RPAREN,
                    "falta ')' para cerrar la lista de argumentos."
                )

                return ActionNode(
                    name=ident_token.value,
                    args=args,
                    lineno=getattr(ident_token, 'line', 1)
                )

            raise SyntaxError(
                f"Error sintáctico en la línea {statement_line}: "
                f"se esperaba '=' o '(' después del identificador '{ident_token.value}'."
            )

        raise SyntaxError(
            f"Error sintáctico en la línea {statement_line}: "
            f"token inesperado '{self.current.value}'."
        )

    def parse_arguments(self):
        args = []
        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expr())
            while self.match(TokenType.COMMA):
                self.advance()
                args.append(self.parse_expr())
        return args

    def parse_expr(self):
        left = self.parse_and()

        while self.match(TokenType.OR):
            op_token = self.current
            self.advance()
            right = self.parse_and()
            left = BinaryOpNode(left=left, op=op_token.value , right=right, lineno=getattr(op_token, 'line', 1))

        return left

    def parse_and(self):
        left = self.parse_not()

        while self.match(TokenType.AND):
            op_token = self.current
            self.advance()
            right = self.parse_not()

            left = BinaryOpNode(
                left=left,
                op=op_token.value,
                right=right,
                lineno=getattr(op_token, 'line', 1)
            )

        return left

    def parse_not(self):
        if self.match(TokenType.NOT):
            op_token = self.current
            self.advance()

            operand = self.parse_not()

            return UnaryOpNode(
                op=op_token.value,
                operand=operand,
                lineno=getattr(op_token, 'line', 1)
            )

        return self.parse_equality()

    def parse_equality(self):
        left = self.parse_comparison()

        while self.current and self.current.type in (
            TokenType.EQUAL,
            TokenType.NOTEQUAL
        ):
            op_token = self.current
            self.advance()
            right = self.parse_comparison()

            left = BinaryOpNode(
                left=left,
                op=op_token.value,
                right=right,
                lineno=getattr(op_token, 'line', 1)
            )

        return left


    def parse_comparison(self):
        left = self.parse_additive()

        while self.current and self.current.type in (
            TokenType.LESS,
            TokenType.LESSEQUAL,
            TokenType.GREATER,
            TokenType.GREATEREQUAL
        ):
            op_token = self.current
            self.advance()
            right = self.parse_additive()

            left = BinaryOpNode(
                left=left,
                op=op_token.value,
                right=right,
                lineno=getattr(op_token, 'line', 1)
            )

        return left

    def parse_additive(self):
        left = self.parse_multiplicative()

        while self.current and self.current.type in(TokenType.PLUS, TokenType.MINUS):
            op_token = self.current
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOpNode(left=left, op=op_token.value, right=right, lineno=getattr(op_token, 'line', 1))

        return left

    def parse_multiplicative(self):
        left = self.parse_unary()

        while self.current and self.current.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_token = self.current
            self.advance()
            right = self.parse_unary()
            left = BinaryOpNode(left=left, op=op_token.value, right=right, lineno=getattr(op_token, 'line', 1))

        return left

    def parse_unary(self):
        if self.match(TokenType.MINUS):
            op_token = self.current
            self.advance()

            operand = self.parse_unary()

            return UnaryOpNode(
                op=op_token.value,
                operand=operand,
                lineno=getattr(op_token, 'line', 1)
            )

        return self.parse_primary()

    def parse_primary(self):
        if self.match(TokenType.NUMBER):
            val = self.current
            self.advance()
            return NumberNode(value=int(val.value), lineno=getattr(val, 'line', 1))

        if self.match(TokenType.STRING):
            val = self.current
            self.advance()
            return StringNode(value=val.value, lineno=getattr(val, 'line', 1))

        if self.match(TokenType.IDENTIFIER):
            ident_token = self.current
            self.advance()

            if self.match(TokenType.LPAREN):
                self.advance()
                args = self.parse_arguments()
                self.consume(
                    TokenType.RPAREN,
                    "falta ')' después de los argumentos."
                )
                return FunctionCallNode(name=ident_token.value, args=args, lineno=getattr(ident_token, 'line', 1))

            return IdentifierNode(name=ident_token.value, lineno=getattr(ident_token, 'line', 1))


        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expr()
            self.consume(TokenType.RPAREN, "falta ')' después de los argumentos.")
            return expr

        if self.current is None:
            raise SyntaxError(
                "Error sintáctico: final inesperado de la entrada; "
                "se esperaba una expresión."
            )

        raise SyntaxError(
            f"Error sintáctico en la línea {getattr(self.current, 'line', '?')}: "
            f"se esperaba una expresión, pero se encontró '{self.current.value}'."
        )