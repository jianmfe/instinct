from dataclasses import dataclass

from instinct.frontend.animation.animation_state import AnimationState


@dataclass(frozen=True, slots=True)
class AnimationDefinition:
    """Parámetros de reproducción de una spritesheet."""

    frame_count: int = 4
    frame_duration: int = 150
    loop: bool = False
    filename: str | None = None

    def __post_init__(self):
        if isinstance(self.frame_count, bool) or self.frame_count <= 0:
            raise ValueError("La cantidad de fotogramas debe ser positiva.")
        if isinstance(self.frame_duration, bool) or self.frame_duration <= 0:
            raise ValueError("La duración de los fotogramas debe ser positiva.")


DEFAULT_ANIMATIONS = {
    AnimationState.IDLE: AnimationDefinition(
        frame_count=4, frame_duration=180, loop=True
    ),
    AnimationState.WALK: AnimationDefinition(
        frame_count=6, frame_duration=110, loop=False
    ),
    AnimationState.RUN: AnimationDefinition(
        frame_count=6, frame_duration=85, loop=False
    ),
    AnimationState.ATTACK: AnimationDefinition(
        frame_count=6, frame_duration=90, loop=False
    ),
    AnimationState.HURT: AnimationDefinition(
        frame_count=3, frame_duration=110, loop=False
    ),
    AnimationState.DEATH: AnimationDefinition(
        frame_count=6, frame_duration=150, loop=False
    ),
    AnimationState.ROAR: AnimationDefinition(
        frame_count=5, frame_duration=120, loop=False
    ),
    AnimationState.CONSUME: AnimationDefinition(
        frame_count=5, frame_duration=130, loop=False
    ),
    AnimationState.REPRODUCE: AnimationDefinition(
        frame_count=5, frame_duration=140, loop=False
    ),
}


class AnimationConfig:
    """
    Configuración de animaciones por especie.

    Para personalizar una especie:
        AnimationConfig.register("naruto", {
            AnimationState.IDLE: AnimationDefinition(...),
        })
    Las animaciones no declaradas utilizan la configuración predeterminada.
    """

    _species_configs = {}

    @classmethod
    def register(cls, species_name, definitions):
        if not isinstance(species_name, str) or not species_name.strip():
            raise ValueError("El nombre de la especie no puede estar vacío.")

        normalized = {}
        for state, definition in definitions.items():
            if isinstance(state, str):
                state = AnimationState(state.lower())
            if not isinstance(state, AnimationState):
                raise TypeError("El estado de animación no es válido.")
            if not isinstance(definition, AnimationDefinition):
                raise TypeError(
                    "Cada configuración debe ser una AnimationDefinition."
                )
            normalized[state] = definition

        cls._species_configs[species_name.lower()] = normalized

    @classmethod
    def get(cls, species_name, state):
        if isinstance(state, str):
            state = AnimationState(state.lower())

        species = cls._species_configs.get(species_name.lower(), {})
        return species.get(state, DEFAULT_ANIMATIONS[state])

    @classmethod
    def clear_species(cls, species_name):
        cls._species_configs.pop(species_name.lower(), None)
