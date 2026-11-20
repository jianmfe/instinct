
"""
Paquete del backend de Instinct.

Contiene el análisis léxico, sintáctico y semántico,
la construcción del AST y la compilación de programas.
"""

from instinct.backend.ast_nodes import (
    ASTNode,
    ActionNode,
    AssignNode,
    BinaryOpNode,
    FunctionCallNode,
    GotoNode,
    HeaderNode,
    IdentifierNode,
    IfGotoNode,
    LabelNode,
    NumberNode,
    ProgramNode,
    StringNode,
    UnaryOpNode,
    dump_ast,
)

from instinct.backend.compiler import compile_file
from instinct.backend.lexer import Lexer, LexerError
from instinct.backend.parser import Parser
from instinct.backend.semantic import SemanticAnalyzer, SemanticError
from instinct.backend.tokens import Token, TokenType


__all__ = [
    "ASTNode",
    "ActionNode",
    "AssignNode",
    "BinaryOpNode",
    "FunctionCallNode",
    "GotoNode",
    "HeaderNode",
    "IdentifierNode",
    "IfGotoNode",
    "LabelNode",
    "NumberNode",
    "ProgramNode",
    "StringNode",
    "UnaryOpNode",
    "dump_ast",
    "compile_file",
    "Lexer",
    "LexerError",
    "Parser",
    "SemanticAnalyzer",
    "SemanticError",
    "Token",
    "TokenType",
]
