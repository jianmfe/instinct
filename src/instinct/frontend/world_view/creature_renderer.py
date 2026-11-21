import pygame

from instinct.frontend.animation.animation_controller import AnimationController
from instinct.frontend.animation.animation_state import AnimationState


class CreatureRenderer:
    """Carga spritesheets y dibuja criaturas usando estados visuales por instancia."""

    FRAME_WIDTH = 64
    FRAME_HEIGHT = 64

    def __init__(self, asset_loader, scale=1, animation_controller=None):
        self.asset_loader = asset_loader
        self.scale = scale
        self.animation_controller = (
            animation_controller or AnimationController()
        )
        self.spritesheets = {}

    def load_animation(
        self,
        creature_name,
        animation_name="idle",
        frame_count=None,
        frame_duration=None,
    ):
        """Carga una spritesheet; los parámetros opcionales permiten compatibilidad."""

        state = (
            animation_name
            if isinstance(animation_name, AnimationState)
            else AnimationState(animation_name.lower())
        )

        definition = self.animation_controller.config.get(
            creature_name,
            state,
        )

        if frame_count is None:
            frame_count = definition.frame_count

        if frame_duration is None:
            frame_duration = definition.frame_duration

        if frame_count <= 0 or frame_duration <= 0:
            raise ValueError(
                "La cantidad de fotogramas y su duración deben ser positivas."
            )

        key = (creature_name.lower(), state.value)

        if key in self.spritesheets:
            return self.spritesheets[key]

        path = (
            f"creatures/sprites/{creature_name.lower()}/"
            f"{(definition.filename or state.value).lower()}.png"
        )

        frames = self.asset_loader.load_sprite_sheet(
            path,
            frame_width=self.FRAME_WIDTH,
            frame_height=self.FRAME_HEIGHT,
            scale=self.scale,
        )

        if not frames:
            self.spritesheets[key] = None
            return None

        self.spritesheets[key] = {
            "frames": frames[:frame_count],
            "duration": frame_duration,
        }

        return self.spritesheets[key]

    def update(self, delta_time):
        """Actualiza los fotogramas y desplazamientos visuales."""

        self.animation_controller.update(delta_time)

    def draw_creature(self, screen, creature, camera):
        """Dibuja una criatura en su posición visual actual."""

        if creature is None:
            return

        state = self.animation_controller.get_state(creature)

        self._draw_with_state(
            screen,
            creature,
            camera,
            state,
        )

    def draw_death_animations(self, screen, camera):
        """Dibuja criaturas retiradas del mundo que aún están muriendo."""

        completed = []

        for creature, frame_index, finished in (
            self.animation_controller.iter_death_animations()
        ):
            self._draw_with_state(
                screen,
                creature,
                camera,
                AnimationState.DEATH,
                frame_index=frame_index,
            )

            if finished:
                completed.append(creature)

        for creature in completed:
            self.animation_controller.remove_creature(creature)

    def _draw_with_state(
        self,
        screen,
        creature,
        camera,
        state,
        frame_index=None,
    ):
        """Dibuja una criatura usando su estado y posición visual."""

        sheet = self.load_animation(
            creature.name,
            state,
        )

        if sheet is None or not sheet["frames"]:
            self._draw_placeholder(
                screen,
                creature,
                camera,
            )
            return

        if frame_index is None:
            frame_index = self.animation_controller.get_frame(
                creature
            )

        frames = sheet["frames"]

        frame = frames[
            min(frame_index, len(frames) - 1)
        ]

        size = max(
            1,
            int(self.FRAME_WIDTH * camera.zoom),
        )

        scaled_frame = pygame.transform.scale(
            frame,
            (size, size),
        )

        visual_x, visual_y = (
            self.animation_controller.get_visual_position(
                creature
            )
        )

        tile_left = visual_x * camera.tile_size
        
        tile_bottom = (
            visual_y + 1
        ) * camera.tile_size

        screen_x, screen_y = camera.world_to_screen(
            tile_left + camera.tile_size / 2,
            tile_bottom,
        )

        rect = scaled_frame.get_rect(
            midbottom=(
                int(screen_x),
                int(screen_y),
            )
        )

        screen.blit(
            scaled_frame,
            rect,
        )

    def _draw_placeholder(self, screen, creature, camera):
        """Dibuja un marcador cuando no existe la spritesheet."""

        visual_x, visual_y = (
            self.animation_controller.get_visual_position(
                creature
            )
        )

        center_x = (
            visual_x + 0.5
        ) * camera.tile_size

        center_y = (
            visual_y + 0.5
        ) * camera.tile_size

        screen_x, screen_y = camera.world_to_screen(
            center_x,
            center_y,
        )

        radius = max(
            3,
            int(camera.zoom * 6),
        )

        pygame.draw.circle(
            screen,
            (212, 174, 98),
            (
                int(screen_x),
                int(screen_y),
            ),
            radius,
        )
