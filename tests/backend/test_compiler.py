
import pytest

from instinct.backend.ast_nodes import ProgramNode
from instinct.backend.compiler import compile_file
from instinct.runtime.program import Program


def test_compile_file_returns_program_node(
    tmp_path,
    valid_creature_source,
):
    script = tmp_path / "test_creature.ins"
    script.write_text(valid_creature_source, encoding="utf-8")

    ast = compile_file(str(script))

    assert isinstance(ast, ProgramNode)


def test_compiled_header_contains_creature_attributes(
    tmp_path,
    valid_creature_source,
):
    script = tmp_path / "test_creature.ins"
    script.write_text(valid_creature_source, encoding="utf-8")

    ast = compile_file(str(script))

    assert ast.header.creature == "TestCreature"
    assert ast.header.faction == "test_faction"
    assert ast.header.health == 100
    assert ast.header.vision == 5
    assert ast.header.lifespan == 200


def test_compiled_ast_can_be_wrapped_in_program(
    tmp_path,
    valid_creature_source,
):
    script = tmp_path / "test_creature.ins"
    script.write_text(valid_creature_source, encoding="utf-8")

    ast = compile_file(str(script))
    program = Program(ast)

    assert isinstance(program, Program)
    assert program.header is ast.header
    assert len(program) == len(ast.statements)


def test_program_registers_start_label(
    tmp_path,
    valid_creature_source,
):
    script = tmp_path / "test_creature.ins"
    script.write_text(valid_creature_source, encoding="utf-8")

    ast = compile_file(str(script))
    program = Program(ast)

    assert program.has_label("start")
    assert program.start_position == program.get_label_position("start")


def test_compile_file_raises_error_for_missing_file(tmp_path):
    missing_script = tmp_path / "inexistent.ins"

    with pytest.raises(FileNotFoundError):
        compile_file(str(missing_script))
