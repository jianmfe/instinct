
import pytest

from instinct.engine.action_event import ActionEvent, ActionEventLog
from instinct.world.entities import Creature


@pytest.fixture
def actor() -> Creature:
    return Creature(
        name="Naruto",
        faction="Konoha",
        health=100,
        vision=5,
        lifespan=100,
    )


@pytest.fixture
def target() -> Creature:
    return Creature(
        name="Sasuke",
        faction="Konoha",
        health=80,
        vision=5,
        lifespan=100,
    )


@pytest.fixture
def event_log() -> ActionEventLog:
    return ActionEventLog()


def test_action_event_log_publish_preserves_actor_reference(
    event_log: ActionEventLog,
    actor: Creature,
) -> None:
    event = event_log.publish(
        tick=1,
        event_type="move",
        actor=actor,
    )

    assert event.actor_ref is actor
    assert event.actor_id == id(actor)
    assert event.actor_name == actor.name


def test_action_event_log_publish_preserves_target_reference(
    event_log: ActionEventLog,
    actor: Creature,
    target: Creature,
) -> None:
    event = event_log.publish(
        tick=1,
        event_type="attack",
        actor=actor,
        target=target,
    )

    assert event.actor_ref is actor
    assert event.target_ref is target
    assert event.target_id == id(target)
    assert event.target_name == target.name


def test_action_event_preserves_coordinates_snapshot(
    event_log: ActionEventLog,
    actor: Creature,
    target: Creature,
) -> None:
    actor.x, actor.y = 3, 4
    target.x, target.y = 5, 6

    event = event_log.publish(
        tick=1,
        event_type="attack",
        actor=actor,
        target=target,
    )

    actor.x, actor.y = 10, 10
    target.x, target.y = 20, 20

    assert (event.x, event.y) == (3, 4)
    assert (event.target_x, event.target_y) == (5, 6)


def test_action_event_keeps_reference_after_creature_is_removed(
    event_log: ActionEventLog,
    actor: Creature,
    target: Creature,
) -> None:
    event = event_log.publish(
        tick=1,
        event_type="death",
        actor=actor,
        target=target,
    )

    # Simula que la criatura deja de estar disponible en el mundo.
    removed_creatures = [target]
    removed_creatures.clear()

    assert event.target_ref is target
    assert event.target_ref.name == "Sasuke"


def test_action_event_data_is_immutable(
    event_log: ActionEventLog,
    actor: Creature,
) -> None:
    data = {"damage": 20}

    event = event_log.publish(
        tick=1,
        event_type="attack",
        actor=actor,
        data=data,
    )

    data["damage"] = 50

    assert event.data["damage"] == 20

    with pytest.raises(TypeError):
        event.data["damage"] = 100


def test_action_event_log_returns_immutable_events(
    event_log: ActionEventLog,
    actor: Creature,
) -> None:
    event_log.publish(1, "move", actor)

    events = event_log.events

    assert isinstance(events, tuple)
    assert len(events) == 1


def test_action_event_log_get_since(
    event_log: ActionEventLog,
    actor: Creature,
) -> None:
    event_log.publish(1, "move", actor)
    event_log.publish(2, "attack", actor)
    event_log.publish(3, "roar", actor)

    assert len(event_log.get_since(0)) == 3
    assert len(event_log.get_since(1)) == 2
    assert len(event_log.get_since(2)) == 1
    assert len(event_log.get_since(3)) == 0


def test_action_event_log_get_since_rejects_invalid_cursor(
    event_log: ActionEventLog,
) -> None:
    with pytest.raises(ValueError):
        event_log.get_since(-1)

    with pytest.raises(ValueError):
        event_log.get_since(True)


def test_action_event_log_clear(
    event_log: ActionEventLog,
    actor: Creature,
) -> None:
    event_log.publish(1, "move", actor)

    event_log.clear()

    assert len(event_log) == 0
    assert event_log.events == ()


def test_action_event_rejects_invalid_tick() -> None:
    with pytest.raises(ValueError):
        ActionEvent(
            tick=-1,
            event_type="move",
            actor_id=1,
            actor_name="Naruto",
            x=0,
            y=0,
        )


def test_action_event_rejects_invalid_event_type() -> None:
    with pytest.raises(ValueError):
        ActionEvent(
            tick=1,
            event_type="",
            actor_id=1,
            actor_name="Naruto",
            x=0,
            y=0,
        )


def test_action_event_rejects_invalid_actor_id() -> None:
    with pytest.raises(ValueError):
        ActionEvent(
            tick=1,
            event_type="move",
            actor_id=0,
            actor_name="Naruto",
            x=0,
            y=0,
        )


def test_action_event_rejects_incomplete_target_coordinates() -> None:
    with pytest.raises(ValueError):
        ActionEvent(
            tick=1,
            event_type="attack",
            actor_id=1,
            actor_name="Naruto",
            x=0,
            y=0,
            target_id=2,
            target_x=5,
        )


def test_action_event_rejects_mismatched_actor_reference(
    actor: Creature,
) -> None:
    with pytest.raises(ValueError):
        ActionEvent(
            tick=1,
            event_type="move",
            actor_id=id(actor) + 1,
            actor_name=actor.name,
            x=0,
            y=0,
            actor_ref=actor,
        )


def test_action_event_rejects_mismatched_target_reference(
    actor: Creature,
    target: Creature,
) -> None:
    with pytest.raises(ValueError):
        ActionEvent(
            tick=1,
            event_type="attack",
            actor_id=id(actor),
            actor_name=actor.name,
            x=0,
            y=0,
            target_id=id(target) + 1,
            target_ref=target,
        )


def test_action_event_log_rejects_invalid_actor(
    event_log: ActionEventLog,
) -> None:
    with pytest.raises(TypeError):
        event_log.publish(
            tick=1,
            event_type="move",
            actor="Naruto",
        )
