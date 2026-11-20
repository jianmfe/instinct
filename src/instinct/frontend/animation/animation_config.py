
from dataclasses import dataclass

from instinct.frontend.animation.animation_state import AnimationState


@dataclass(frozen=True, slots=True)
class AnimationDefinition:
    """Configuración de una animación individual."""

    frame_count: int
    frame_duration: int
    loop: bool = True
    filename: str | None = None


class AnimationConfig:
    """Configuraciones de animación organizadas por especie."""

    DEFAULT_ANIMATIONS = {
        AnimationState.IDLE: AnimationDefinition(
            frame_count=4,
            frame_duration=180,
            loop=True,
        ),
        AnimationState.WALK: AnimationDefinition(
            frame_count=6,
            frame_duration=150,
            loop=True,
        ),
        AnimationState.RUN: AnimationDefinition(
            frame_count=6,
            frame_duration=120,
            loop=True,
        ),
        AnimationState.ATTACK: AnimationDefinition(
            frame_count=6,
            frame_duration=120,
            loop=False,
        ),
        AnimationState.HURT: AnimationDefinition(
            frame_count=3,
            frame_duration=150,
            loop=False,
        ),
        AnimationState.DEATH: AnimationDefinition(
            frame_count=6,
            frame_duration=180,
            loop=False,
        ),
    }

    CREATURES = {
        "naruto": {
            AnimationState.IDLE: AnimationDefinition(
                frame_count=4,
                frame_duration=180,
                loop=True,
                filename="idle",
            ),
            AnimationState.WALK: AnimationDefinition(
                frame_count=6,
                frame_duration=150,
                loop=True,
                filename="walk",
            ),
            AnimationState.RUN: AnimationDefinition(
                frame_count=6,
                frame_duration=120,
                loop=True,
                filename="run",
            ),
            AnimationState.ATTACK: AnimationDefinition(
                frame_count=6,
                frame_duration=120,
                loop=False,
                filename="attack",
            ),
            AnimationState.HURT: AnimationDefinition(
                frame_count=3,
                frame_duration=150,
                loop=False,
                filename="damage",
            ),
            AnimationState.DEATH: AnimationDefinition(
                frame_count=6,
                frame_duration=180,
                loop=False,
                filename="death",
            ),
        },
    }

    @classmethod
    def get(cls, creature_name, state):
        """Obtiene la configuración de una animación.

        Si una especie no tiene configuración propia, utiliza
        la configuración predeterminada.
        """

        creature_name = creature_name.lower()

        if isinstance(state, str):
            state = AnimationState(state.lower())

        creature_config = cls.CREATURES.get(
            creature_name,
            {},
        )

        return (
            creature_config.get(state)
            or cls.DEFAULT_ANIMATIONS.get(state)
            or cls.DEFAULT_ANIMATIONS[AnimationState.IDLE]
        )
