
import pygame


class CreatureRenderer:
    """Representa y anima las criaturas del mundo."""

    FRAME_WIDTH = 64
    FRAME_HEIGHT = 64
    DEFAULT_FRAME_DURATION = 150

    def __init__(self, asset_loader, scale=1):
        self.asset_loader = asset_loader
        self.scale = scale

        # Spritesheets cargados por criatura y animación.
        self.spritesheets = {}

        # Estado de cada animación.
        self.animations = {}

        # Animación seleccionada para cada tipo de criatura.
        self.active_animations = {}

    def load_animation(
        self,
        creature_name,
        animation_name="idle",
        frame_count=4,
        frame_duration=DEFAULT_FRAME_DURATION,
    ):
        """Carga una animación de una criatura."""

        if frame_count <= 0 or frame_duration <= 0:
            raise ValueError(
                "La cantidad de fotogramas y su duración deben ser positivas."
            )

        key = (creature_name.lower(), animation_name.lower())

        if key in self.spritesheets:
            return self.spritesheets[key]

        path = (
            f"creatures/sprites/{creature_name.lower()}/"
            f"{animation_name.lower()}.png"
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

        frames = frames[:frame_count]

        self.spritesheets[key] = {
            "frames": frames,
            "duration": frame_duration,
        }

        self.animations[key] = {
            "frame": 0,
            "elapsed": 0,
        }

        return self.spritesheets[key]

    def set_animation(
        self,
        creature_name,
        animation_name,
        frame_count=4,
        frame_duration=DEFAULT_FRAME_DURATION,
    ):
        """Cambia la animación activa de una criatura."""

        creature_key = creature_name.lower()
        animation_name = animation_name.lower()

        sheet = self.load_animation(
            creature_name,
            animation_name,
            frame_count,
            frame_duration,
        )

        if sheet is None:
            return False

        animation_key = (creature_key, animation_name)

        # Reiniciar la animación desde el primer fotograma.
        self.animations[animation_key] = {
            "frame": 0,
            "elapsed": 0,
        }

        self.active_animations[creature_key] = animation_name

        return True

    def update(self, delta_time):
        """Actualiza los fotogramas de las animaciones activas."""

        delta_ms = delta_time * 1000

        for creature_name, animation_name in self.active_animations.items():
            key = (creature_name, animation_name)
            sheet = self.spritesheets.get(key)

            if sheet is None:
                continue

            frames = sheet["frames"]

            if len(frames) <= 1:
                continue

            animation = self.animations[key]
            animation["elapsed"] += delta_ms

            while animation["elapsed"] >= sheet["duration"]:
                animation["elapsed"] -= sheet["duration"]
                animation["frame"] = (
                    animation["frame"] + 1
                ) % len(frames)

    def draw_creature(self, screen, creature, camera):
        """Dibuja una criatura animada en el mundo."""

        if creature is None:
            return

        creature_key = creature.name.lower()

        # Si no tiene una animación seleccionada, usar idle.
        if creature_key not in self.active_animations:
            self.set_animation(creature.name, "idle")

        animation_name = self.active_animations.get(
            creature_key,
            "idle",
        )

        animation_key = (creature_key, animation_name)
        sheet = self.spritesheets.get(animation_key)

        if sheet is None:
            self._draw_placeholder(screen, creature, camera)
            return

        frames = sheet["frames"]

        if not frames:
            self._draw_placeholder(screen, creature, camera)
            return

        animation = self.animations[animation_key]
        frame = frames[animation["frame"]]

        size = int(self.FRAME_WIDTH * camera.zoom)

        tile_center_x = (
            creature.x * camera.tile_size
            + camera.tile_size / 2
        )

        tile_center_y = (
            creature.y * camera.tile_size
            + camera.tile_size / 2
        )

        screen_x, screen_y = camera.world_to_screen(
            tile_center_x,
            tile_center_y,
        )

        scaled_frame = pygame.transform.scale(
            frame,
            (size, size),
        )

        rect = scaled_frame.get_rect(
            center=(int(screen_x), int(screen_y))
        )

        screen.blit(scaled_frame, rect)

    def _draw_placeholder(self, screen, creature, camera):
        """Dibuja un marcador si no existe la spritesheet."""

        center_x = (creature.x + 0.5) * camera.tile_size
        center_y = (creature.y + 0.5) * camera.tile_size

        screen_x, screen_y = camera.world_to_screen(
            center_x,
            center_y,
        )

        radius = max(3, int(camera.zoom * 6))

        pygame.draw.circle(
            screen,
            (212, 174, 98),
            (int(screen_x), int(screen_y)),
            radius,
        )
