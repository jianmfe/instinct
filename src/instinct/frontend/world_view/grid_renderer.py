import pygame


class GridRenderer:
    """Dibuja la cuadrícula del mundo."""

    def __init__(
        self,
        color=(35, 38, 55),
        enabled=True,
        max_zoom=3,
    ):
        self.color = color
        self.enabled = enabled
        self.max_zoom = max_zoom

    def draw(self, screen, camera):
        """Dibuja las líneas de las casillas visibles."""

        if not self.enabled:
            return

        viewport = camera.viewport
        tile_size = camera.tile_size * camera.zoom

        if tile_size <= 0:
            return

        start_x, start_y, end_x, end_y = camera.get_visible_tiles()

        if start_x >= end_x or start_y >= end_y:
            return

        previous_clip = screen.get_clip()
        screen.set_clip(viewport)

        line_width = 1

        # Líneas verticales.
        for x in range(start_x, end_x + 1):
            world_x = x * camera.tile_size
            screen_x, _ = camera.world_to_screen(world_x, 0)

            pygame.draw.line(
                screen,
                self.color,
                (screen_x, viewport.top),
                (screen_x, viewport.bottom),
                line_width,
            )

        # Líneas horizontales.
        for y in range(start_y, end_y + 1):
            world_y = y * camera.tile_size
            _, screen_y = camera.world_to_screen(0, world_y)

            pygame.draw.line(
                screen,
                self.color,
                (viewport.left, screen_y),
                (viewport.right, screen_y),
                line_width,
            )

        screen.set_clip(previous_clip)

    def toggle(self):
        """Activa o desactiva la cuadrícula."""

        self.enabled = not self.enabled

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_color(self, color):
        self.color = color
