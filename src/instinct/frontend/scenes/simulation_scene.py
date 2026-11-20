
from pathlib import Path

import pygame


from instinct.frontend.scenes.base_scene import BaseScene
from instinct.frontend.settings import DEFAULT_TILE_SIZE

from instinct.loaders.resource_manager import ResourceManager
from instinct.engine.simulation import Simulation

from instinct.frontend.core.simulation_controller import (
    SimulationController,
)

from instinct.frontend.menu.asset_loader import AssetLoader

from instinct.frontend.world_view.camera import Camera
from instinct.frontend.world_view.world_renderer import WorldRenderer
from instinct.frontend.world_view.creature_renderer import CreatureRenderer
from instinct.frontend.world_view.selection import Selection


class SimulationScene(BaseScene):
    """Escena principal de visualización y control del mundo."""

    def __init__(self, game):
        super().__init__(game)

        self.title_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 24)

        self.resource_manager = None
        self.simulation = None
        self.controller = None

        self.asset_loader = AssetLoader()

        self.world_renderer = WorldRenderer(
            asset_loader=self.asset_loader,
            show_grid=True,
        )

        self.creature_renderer = CreatureRenderer(
            self.asset_loader,
        )

        self.selection = Selection()

        self.camera = None
        self.world = None

        self.map_name = None
        self.error_message = None

        self.dragging = False
        self.last_mouse_position = None

        self._load_resources()

    def _load_resources(self):
        """Carga los recursos y prepara el primer mapa disponible."""

        project_root = Path(__file__).resolve().parents[4]
        resources_path = project_root / "resources"

        self.resource_manager = ResourceManager(
            resource_dir=resources_path,
        )

        self.resource_manager.load_all()

        if not self.resource_manager.maps:
            self.error_message = (
                "No hay mapas disponibles para iniciar la simulación."
            )
            return

        # Seleccionamos provisionalmente el primer mapa disponible.
        self.map_name = next(iter(self.resource_manager.maps))

        self._load_map(self.map_name)

    def _load_map(self, map_name):
        """Inicializa una simulación utilizando un mapa existente."""

        world = self.resource_manager.get_map(map_name)

        if world is None:
            self.error_message = (
                f"No se encontró el mapa '{map_name}'."
            )
            return

        self.world = world
        self._place_naruto()

        self.simulation = Simulation(self.world)

        self.controller = SimulationController(
            simulation=self.simulation,
        )

        screen_width, screen_height = self.game.screen.get_size()

        viewport = pygame.Rect(
            40,
            90,
            screen_width - 80,
            screen_height - 150,
        )

        self.camera = Camera(
            viewport=viewport,
            world_width=self.world.width,
            world_height=self.world.height,
            tile_size=DEFAULT_TILE_SIZE,
        )

        # Utilizamos el zoom inicial definido para el proyecto.
        self.camera.zoom = 1

        self.world_renderer.set_world(self.world)
        self.world_renderer.set_camera(self.camera)

        self.selection.clear()
        self.error_message = None

    def _place_naruto(self):
        """Crea y coloca una instancia de Naruto en el centro del mapa."""

        naruto = self.resource_manager.create_creature("Naruto")

        if naruto is None:
            print("No se encontró la plantilla de Naruto.")
            return

        x = self.world.width // 2
        y = self.world.height // 2

        self.world.place_creature(naruto, x, y)

        print(f"Naruto colocado en ({x}, {y}).")

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                from instinct.frontend.scenes.main_menu import MainMenu

                self.game.scene_manager.change_scene(
                    MainMenu(self.game)
                )
                return

            if self.controller is None:
                return

            if event.key == pygame.K_SPACE:
                self.controller.toggle_pause()

            elif event.key == pygame.K_PERIOD:
                self.controller.step()

            elif event.key == pygame.K_RIGHTBRACKET:
                self.controller.increase_speed()

            elif event.key == pygame.K_LEFTBRACKET:
                self.controller.decrease_speed()

            elif event.key == pygame.K_g:
                self.world_renderer.toggle_grid()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.camera is None:
                return

            if event.button == 1:
                self.selection.handle_click(
                    world=self.world,
                    camera=self.camera,
                    mouse_position=event.pos,
                    shift=bool(event.mod & pygame.KMOD_SHIFT),
                )

            elif event.button == 2:
                self.dragging = True
                self.last_mouse_position = event.pos

            elif event.button == 4:
                self.camera.zoom_in(event.pos)

            elif event.button == 5:
                self.camera.zoom_out(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 2:
                self.dragging = False
                self.last_mouse_position = None

        elif event.type == pygame.MOUSEMOTION:

            if self.dragging and self.camera is not None:
                current_position = event.pos

                dx = current_position[0] - self.last_mouse_position[0]
                dy = current_position[1] - self.last_mouse_position[1]

                self.camera.pan(dx, dy)

                self.last_mouse_position = current_position

        elif event.type == pygame.MOUSEWHEEL:

            if self.camera is not None:
                mouse_position = pygame.mouse.get_pos()

                if event.y > 0:
                    self.camera.zoom_in(mouse_position)

                elif event.y < 0:
                    self.camera.zoom_out(mouse_position)

        elif event.type == pygame.VIDEORESIZE:

            if self.camera is not None:
                width, height = event.size

                viewport = pygame.Rect(
                    40,
                    90,
                    width - 80,
                    height - 150,
                )

                self.camera.set_viewport(viewport)

    def update(self, delta_time):

        if self.controller is not None:
            self.controller.update(delta_time)

        if self.camera is not None:
            self.creature_renderer.update(delta_time)

    def draw(self, screen):

        screen.fill((17, 22, 41))

        if self.error_message is not None:
            self._draw_error(screen)
            return

        if self.world is None:
            return

        self.world_renderer.draw(screen)

        self._draw_creatures(screen)

        self.selection.draw(
            screen,
            self.camera,
        )

        self._draw_interface(screen)

    def _draw_creatures(self, screen):
        """Dibuja las criaturas existentes en las casillas visibles."""

        start_x, start_y, end_x, end_y = (
            self.camera.get_visible_tiles()
        )

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):

                tile = self.world.get_tile(x, y)

                if tile is None or tile.creature is None:
                    continue

                self.creature_renderer.draw_creature(
                    screen,
                    tile.creature,
                    self.camera,
                )

    def _draw_interface(self, screen):
        """Dibuja información básica de la simulación."""

        title = self.title_font.render(
            f"INSTINCT | {self.map_name}",
            True,
            (212, 174, 98),
        )

        screen.blit(title, (40, 25))

        if self.controller is not None:

            status = (
                "PAUSADA"
                if self.controller.paused
                else "EN EJECUCIÓN"
            )

            info = (
                f"Tick: {self.controller.tick}  |  "
                f"Estado: {status}  |  "
                f"Velocidad: {self.controller.speed}x"
            )

            info_surface = self.info_font.render(
                info,
                True,
                (242, 239, 250),
            )

            screen.blit(
                info_surface,
                (40, 65),
            )

        controls = (
            "ESPACIO: Pausar/Reanudar | "
            ".: Avanzar tick | "
            "G: Cuadrícula | "
            "[ / ]: Velocidad | "
            "Rueda: Zoom | "
            "Botón central: Mover cámara | "
            "ESC: Menú"
        )

        controls_surface = self.info_font.render(
            controls,
            True,
            (170, 166, 190),
        )

        screen.blit(
            controls_surface,
            (40, screen.get_height() - 35),
        )

    def _draw_error(self, screen):

        title = self.title_font.render(
            "No se pudo iniciar el mundo",
            True,
            (212, 174, 98),
        )

        message = self.info_font.render(
            self.error_message,
            True,
            (242, 239, 250),
        )

        screen.blit(
            title,
            title.get_rect(
                center=(screen.get_width() // 2, 450)
            ),
        )

        screen.blit(
            message,
            message.get_rect(
                center=(screen.get_width() // 2, 510)
            ),
        )

        hint = self.info_font.render(
            "Pulsa ESC para volver al menú",
            True,
            (170, 166, 190),
        )

        screen.blit(
            hint,
            hint.get_rect(
                center=(screen.get_width() // 2, 580)
            ),
        )
