
import math

import pygame


class Camera:
    """Controla la posición y el zoom de la vista del mundo."""

    MIN_ZOOM = 0.25
    MAX_ZOOM = 8.0
    ZOOM_FACTOR = 1.25

    def __init__(
        self,
        viewport: pygame.Rect,
        world_width: int,
        world_height: int,
        tile_size: int = 32,
    ):
        self.viewport = viewport.copy()

        self.world_width = world_width
        self.world_height = world_height
        self.tile_size = tile_size

        # Centro del mundo en coordenadas de píxeles.
        self.x = world_width * tile_size / 2
        self.y = world_height * tile_size / 2

        # Ajusta inicialmente el mundo al espacio disponible.
        self.fit_to_viewport()

    @property
    def visible_width(self) -> float:
        return self.viewport.width / self.zoom

    @property
    def visible_height(self) -> float:
        return self.viewport.height / self.zoom

    def fit_to_viewport(self):
        """Ajusta el mundo completo al área disponible."""

        world_pixel_width = self.world_width * self.tile_size
        world_pixel_height = self.world_height * self.tile_size

        if world_pixel_width <= 0 or world_pixel_height <= 0:
            self.zoom = 1.0
            return

        zoom_x = self.viewport.width / world_pixel_width
        zoom_y = self.viewport.height / world_pixel_height

        # Utiliza el menor valor para evitar recortar el mapa.
        self.zoom = min(zoom_x, zoom_y)

        self.x = world_pixel_width / 2
        self.y = world_pixel_height / 2

    def world_to_screen(self, world_x: float, world_y: float):
        """Convierte coordenadas del mundo a coordenadas de pantalla."""

        screen_x = (
            self.viewport.centerx
            + (world_x - self.x) * self.zoom
        )

        screen_y = (
            self.viewport.centery
            + (world_y - self.y) * self.zoom
        )

        return round(screen_x), round(screen_y)

    def screen_to_world(self, screen_x: float, screen_y: float):
        """Convierte coordenadas de pantalla a coordenadas del mundo."""

        world_x = (
            self.x
            + (screen_x - self.viewport.centerx) / self.zoom
        )

        world_y = (
            self.y
            + (screen_y - self.viewport.centery) / self.zoom
        )

        return world_x, world_y

    def screen_to_tile(self, screen_x: float, screen_y: float):
        """Obtiene la casilla correspondiente a una posición de pantalla."""

        world_x, world_y = self.screen_to_world(
            screen_x,
            screen_y,
        )

        tile_x = math.floor(world_x / self.tile_size)
        tile_y = math.floor(world_y / self.tile_size)

        return tile_x, tile_y

    def get_tile_rect(self, tile_x: int, tile_y: int):
        """Obtiene el rectángulo de pantalla de una casilla."""

        world_x = tile_x * self.tile_size
        world_y = tile_y * self.tile_size

        left, top = self.world_to_screen(world_x, world_y)

        right, bottom = self.world_to_screen(
            world_x + self.tile_size,
            world_y + self.tile_size,
        )

        return pygame.Rect(
            left,
            top,
            right - left,
            bottom - top,
        )

    def pan(self, dx: float, dy: float):
        """Desplaza la cámara según el movimiento del ratón."""

        self.x -= dx / self.zoom
        self.y -= dy / self.zoom

    def set_zoom(self, zoom: float, mouse_position=None):
        """Cambia el zoom manteniendo fija la posición bajo el cursor."""

        zoom = max(
            self.MIN_ZOOM,
            min(self.MAX_ZOOM, float(zoom)),
        )

        if math.isclose(zoom, self.zoom):
            return

        if mouse_position is None:
            mouse_position = self.viewport.center

        world_before = self.screen_to_world(*mouse_position)

        self.zoom = zoom

        world_after = self.screen_to_world(*mouse_position)

        self.x += world_before[0] - world_after[0]
        self.y += world_before[1] - world_after[1]

    def zoom_in(self, mouse_position=None):
        """Acerca la vista."""

        self.set_zoom(
            self.zoom * self.ZOOM_FACTOR,
            mouse_position,
        )

    def zoom_out(self, mouse_position=None):
        """Aleja la vista."""

        self.set_zoom(
            self.zoom / self.ZOOM_FACTOR,
            mouse_position,
        )

    def get_visible_tiles(self):
        """Devuelve los límites de las casillas que pueden verse."""

        left = self.x - self.visible_width / 2
        top = self.y - self.visible_height / 2

        right = self.x + self.visible_width / 2
        bottom = self.y + self.visible_height / 2

        start_x = max(0, math.floor(left / self.tile_size))
        start_y = max(0, math.floor(top / self.tile_size))

        end_x = min(
            self.world_width,
            math.ceil(right / self.tile_size),
        )

        end_y = min(
            self.world_height,
            math.ceil(bottom / self.tile_size),
        )

        return start_x, start_y, end_x, end_y

    def set_viewport(self, viewport: pygame.Rect):
        """Actualiza el área disponible y reajusta el mundo."""

        self.viewport = viewport.copy()
        self.fit_to_viewport()
