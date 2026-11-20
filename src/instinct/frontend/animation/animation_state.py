from enum import Enum


class AnimationState(str, Enum):
    """Estados visuales disponibles para una criatura."""

    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    ATTACK = "attack"
    HURT = "hurt"
    DEATH = "death"
    ROAR = "roar"
    CONSUME = "consume"
    REPRODUCE = "reproduce"
