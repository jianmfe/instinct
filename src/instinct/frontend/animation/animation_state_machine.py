from instinct.frontend.animation.animation_state import AnimationState


class AnimationStateMachine:
    """FSM visual independiente para una instancia de criatura."""

    PRIORITY = {
        AnimationState.IDLE: 0,
        AnimationState.WALK: 10,
        AnimationState.RUN: 20,
        AnimationState.REPRODUCE: 40,
        AnimationState.CONSUME: 45,
        AnimationState.ROAR: 50,
        AnimationState.ATTACK: 60,
        AnimationState.HURT: 90,
        AnimationState.DEATH: 100,
    }

    def __init__(self):
        self.current_state = AnimationState.IDLE
        self.previous_state = None

    @property
    def is_dead(self):
        return self.current_state is AnimationState.DEATH

    def transition(self, new_state, force=False):
        """Intenta cambiar de estado respetando las prioridades."""

        if isinstance(new_state, str):
            new_state = AnimationState(new_state.lower())

        if not isinstance(new_state, AnimationState):
            raise TypeError("El estado de animación no es válido.")

        if self.is_dead:
            return False

        if new_state is self.current_state:
            # Repetir la misma acción reinicia su animación.
            return True

        current_priority = self.PRIORITY[self.current_state]
        new_priority = self.PRIORITY[new_state]

        if not force and new_priority < current_priority:
            return False

        self.previous_state = self.current_state
        self.current_state = new_state
        return True

    def finish_animation(self):
        """Finaliza una animación no repetitiva y vuelve a reposo."""

        if self.is_dead or self.current_state is AnimationState.IDLE:
            return False

        self.previous_state = self.current_state
        self.current_state = AnimationState.IDLE
        return True
