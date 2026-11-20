
import pytest


@pytest.fixture
def valid_creature_source():
    return """
creature TestCreature
faction test_faction
health 100
vision 5
lifespan 200

start:
    wait(1)
    goto start
"""
